import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
from datetime import date, timedelta

from optimization.energy_optimizer import find_cheapest_hours
from data.live_weather import get_weather_features
from database.db_manager import load_market_data, load_latest_prices

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
# LOAD DATA FROM DATABASE
# ------------------------------------------------

df = load_market_data()

df["date"] = pd.to_datetime(df["date"])

live_prices = load_latest_prices()

latest_live_price = None

if not live_prices.empty:
    latest_live_price = live_prices["price_dkk"].iloc[-1]

# ------------------------------------------------
# LOAD LIVE PRICES
# ------------------------------------------------

live_prices = None
latest_live_price_kwh = None

if os.path.exists(LIVE_PRICE_PATH):

    try:

        live_prices = pd.read_csv(LIVE_PRICE_PATH)

        if not live_prices.empty:

            live_prices["timestamp"] = pd.to_datetime(live_prices["timestamp"], errors="coerce")

            # convert MWh → kWh
            live_prices["price_kwh"] = live_prices["price_dkk"] / 1000

            latest_live_price_kwh = live_prices["price_kwh"].iloc[-1]

    except Exception:
        live_prices = None


# fallback if live data missing
if latest_live_price_kwh is None:
    latest_live_price_kwh = df["electricity_price"].iloc[-1] / 1000


# ------------------------------------------------
# MARKET SCALING ADJUSTMENT
# ------------------------------------------------

# Historical dataset is 2020, modern prices are higher
# We scale predictions relative to current market

historical_avg = df["electricity_price"].mean()
live_mwh_price = latest_live_price_kwh * 1000

market_scale_factor = live_mwh_price / historical_avg


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

    today = date.today()

    weather_today = get_weather_features(today)

    if weather_today is not None:

        weather_today["day_of_week"] = today.weekday()
        weather_today["month"] = today.month
        weather_today["day_of_year"] = today.timetuple().tm_yday

        # approximate demand
        weather_today["electricity_demand"] = 4000

        predicted_mwh = model.predict(weather_today)[0]

    else:

        predicted_mwh = df["electricity_price"].iloc[-1]

    # apply market scaling
    predicted_mwh = predicted_mwh * market_scale_factor

    predicted_kwh = predicted_mwh / 1000

    demand = 4000

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "⚡ Live Electricity Price",
        f"{latest_live_price_kwh:.3f} DKK/kWh"
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

        st.subheader("Today's Electricity Prices")

        fig_live = px.line(
            live_prices,
            x="timestamp",
            y="price_kwh",
            labels={
                "timestamp": "Time",
                "price_kwh": "Price (DKK/kWh)"
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

        weather_features["day_of_week"] = selected_date.weekday()
        weather_features["month"] = selected_date.month
        weather_features["day_of_year"] = selected_date.timetuple().tm_yday

        weather_features["electricity_demand"] = 4000

        predicted_mwh = model.predict(weather_features)[0]

        # scale to modern market
        predicted_mwh = predicted_mwh * market_scale_factor

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

        live_prices["hour"] = pd.to_datetime(live_prices["timestamp"]).dt.hour

        hourly_prices = live_prices.groupby("hour")["price_kwh"].mean().reset_index()

        fig_hourly = px.bar(
            hourly_prices,
            x="hour",
            y="price_kwh",
            labels={
                "hour": "Hour",
                "price_kwh": "Price (DKK/kWh)"
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
