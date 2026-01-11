# n8n Workflow Assignment: Smart Expense Tracker with Budget Monitoring

video-link: https://epam-my.sharepoint.com/:v:/r/personal/anuar_sultan_epam_com/Documents/Recordings/06-no-code-agent-platform-20260111_230836-Meeting%20Recording.mp4?csf=1&web=1&e=XeUDbS&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D

## 1. Workflow Purpose and Scenario

### Overview
This n8n workflow automates personal expense tracking through Telegram with intelligent features:
- **Multi-currency support** - Accepts expenses in USD, EUR, GBP, KZT, RUB with automatic conversion
- **AI-powered classification** - Uses OpenAI GPT-4o-mini to categorize expenses
- **Automatic storage** - Saves all data to Google Sheets with timestamps
- **Real-time budget alerts** - Monitors daily, weekly, and monthly spending limits
- **Instant feedback** - Confirms each entry via Telegram

### Real-World Use Case
A freelancer working internationally needs to track expenses in multiple currencies. Instead of manually entering data into spreadsheets and converting currencies, they simply message their Telegram bot:
- `100 lunch cafe` → Automatically categorized as "Food"
- `€25 grocery` → Converted to USD at current exchange rate
- `₸5000 taxi home` → Converted and categorized as "Transport"

The system automatically:
1. Detects the currency (or defaults to USD)
2. Converts to USD using live exchange rates
3. Classifies the expense using AI
4. Stores in Google Sheets
5. Checks against budget limits and alerts if exceeded
6. Sends a confirmation message

---

## 2. Key Nodes and Logic

### Workflow Architecture

```
┌─────────────────────┐
│  Telegram Trigger   │ (Webhook - receives expense messages)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Parse Message     │ (Detect currency, extract amount & description)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    IF: USD?         │ (Check if currency conversion needed)
└──────────┬──────────┘
     ┌─────┴─────┐
     ▼           ▼
  [USD]    [Other Currency]
     │           │
     │           ▼
     │    ┌──────────────┐
     │    │ HTTP Request │ (Get exchange rates)
     │    └──────┬───────┘
     │           │
     │           ▼
     │    ┌──────────────┐
     │    │   Convert    │ (Convert to USD)
     │    └──────┬───────┘
     │           │
     └───────┬───┘
             ▼
      ┌─────────────┐
      │  OpenAI     │ (Classify expense category with AI)
      │ GPT-4o-mini │
      └──────┬──────┘
             │
             ▼
      ┌─────────────┐
      │Parse OpenAI │ (Extract structured JSON)
      │   Output    │
      └──────┬──────┘
             │
             ▼
      ┌─────────────┐
      │Google Sheets│ (Append row: timestamp, amount, currency, category)
      └──────┬──────┘
             │
        ┌────┴────┐
        ▼         ▼
  ┌─────────┐  ┌──────────────┐
  │Telegram │  │Google Sheets │ (Get all rows)
  │ Reply   │  │  Read All    │
  └─────────┘  └──────┬───────┘
                      │
                      ▼
               ┌──────────────┐
               │Budget Check  │ (Calculate daily/weekly/monthly totals)
               └──────┬───────┘
                      │
                      ▼
               ┌──────────────┐
               │ IF: Alert?   │ (Check if limits exceeded)
               └──────┬───────┘
                   ┌──┴──┐
                   ▼     ▼
              [Yes]      [No - Skip]
                   │
                   ▼
            ┌──────────┐
            │ Telegram │ (Send budget alert with totals)
            │  Alert   │
            └──────────┘
```

### Detailed Node Descriptions

#### 1. **Telegram Trigger** (Webhook)
- **Type**: Telegram Trigger
- **Event**: Message
- **Purpose**: Listens for expense messages from users
- **Output**: Full Telegram message object with text, user info

#### 2. **Parse Message** (Code Node)
Advanced parsing with multi-currency support:
```javascript
const text = $json.message?.text || $json.text || '';
const chatId = $json.message?.chat?.id || $json.chat?.id || null;

// Currency detection patterns
const currencyPatterns = [
  { symbol: '$', code: 'USD', regex: /\$\s*(\d+[\.,]?\d*)/ },
  { symbol: '€', code: 'EUR', regex: /€\s*(\d+[\.,]?\d*)/ },
  { symbol: '£', code: 'GBP', regex: /£\s*(\d+[\.,]?\d*)/ },
  { symbol: '₸', code: 'KZT', regex: /₸\s*(\d+[\.,]?\d*)/ },
  { symbol: '₽', code: 'RUB', regex: /₽\s*(\d+[\.,]?\d*)/ }
];

// Supports both "100 lunch" and "lunch 100" formats
// Returns: amount, currency, description, needs_conversion flag
```

