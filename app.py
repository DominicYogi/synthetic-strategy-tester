import streamlit as st
import plotly.graph_objects as go
from market_generator import generate_candles
from strategies.breakout import breakout_strategy

st.set_page_config(page_title="Synthetic Strategy Tester", layout="wide")

st.title("📈 Synthetic Strategy Tester")
st.markdown("Simulate fake markets, test breakout + retest strategy, and visualize results.")

# --- Sidebar Inputs ---
st.sidebar.header("Market Parameters")

price_min = st.sidebar.number_input("Min Price", value=100.0)
price_max = st.sidebar.number_input("Max Price", value=200.0)
volatility = st.sidebar.slider("Volatility Level (1–10)", 1, 10, 3)
num_candles = st.sidebar.number_input("Number of Candles", value=100)
market_mode = st.sidebar.selectbox("Market Behavior", ["trending", "ranging", "wild"])

st.sidebar.header("Strategy Settings")
lookback = st.sidebar.number_input("Breakout Lookback Candles", value=5)
rr_ratio = st.sidebar.number_input("Risk-Reward Ratio", value=2.0)

if st.sidebar.button("Run Strategy"):
    # --- Generate market ---
    candles = generate_candles(price_min, price_max, volatility, num_candles, mode=market_mode)

    # --- Run strategy ---
    results = breakout_strategy(candles, breakout_lookback=lookback, risk_reward=rr_ratio)

    # --- Plot chart ---
    fig = go.Figure()

    for i, candle in enumerate(candles):
        color = "green" if candle["close"] > candle["open"] else "red"
        fig.add_trace(go.Candlestick(
            x=[i], open=[candle["open"]], high=[candle["high"]],
            low=[candle["low"]], close=[candle["close"]],
            increasing_line_color='green', decreasing_line_color='red',
            showlegend=False
        ))

    for idx in results["entries"]:
        fig.add_trace(go.Scatter(x=[idx], y=[candles[idx]["close"]],
                                 mode="markers", marker=dict(color="blue", size=10),
                                 name="Entry"))

    for idx in results["exits"]:
        fig.add_trace(go.Scatter(x=[idx], y=[candles[idx]["close"]],
                                 mode="markers", marker=dict(color="orange", size=10),
                                 name="Exit"))

    st.plotly_chart(fig, use_container_width=True)

    # --- Stats ---
    total_trades = results["win_count"] + results["loss_count"]
    win_rate = (results["win_count"] / total_trades) * 100 if total_trades > 0 else 0

    st.subheader("📊 Strategy Results")
    st.write(f"**Total Trades**: {total_trades}")
    st.write(f"**Wins**: {results['win_count']}")
    st.write(f"**Losses**: {results['loss_count']}")
    st.write(f"**Win Rate**: {win_rate:.2f}%")

    # --- Export option ---
    st.download_button("Download Candle Data", str(candles), file_name="synthetic_candles.txt")
