import streamlit as st
import plotly.graph_objects as go

from market_generator import generate_candles
from strategies.breakout import breakout_retest_strategy

st.set_page_config(page_title="Synthetic Strategy Tester", layout="wide")

st.title("Synthetic Strategy Tester")

# Sidebar inputs
st.sidebar.header("Market Settings")
min_price = st.sidebar.number_input("Min Price", value=90.0)
max_price = st.sidebar.number_input("Max Price", value=110.0)
volatility = st.sidebar.slider("Volatility Level", 1, 10, 3)
num_candles = st.sidebar.slider("Number of Candles", 50, 500, 100)
market_mode = st.sidebar.selectbox("Market Behavior Mode", ["trending", "ranging", "wild"])

st.sidebar.header("Strategy Settings")
strategy_choice = st.sidebar.selectbox("Strategy", ["Breakout + Retest"])
lookback = st.sidebar.slider("Breakout Lookback", 5, 30, 10)
rr_ratio = st.sidebar.slider("Risk:Reward Ratio", 1.0, 3.0, 2.0)

if st.sidebar.button("Run Backtest"):
    # Generate synthetic market
    candles = generate_candles(min_price, max_price, volatility, num_candles, market_mode)

    # Run strategy
    trades = breakout_retest_strategy(candles, breakout_lookback=lookback, risk_reward_ratio=rr_ratio)

    # Display stats
    wins = sum(1 for t in trades if t['result'] == 'win')
    losses = len(trades) - wins
    win_rate = (wins / len(trades) * 100) if trades else 0

    st.subheader("Strategy Stats")
    st.write(f"Total Trades: {len(trades)}")
    st.write(f"Wins: {wins}")
    st.write(f"Losses: {losses}")
    st.write(f"Win Rate: {win_rate:.2f}%")

    # Plot candlesticks
    fig = go.Figure()
    for i, c in enumerate(candles):
        color = 'green' if c['close'] >= c['open'] else 'red'
        fig.add_trace(go.Candlestick(
            x=[i],
            open=[c['open']],
            high=[c['high']],
            low=[c['low']],
            close=[c['close']],
            increasing_line_color='green',
            decreasing_line_color='red',
            showlegend=False
        ))

    # Mark entries
    for trade in trades:
        entry_x = trade['entry_index']
        entry_price = trade['entry_price']
        color = 'blue' if trade['type'] == 'long' else 'orange'
        fig.add_trace(go.Scatter(
            x=[entry_x],
            y=[entry_price],
            mode='markers',
            marker=dict(color=color, size=10),
            name=f"{trade['type'].capitalize()} Entry"
        ))

    st.subheader("Candlestick Chart")
    st.plotly_chart(fig, use_container_width=True)

    # Export data
    if st.button("Download Test Data"):
        import pandas as pd
        df = pd.DataFrame(candles)
        st.download_button("Download Candles CSV", df.to_csv(index=False), file_name="synthetic_candles.csv")