#### 3. **IF USD** (Conditional Node)
- **Condition**: `needs_conversion === true`
- **True Branch**: Fetch exchange rates and convert
- **False Branch**: Skip to OpenAI classification

#### 4. **HTTP Request** (Exchange Rate API)
- **URL**: `https://api.exchangerate-api.com/v4/latest/{currency}`
- **Purpose**: Get real-time exchange rates
- **Output**: Exchange rates for all currencies

#### 5. **Convert Currency** (Code Node)
Converts amount to USD:
```javascript
const usdRate = rates?.USD || 1;
const convertedAmount = originalAmount * usdRate;
// Preserves original amount and currency for reference
```

#### 6. **OpenAI GPT-4o-mini** (AI Classification)
- **Model**: gpt-4o-mini (cost-effective, fast)
- **Temperature**: 0.2 (deterministic output)
- **Structured Output Schema**:
```json
{
  "category": "Food|Transport|Housing|Utilities|Health|Entertainment|...",
  "confidence": 0.95,
  "normalized_amount": 100,
  "currency": "USD",
  "description": "lunch cafe",
  "source_text": "100 lunch cafe"
}
```

#### 7. **Parse OpenAI Output** (Code Node)
Extracts JSON from nested OpenAI response structure:
```javascript
const output = $json.output?.[0]?.content?.[0]?.text;
return { json: typeof output === 'object' ? output : JSON.parse(output) };
```

#### 8. **Google Sheets - Append Row**
- **Operation**: Append
- **Columns**: timestamp, amount, currency, description, category, source
- **Auto-creates** new rows without overwriting

#### 9. **Telegram Reply** (Confirmation)
Sends immediate feedback:
```
Added: 100 USD — lunch cafe (Food)
```

#### 10. **Google Sheets - Get All Rows**
Reads entire expense history for budget calculations

#### 11. **Budget Check** (Code Node)
Calculates spending totals:
- **Daily** (since midnight)
- **Weekly** (Monday to today)
- **Monthly** (current month)
```javascript
const DAILY_LIMIT = 100;
const WEEKLY_LIMIT = 500;
const MONTHLY_LIMIT = 2000;
// Compares totals and generates alert messages
```

#### 12. **IF Alert** (Conditional Node)
Only triggers if `hasAlerts === true`

#### 13. **Budget Alert** (Telegram Message)
Sends warning with spending breakdown:
```
🚨 Daily limit exceeded! $515.90 / $100
⚠️ Weekly limit exceeded! $515.90 / $500

📈 Current Spending:
• Today: $515.90
• This Week: $515.90
• This Month: $515.90
```

---

## 3. Example Input and Output

### Example 1: Basic USD Expense

**Input (Telegram Message)**
```
100 lunch cafe
```

**Processing Flow**
1. **Parse Message Output**:
```json
{
  "amount": 100,
  "original_currency": "USD",
  "description": "lunch cafe",
  "source_text": "100 lunch cafe",
  "needs_conversion": false
}
```

2. **OpenAI Classification Output**:
```json
{
  "category": "Food",
  "confidence": 0.95,
  "normalized_amount": 100,
  "currency": "USD",
  "description": "lunch cafe",
  "source_text": "100 lunch cafe"
}
```

3. **Google Sheet Row**:
| timestamp | amount | currency | description | category | source |
|-----------|--------|----------|-------------|----------|--------|---------|
| 2026-01-11T09:05:25.528-05:00 | 100 | USD | lunch cafe | Food | telegram | 

4. **Telegram Confirmation**:
```
Added: 100 USD — lunch cafe (Food)
```

---

### Example 2: Multi-Currency with Budget Alert

**Input (Telegram Message)**
```
€250 groceries
```

**Processing Flow**
1. **Parse Message Output**:
```json
{
  "amount": 250,
  "original_currency": "EUR",
  "description": "groceries",
  "source_text": "€250 groceries",
  "needs_conversion": true
}
```

2. **Exchange Rate API Response**:
```json
{
  "base": "EUR",
  "rates": {
    "USD": 1.09,
    "GBP": 0.85,
    ...
  }
}
```

3. **Currency Conversion**:
```json
{
  "amount": 272.5,
  "currency": "USD",
  "original_amount": 250,
  "original_currency": "EUR",
  "exchange_rate": 1.09,
  "description": "groceries"
}
```

4. **OpenAI Classification**:
```json
{
  "category": "Food",
  "confidence": 0.92,
  "normalized_amount": 272.5,
  "currency": "USD",
  "description": "groceries"
}
```

5. **Google Sheet Row**:
| timestamp | amount | currency | description | category | source | 
|-----------|--------|----------|-------------|----------|--------|---------|
| 2026-01-11T09:50:01.511-05:00 | 272.5 | USD | groceries | Food | telegram |

