# Agentic Weather & News (Streamlit + LangChain + MCP)

A small but capable chat-style app that answers weather and news questions. It routes intents with Claude, hits Open-Meteo for live weather/forecast, and pulls news from TheNews API (with a Hacker News fallback if the primary is down or rate-limited). Everything runs in Streamlit with a simple, friendly UI.

## What it does
- Figures out if you asked about weather, news, or both; falls back to keyword heuristics if the LLM is slow/unavailable.
- Weather: Open-Meteo geocoding + current conditions; when you say “tomorrow” (or mention snow), it also fetches rain chance, snowfall, and tomorrow’s highs/lows.
- News: TheNews API first, then Hacker News (fresh, last ~14 days) if the primary fails or is throttled.
- UI: Chat history, unit toggle (°C/°F), optional hide-current toggle, and a quick weather-code legend.

## Quickstart
1) Python 3.12.1
2) Install deps:
```bash
pip install -r requirements.txt
```
3) Environment:
- Required: `ANTHROPIC_API_KEY`
- Optional: `CHAT_MODEL` (default `claude-3-5-sonnet-latest`), `NEWS_API_TOKEN` (default `demo`).
4) Run:
```bash
streamlit run app.py
```
5) Try:
- “What’s the weather in Almaty?”
- “Latest tech news”
- “Will it rain tomorrow in Tokyo?”
- “Snow in Helsinki tomorrow?”

## Project layout
- `app.py` — Streamlit UI and conversation loop
- `agents/orchestrator.py` — intent routing + tool calls (LangChain + Claude)
- `agents/mcp_clients.py` — MCP-style HTTP wrappers for weather and news
- `mcp_config/` — JSON descriptors for the two services
- `requirements.txt` — dependencies
- `video_link.txt` — put your published screencast URL here

## Service notes
- Weather: Open-Meteo, no API key. Uses `current_weather=true`; when “tomorrow” is detected, also requests `precipitation_probability_max`, `temperature_2m_max/min`, and `snowfall_sum`.
- News: TheNews API (demo token by default); Hacker News fallback filtered to ~14 days. Set `NEWS_API_TOKEN` for better quota.
- Location parsing normalizes aliases like Astana/Nur-Sultan; still best to name the city explicitly.

## Known limits
- No persistence; a refresh clears session history.
- Demo news token can hit rate limits; fallback is automatic but may be brief.
- Geocoding is best-effort; ambiguous queries may need a clearer city name.

## Screencast script (short)
1) Open terminal: `streamlit run app.py`.
2) Show the UI: mention the unit toggle, hide-current checkbox, and weather-code legend in the sidebar.
3) Demo weather: “Weather in Almaty” → point out current conditions and code description.
4) Demo tomorrow forecast: “Will it rain tomorrow in Tokyo?” → highlight rain chance, highs/lows, snowfall.
5) Demo snow intent: “Snow in Helsinki tomorrow?” → show snowfall field.
6) Demo news: “Latest tech news” → note primary/fallback handling and freshness window.