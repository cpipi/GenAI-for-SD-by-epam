# Sample Test Cases for Upload File Button

Use these JSON files to test the **Upload File** feature in the Streamlit app.

## Available Test Cases

### Low-Risk Scenarios
- **normal_low_transfer.json** - Standard domestic transfer, low amount, established customer
- **mobile_payment.json** - Mobile app payment, small amount, multiple historical transactions
- **atm_withdrawal.json** - ATM withdrawal, typical amount, regular pattern

### High-Risk Scenarios
- **large_amount_block.json** - Transfer >= $50k (triggers hard gate block)
- **sanctioned_entity.json** - Customer name matching sanctions list (vladimir putin)
- **risky_country_international.json** - Wire transfer to high-risk jurisdiction (RU/IR)
- **dormant_account_spike.json** - Newly activated account with large transaction
- **structured_transactions.json** - Multiple round-amount transfers (structuring pattern)

### Edge Cases & Adversarial
- **missing_profile.json** - Transaction with minimal customer profile
- **negative_amount.json** - Invalid negative transaction amount
- **unknown_channel.json** - Unrecognized transaction channel

## How to Use

1. In the Streamlit app, select **"Upload File"** mode from sidebar
2. Click **"Choose a JSON file"** and select any file from this directory
3. Click **"Process File"**
4. Review the decision in the main panel

## File Structure

Each JSON file contains:
```json
{
  "case_id": "string",
  "customer_id": "string or name",
  "transaction_amount": number,
  "transaction_type": "transfer|payment|withdrawal|deposit",
  "channel": "online|mobile_app|atm|branch|wire_transfer|international",
  "device_location": "country code (US, RU, IR, KP, etc.)",
  "customer_profile": {
    "account_age_days": number,
    "avg_monthly_volume": number,
    "previous_txn_count": number,
    "country_of_residence": "country code"
  }
}
```

## Expected Outcomes

- **Low-Risk Cases**: Should be APPROVED with low risk scores
- **High-Risk Cases**: Should be BLOCKED or MANUAL_REVIEW
- **Sanctioned Entity Cases**: Should be BLOCKED due to sanctions gate
- **Large Amount Cases**: Should be BLOCKED due to amount gate (>= $50k)
- **Edge Cases**: Should handle gracefully or validate inputs