6. **Budget Check Output** (after daily total reaches $515.90):
```json
{
  "dailyTotal": 515.9,
  "weeklyTotal": 515.9,
  "monthlyTotal": 515.9,
  "hasAlerts": true,
  "alertMessage": "🚨 Daily limit exceeded! $515.90 / $100\n⚠️ Weekly limit exceeded! $515.90 / $500"
}
```

7. **Telegram Messages**:
```
Added: 272.5 USD — groceries (Food)

🚨 Daily limit exceeded! $515.90 / $100
⚠️ Weekly limit exceeded! $515.90 / $500

📈 Current Spending:
• Today: $515.90
• This Week: $515.90
• This Month: $515.90
```

---

### Example 3: Alternative Input Format

**Input**
```
taxi home ₸5000
```

**Output (After Processing)**
- **Parsed**: 5000 KZT = ~$10.50 USD (at current rate)
- **Category**: Transport
- **Confirmation**: `Added: 10.5 USD — taxi home (Transport)`

---

## 4. Challenges and AI Assistance

### Challenge 1: Telegram Webhook Not Receiving Messages ⭐ CRITICAL
**Problem**: After setting up ngrok tunnel and n8n, no messages from Telegram reached the workflow. The ngrok logs showed only internal n8n telemetry requests, not Telegram webhook calls.

**Symptoms**:
- n8n workflow showed as "Active"
- ngrok tunnel was running successfully
- Telegram bot responded to `/start` command
- But `getWebhookInfo` showed webhook was registered
- Zero POST requests from Telegram appeared in ngrok logs

**Root Causes Identified by AI**:
1. **Workflow not activated**: Production webhooks only work when workflow is published/active (not just saved)
2. **Wrong webhook URL**: Was using test URL (`/webhook-test/...`) instead of production URL (`/webhook/...`)
3. **ngrok free tier limitation**: Free ngrok shows interstitial warning page that blocks automated bot requests
4. **Secret token**: n8n Telegram Trigger auto-generates a secret token for security

**AI-Assisted Solution**:
GitHub Copilot identified the activation issue:
```
"The requested webhook POST 4553dfb0-f27e-4518-99bf-b727f4a97c96/webhook is not registered."
Hint: "The workflow must be active for a production URL to run successfully."
```

**Steps Taken**:
1. ✅ Activated workflow using toggle in top-right corner of n8n
2. ✅ Deleted webhook: `DELETE /deleteWebhook` 
3. ✅ Let n8n auto-register with correct URL and secret on activation
4. ✅ Verified with `getWebhookInfo` - showed `pending_update_count: 0` (working)

**Verification Command**:
```powershell
Invoke-WebRequest -Uri "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"
```

---

### Challenge 2: Parsing Nested Message Text ⭐
**Problem**: Code error `text.match is not a function` when processing Telegram messages.

**Root Cause**: 
Telegram's webhook payload structure:
```json
{
  "message": {
    "text": "100 lunch",  // ← actual text here
    "chat": {...}
  }
}
```

But code tried: `$json.message` (which is an object, not a string)

**AI Solution**:
Copilot corrected the path:
```javascript
// ❌ Wrong
const text = $json.message || $json.text || '';

// ✅ Correct
const text = $json.message?.text || $json.text || '';
```

---

### Challenge 3: Flexible Input Format Support ⭐
**Problem**: Users might type `100 lunch` OR `lunch 100` - needed to support both orders.

**AI-Provided Dual-Regex Solution**:
```javascript
// Try amount first: "100 lunch"
let m = text.match(/^(\d+[\.,]?\d*)\s+(.*)$/);

// Try description first: "lunch 100"
if (!m) {
  m = text.match(/^(.+?)\s+(\d+[\.,]?\d*)$/);
  if (m) {
    m = [m[0], m[2], m[1]]; // Swap positions
  }
}
```

This elegantly handles both formats without requiring strict user input conventions.

---

### Challenge 4: OpenAI Structured Output Schema Error ⭐
**Problem**: 
```
Invalid schema for response_format 'expense_classification': 
schema must be a JSON Schema of 'type: "object"', got 'type: "None"'.
```

**Root Cause**: 
n8n expects only the inner schema object, not wrapped in `{name, schema}` structure.

**AI Diagnosis**:
Copilot identified that:
1. The wrapper with `name` and `schema` should be split
2. Advanced constraints (`minimum`, `maximum`, `minLength`) aren't supported in structured output
3. The `name` goes in a separate field

**Fix**:
```json
// ❌ Wrong - wrapped structure
{
  "name": "expense_classification",
  "schema": { "type": "object", ... }
}

// ✅ Correct - just the schema
{
  "type": "object",
  "properties": { ... }
}
```

