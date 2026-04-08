import streamlit as st
import pandas as pd
import joblib
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Energy Market Intelligence", layout="wide")

st.title("⚡ Energy Market Intelligence Dashboard")

st.markdown(
"""
Machine Learning + Data Engineering pipeline for predicting **energy demand,
electricity prices, and market insights for energy companies**.
"""
)

# -------------------------
# LOAD DATA
# -------------------------

df = pd.read_csv("data/final_dataset.csv")

demand_model = joblib.load("models/demand_model/demand_model.pkl")
price_model = joblib.load("models/price_model/price_model.pkl")

avg_demand = df["electricity_demand"].mean()
avg_price = df["electricity_price"].mean()

# -------------------------
# WEATHER INPUT
# -------------------------

st.header("Weather Conditions")

col1, col2, col3 = st.columns(3)

temperature = col1.slider("Temperature (°C)", -10, 35, 10)
wind_speed = col2.slider("Wind Speed (m/s)", 0, 20, 5)
month = col3.slider("Month", 1, 12, 6)

day_of_week = 2
day_of_year = 180

# -------------------------
# MODEL FORECAST
# -------------------------

st.header("Energy Forecast")

if st.button("Run Forecast"):

    demand_features = [[
        temperature,
        wind_speed,
        day_of_week,
        month,
        day_of_year
    ]]

    predicted_demand = demand_model.predict(demand_features)[0]

    price_features = [[
        temperature,
        wind_speed,
        day_of_week,
        month,
        day_of_year,
        predicted_demand
    ]]

    predicted_price = price_model.predict(price_features)[0]

    # -------------------------
    # BLOOMBERG STYLE METRICS
    # -------------------------

    st.subheader("Market Indicators")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Predicted Demand (MWh)",
        round(predicted_demand,2),
        round(predicted_demand-avg_demand,2)
    )

    c2.metric(
        "Predicted Price (€)",
        round(predicted_price,2),
        round(predicted_price-avg_price,2)
    )

    if predicted_price > avg_price:
        signal = "Bullish Energy Market"
        color = "green"
    else:
        signal = "Weak Energy Market"
        color = "red"

    c3.metric("Market Signal", signal)

    # -------------------------
    # MARKET INSIGHT TEXT
    # -------------------------

    st.subheader("Market Insight")

    if predicted_price > avg_price:
        st.success(
            "Electricity prices predicted ABOVE average. Renewable energy companies may benefit."
        )
    else:
        st.warning(
            "Electricity prices predicted BELOW average. Energy market conditions may weaken."
        )

# -------------------------
# DATA ANALYSIS
# -------------------------

st.header("Energy Data Analysis")

col1, col2 = st.columns(2)

fig1 = px.scatter(
    df,
    x="temperature",
    y="electricity_demand",
    title="Temperature vs Electricity Demand"
)

fig2 = px.scatter(
    df,
    x="electricity_demand",
    y="electricity_price",
    title="Demand vs Electricity Price"
)

col1.plotly_chart(fig1, use_container_width=True)
col2.plotly_chart(fig2, use_container_width=True)

# -------------------------
# CORRELATION HEATMAP
# -------------------------

st.subheader("Feature Correlation")

corr = df.corr(numeric_only=True)

fig3 = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="Blues",
    title="Correlation Heatmap"
)

st.plotly_chart(fig3, use_container_width=True)

# -------------------------
# ENERGY STOCK MARKET
# -------------------------

st.header("Energy Company Market Comparison")

stocks = {
    "Ørsted (Denmark)": "ORSTED.CO",
    "Vestas Wind Systems": "VWS.CO",
    "Siemens Energy": "ENR.DE",
    "Iberdrola": "IBE.MC",
    "Equinor": "EQNR",
    "TotalEnergies": "TTE",
    "Shell": "SHEL",
    "BP": "BP"
}

companies = st.multiselect(
    "Compare Energy Companies",
    list(stocks.keys()),
    default=["Ørsted (Denmark)", "Vestas Wind Systems"]
)

fig = go.Figure()

for company in companies:

    ticker = yf.Ticker(stocks[company])
    data = ticker.history(period="6mo")

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name=company
        )
    )

fig.update_layout(
    title="Energy Company Stock Performance (6 Months)",
    xaxis_title="Date",
    yaxis_title="Stock Price"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# DATASET PREVIEW
# -------------------------

st.header("Dataset Preview")

st.dataframe(df.head())

# -------------------------
# FOOTER
# -------------------------

st.markdown("---")

st.markdown(
"""
**Project Pipeline**

Weather Data → Demand Prediction Model → Price Prediction Model → Energy Market Insight

Built using **Python, Streamlit, Scikit-Learn, Plotly, and Financial APIs**
"""
)