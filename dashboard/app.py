import sys
import os

# allow imports from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
from datetime import date, timedelta

from optimization.energy_optimizer import find_cheapest_hours
from data.live_weather import get_weather_features

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="AI Electricity Optimizer",
    layout="wide"
)

st.title("⚡ AI Electricity Cost Optimizer")
st.caption("Electricity prices sourced from the Nord Pool wholesale electricity market for Denmark.")

# ------------------------------------------------
# FILE PATHS
# ------------------------------------------------

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DATA_PATH = os.path.join(BASE_DIR, "data", "final_dataset.csv")
LIVE_PRICE_PATH = os.path.join(BASE_DIR, "data", "latest_prices.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "electricity_price_model.pkl")

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------

df = pd.read_csv(DATA_PATH)
df["date"] = pd.to_datetime(df["date"])

model = joblib.load(MODEL_PATH)

# ------------------------------------------------
# LOAD LIVE PRICES FROM CSV
# ------------------------------------------------

live_prices = None
latest_live_price = None

if os.path.exists(LIVE_PRICE_PATH):

    live_prices = pd.read_csv(LIVE_PRICE_PATH)

    if not live_prices.empty:

        if "timestamp" in live_prices.columns:
            live_prices["timestamp"] = pd.to_datetime(live_prices["timestamp"]).dt.tz_localize(None)

        if "price_dkk" in live_prices.columns:
            latest_live_price = live_prices["price_dkk"].iloc[-1]

# ------------------------------------------------
# NAVIGATION
# ------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Market Analysis",
    "Prediction Tool",
    "Optimization"
])

# =========================================================
# OVERVIEW
# =========================================================

with tab1:

    st.header("Electricity Market Overview")

    latest = df.iloc[-1:]

    X_latest = latest.drop(columns=["electricity_price", "date"])

    predicted_mwh = model.predict(X_latest)[0]
    predicted_kwh = predicted_mwh / 1000

    demand = latest["electricity_demand"].values[0]

    col1, col2, col3 = st.columns(3)

    if latest_live_price is not None:

        col1.metric(
            "⚡ Live Electricity Price",
            f"{latest_live_price:.3f} DKK/kWh"
        )

    else:

        col1.metric(
            "⚡ Live Electricity Price",
            "Unavailable"
        )

    col2.metric(
        "📈 Predicted Electricity Price",
        f"{predicted_kwh:.3f} DKK/kWh"
    )

    col3.metric(
        "🔌 Electricity Demand",
        f"{demand:,.0f} MW"
    )

    if isinstance(live_prices, pd.DataFrame):

        if "timestamp" in live_prices.columns and "price_dkk" in live_prices.columns:

            st.subheader("Today's Electricity Prices")

            fig_live = px.line(
                live_prices,
                x="timestamp",
                y="price_dkk",
                labels={
                    "timestamp": "Time",
                    "price_dkk": "Price (DKK/kWh)"
                }
            )

            st.plotly_chart(fig_live, use_container_width=True)

# =========================================================
# MARKET ANALYSIS
# =========================================================

with tab2:

    st.header("Market Analysis")

    st.subheader("Historical Electricity Prices")

    fig_hist = px.line(
        df,
        x="date",
        y="electricity_price",
        labels={
            "date": "Date",
            "electricity_price": "Price (DKK/MWh)"
        }
    )

    st.plotly_chart(fig_hist, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Demand vs Electricity Price")

        fig_demand = px.scatter(
            df,
            x="electricity_demand",
            y="electricity_price",
            opacity=0.6,
            labels={
                "electricity_demand": "Demand (MW)",
                "electricity_price": "Price (DKK/MWh)"
            }
        )

        st.plotly_chart(fig_demand, use_container_width=True)

    with col2:

        st.subheader("Temperature vs Electricity Price")

        fig_temp = px.scatter(
            df,
            x="temperature",
            y="electricity_price",
            opacity=0.6,
            labels={
                "temperature": "Temperature (°C)",
                "electricity_price": "Price (DKK/MWh)"
            }
        )

        st.plotly_chart(fig_temp, use_container_width=True)

# =========================================================
# PREDICTION TOOL
# =========================================================

with tab3:

    st.header("Electricity Price Prediction")

    selected_date = st.date_input(
        "Select prediction date",
        min_value=date.today(),
        max_value=date.today() + timedelta(days=7)
    )

    weather_features = get_weather_features(selected_date)

    if weather_features is not None:

        predicted_mwh = model.predict(weather_features)[0]
        predicted_kwh = predicted_mwh / 1000

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Predicted Price",
            f"{predicted_kwh:.3f} DKK/kWh"
        )

        col2.metric(
            "Temperature",
            f"{weather_features['temperature'].iloc[0]} °C"
        )

        col3.metric(
            "Wind Speed",
            f"{weather_features['wind_speed'].iloc[0]} km/h"
        )

        st.subheader("Model Input Features")

        st.dataframe(weather_features)

    else:

        st.warning("Weather data unavailable for this date.")

# =========================================================
# OPTIMIZATION
# =========================================================

with tab4:

    st.header("Cheapest Electricity Hours")

    if isinstance(live_prices, pd.DataFrame):

        if "timestamp" in live_prices.columns and "price_dkk" in live_prices.columns:

            live_prices["hour"] = pd.to_datetime(live_prices["timestamp"]).dt.hour

            hourly_prices = live_prices.groupby("hour")["price_dkk"].mean().reset_index()

            fig_hourly = px.bar(
                hourly_prices,
                x="hour",
                y="price_dkk",
                labels={
                    "hour": "Hour",
                    "price_dkk": "Price (DKK/kWh)"
                }
            )

            st.plotly_chart(fig_hourly, use_container_width=True)

            cheapest = find_cheapest_hours(hourly_prices)

            cheapest["hour"] = cheapest["hour"].apply(
                lambda x: f"{(x % 12) or 12} {'AM' if x < 12 else 'PM'}"
            )

            st.subheader("Recommended Cheapest Hours")

            st.dataframe(cheapest)

        else:

            st.warning("Live electricity prices unavailable.")

    else:

        st.warning("Live electricity prices unavailable.")