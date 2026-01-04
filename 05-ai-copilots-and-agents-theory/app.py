import os
from typing import Any, Dict

import streamlit as st
from dotenv import load_dotenv

from agents.orchestrator import AgentOrchestrator, OrchestratorConfig


def describe_weather_code(code: Any) -> str:
    try:
        c = int(code)
    except Exception:
        return ""
    if c == 0:
        return "Clear sky"
    if c in {1, 2, 3}:
        return "Mainly clear/partly cloudy/overcast"
    if c in {45, 48}:
        return "Fog"
    if 51 <= c <= 57:
        return "Drizzle"
    if 61 <= c <= 67:
        return "Rain"
    if 71 <= c <= 77:
        return "Snow"
    if 80 <= c <= 82:
        return "Rain showers"
    if 85 <= c <= 86:
        return "Snow showers"
    if 95 <= c <= 99:
        return "Thunderstorms"
    return ""

# Load environment variables early for Anthropic and optional news token.
load_dotenv()

st.set_page_config(page_title="Agentic Weather & News", page_icon="☁️")

if "orchestrator" not in st.session_state:
    config = OrchestratorConfig(
        model=os.getenv("CHAT_MODEL", "claude-3-5-sonnet-latest"),
        temperature=0.0,
        news_limit=5,
    )
    st.session_state.orchestrator = AgentOrchestrator(config)
    st.session_state.history = []

orchestrator: AgentOrchestrator = st.session_state.orchestrator

unit_choice = st.sidebar.radio("Temperature units", ["C", "F"], index=0)
show_current = st.sidebar.checkbox("Show current conditions", value=True)
st.sidebar.markdown("---")
with st.sidebar.expander("Weather code legend"):
    st.write(
        {
            "0": "Clear sky",
            "1-3": "Mainly clear/partly cloudy/overcast",
            "45/48": "Fog",
            "51-57": "Drizzle",
            "61-67": "Rain",
            "71-77": "Snow",
            "80-82": "Rain showers",
            "85-86": "Snow showers",
            "95-99": "Thunderstorms",
        }
    )

st.title("Agentic Weather & News")
st.caption("Multi-agent Streamlit app using MCP-style tools for Open-Meteo and news.")

with st.form("user-input"):
    user_query = st.text_input("Ask a question", placeholder="What's the weather in Almaty? Any tech news today?")
    submitted = st.form_submit_button("Send")

if submitted and user_query.strip():
    st.session_state.history.append({"role": "user", "content": user_query})
    with st.spinner("Thinking..."):
        result: Dict[str, Any] = orchestrator.handle_query(user_query)
    st.session_state.history.append({"role": "assistant", "content": result})

for message in st.session_state.history:
    role = message["role"]
    content = message["content"]
    with st.chat_message(role):
        if role == "user":
            st.write(content)
        else:
            intents = content.get("intents", [])
            st.write(f"Intents: {', '.join(intents)}")

            weather = content.get("weather")
            if weather:
                st.subheader("Weather")
                if weather.get("error"):
                    st.error(weather["error"])
                else:
                    temp_c = weather.get("temperature_c")
                    wind_kph = weather.get("windspeed_kph")
                    code_desc = describe_weather_code(weather.get("weathercode"))
                    temp = temp_c if unit_choice == "C" else (temp_c * 9 / 5 + 32 if temp_c is not None else None)
                    wind = wind_kph if unit_choice == "C" else (wind_kph * 0.621371 if wind_kph is not None else None)
                    if show_current:
                        st.write(
                            {
                                "location": weather.get("location"),
                                f"temperature_{unit_choice.lower()}": temp,
                                f"windspeed_{'kph' if unit_choice == 'C' else 'mph'}": wind,
                                "provider": weather.get("provider"),
                                "observed_at": weather.get("timestamp"),
                                "condition": code_desc,
                            }
                        )
                    rain_chance = weather.get("rain_chance_tomorrow_pct")
                    snow_cm = weather.get("snowfall_tomorrow_cm")
                    tmax = weather.get("temp_max_tomorrow_c")
                    tmin = weather.get("temp_min_tomorrow_c")
                    if weather.get("tomorrow_requested") or weather.get("snow_requested"):
                        st.subheader("Tomorrow (forecast)")
                        if tmax is not None or tmin is not None:
                            tmax_out = tmax if unit_choice == "C" else (tmax * 9 / 5 + 32 if tmax is not None else None)
                            tmin_out = tmin if unit_choice == "C" else (tmin * 9 / 5 + 32 if tmin is not None else None)
                            st.write({f"temp_max_{unit_choice.lower()}": tmax_out, f"temp_min_{unit_choice.lower()}": tmin_out})
                        if rain_chance is not None:
                            st.info(f"Chance of rain tomorrow: {rain_chance}%")
                        if snow_cm is not None:
                            st.info(f"Snowfall tomorrow (cm): {snow_cm}")
                        if (
                            rain_chance is None
                            and snow_cm is None
                            and tmax is None
                            and tmin is None
                        ):
                            st.warning("Forecast details not available; showing current conditions only.")

            news = content.get("news")
            if news:
                st.subheader("News")
                if news.get("error"):
                    st.error(news["error"])
                else:
                    if warning := news.get("warning"):
                        st.warning(warning)
                    articles = news.get("articles", [])
                    for idx, article in enumerate(articles, start=1):
                        st.markdown(f"**{idx}. {article.get('title')}**")
                        if article.get("summary"):
                            st.write(article["summary"])
                        st.write(f"Source: {article.get('source')} | Published: {article.get('published_at')}")
                        if article.get("url"):
                            st.markdown(f"[Open link]({article['url']})")
                        st.divider()

            if content.get("message"):
                st.info(content["message"])

st.sidebar.header("Status")
st.sidebar.write(
    {
        "LLM": os.getenv("CHAT_MODEL", "claude-3-5-sonnet-latest"),
        "News provider": "TheNews API (fallback: Hacker News)",
        "Weather provider": "Open-Meteo",
    }
)

st.sidebar.markdown("---")
st.sidebar.write("Environment variables are loaded from .env. Keep your keys safe.")