And `expense_classification` goes in the **Schema Name** field.

---

### Challenge 5: Extracting Deeply Nested AI Response ⭐
**Problem**: OpenAI returns deeply nested structure, not flat JSON:
```json
{
  "output": [{
    "content": [{
      "text": {
        "category": "Food",
        "amount": 100,
        ...
      }
    }]
  }]
}
```

**AI-Provided Navigation Code**:
```javascript
const output = $json.output?.[0]?.content?.[0]?.text;

if (!output) {
  // Fallback for other formats
  const out = $json?.data ?? $json?.text ?? $json;
  return { json: typeof out === 'string' ? JSON.parse(out) : out };
}

return { json: typeof output === 'object' ? output : JSON.parse(output) };
```

This handles multiple response formats gracefully with optional chaining and fallbacks.

---

### Challenge 6: Weekly Budget Calculation Not Working ⭐
**Problem**: 
```json
{
  "dailyTotal": 515.9,
  "weeklyTotal": 0,      // ← Should be 515.9
  "monthlyTotal": 515.9
}
```

**Root Cause**: 
Original logic to find "start of week (Monday)":
```javascript
startOfWeek.setDate(today.getDate() - today.getDay() + 1);
```

This fails on Sundays (`getDay() === 0`) → calculates next Monday instead of last Monday!

**AI-Corrected Logic**:
```javascript
const dayOfWeek = today.getDay();
// If Sunday (0), go back 6 days; otherwise go back (dayOfWeek - 1) days
const daysToMonday = dayOfWeek === 0 ? 6 : dayOfWeek - 1;
startOfWeek.setDate(today.getDate() - daysToMonday);
```

**Result**: ✅ Weekly totals now correctly include current week's expenses.

---

### Challenge 7: Multi-Currency Detection
**Problem**: Needed to support currency symbols (€, £, ₸) and codes (EUR, GBP, KZT) in natural text.

**AI-Designed Pattern System**:
```javascript
const currencyPatterns = [
  { symbol: '$', code: 'USD', regex: /\$\s*(\d+[\.,]?\d*)/ },
  { symbol: '€', code: 'EUR', regex: /€\s*(\d+[\.,]?\d*)/ },
  { symbol: '£', code: 'GBP', regex: /£\s*(\d+[\.,]?\d*)/ },
  { symbol: '₸', code: 'KZT', regex: /₸\s*(\d+[\.,]?\d*)/ },
  { symbol: '₽', code: 'RUB', regex: /₽\s*(\d+[\.,]?\d*)/ }
];

for (const pattern of currencyPatterns) {
  const match = text.match(pattern.regex);
  if (match) {
    amount = parseFloat(match[1].replace(',', '.'));
    currency = pattern.code;
    description = text.replace(pattern.regex, '').trim();
    break;
  }
}
```

This supports formats like:
- `€25 lunch`
- `₸5000 taxi`
- `100 EUR meeting`

---

## Key Learnings from AI Assistance

1. **Diagnostic Power**: AI quickly identified "workflow not active" from cryptic n8n error messages
2. **API Understanding**: Copilot knew Telegram's exact payload structure without documentation
3. **Regex Expertise**: Generated complex multi-pattern currency detection in minutes
4. **Edge Case Handling**: Identified Sunday edge case in week calculation that I missed
5. **Production Best Practices**: Suggested optional chaining (`?.`) and fallback patterns
6. **Debugging Strategy**: Recommended verification commands (`getWebhookInfo`, `getUpdates`)

**Total Time Saved**: ~3-4 hours of debugging and research

---

## 5. Technical Setup

### Infrastructure
- **n8n**: Self-hosted via Docker (v2.2.6)
- **Tunneling**: ngrok (for exposing local n8n to Telegram)
- **External Services**: 
  - Telegram Bot API
  - OpenAI API (GPT-4o-mini)
  - Google Sheets API

### Docker Compose Configuration
```yaml
version: '3.1'
services:
  n8n:
    image: n8nio/n8n
    ports:
      - 5678:5678
    environment:
      - WEBHOOK_URL=https://your-ngrok-url.ngrok-free.dev
      - N8N_PROTOCOL=https
    volumes:
      - ~/.n8n:/home/node/.n8n
```

---

## 6. Future Enhancements

Potential improvements for this workflow:
1. **Weekly Summary**: Scheduled workflow to send expense summaries every Sunday
2. **Receipt Image Parsing**: Use OCR to extract expenses from uploaded receipt photos

---

## Author
- **Date**: January 11, 2026
- **Module**: 06 - No-Code Agent Platform (n8n)
- **AI Tools Used**: GitHub Copilot (Claude)
