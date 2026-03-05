import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go


st.set_page_config(page_title="Stock Market Dashboard", page_icon="📈", layout="wide")


st.markdown("<h1 style='text-align:center; color:#00ADB5;'>📊 Real-Time Stock Market Dashboard</h1>", unsafe_allow_html=True)


st.sidebar.header("Select Company")

stocks = {
    "TCS": "TCS.NS",
    "Amazon": "AMZN",
    "Google": "GOOGL",
    "IBM": "IBM",
    "Infosys": "INFY.NS",
    "Tech Mahindra": "TECHM.NS",
    "Wipro": "WIPRO.NS",
    "Accenture": "ACN",
    "Microsoft": "MSFT",
    "Reliance": "RELIANCE.NS"
}

company = st.sidebar.selectbox("Company", list(stocks.keys()))
ticker = stocks[company]

stock = yf.Ticker(ticker)
data = stock.history(period="3mo")


data["MA20"] = data["Close"].rolling(window=20).mean()


st.subheader(f"{company} Stock Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Current Price", round(data["Close"].iloc[-1],2))
col2.metric("Highest Price", round(data["High"].max(),2))
col3.metric("Lowest Price", round(data["Low"].min(),2))


st.subheader("Stock Data Table")
st.dataframe(data)

fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=data.index,
    open=data["Open"],
    high=data["High"],
    low=data["Low"],
    close=data["Close"],
    name="Price"
))

fig.add_trace(go.Scatter(
    x=data.index,
    y=data["MA20"],
    line=dict(color="cyan", width=2),
    name="Moving Average"
))

fig.update_layout(
    title=f"{company} Stock Price Chart",
    template="plotly_dark",
    height=500
)

st.plotly_chart(fig, use_container_width=True)


st.subheader("Trading Volume")

volume_fig = go.Figure()

volume_fig.add_trace(go.Bar(
    x=data.index,
    y=data["Volume"],
    marker_color="orange"
))

volume_fig.update_layout(
    title="Daily Trading Volume",
    height=400
)

st.plotly_chart(volume_fig, use_container_width=True)


st.subheader("Download Stock Data")

csv = data.to_csv().encode('utf-8')

st.download_button(
    label="Download CSV",
    data=csv,
    file_name=f"{company}_stock_data.csv",
    mime='text/csv'
)