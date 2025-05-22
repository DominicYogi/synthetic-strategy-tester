def breakout_retest_strategy(candles, breakout_lookback=10, risk_reward_ratio=2):
    """
    Simple breakout + retest strategy.
    
    Parameters:
        candles (List[dict]): List of OHLC candles.
        breakout_lookback (int): Number of candles to look back for highs/lows.
        risk_reward_ratio (float): Ratio for setting TP based on SL.
    
    Returns:
        List[dict]: List of trades with entry/exit details.
    """
    trades = []
    i = breakout_lookback

    while i < len(candles) - 1:
        window = candles[i - breakout_lookback:i]
        current = candles[i]

        # Get highest high in lookback window
        recent_high = max(c['high'] for c in window)
        recent_low = min(c['low'] for c in window)

        # Long Breakout Setup
        if current['close'] > recent_high:
            breakout_level = recent_high
            entry_candle = candles[i + 1]  # Next candle
            entry_price = breakout_level

            # Wait for retest
            for j in range(i + 1, len(candles)):
                retest_candle = candles[j]
                if retest_candle['low'] <= breakout_level:
                    sl = breakout_level - 1  # Static 1 unit below
                    tp = entry_price + (entry_price - sl) * risk_reward_ratio
                    result = 'win' if retest_candle['high'] >= tp else 'loss'

                    trades.append({
                        'type': 'long',
                        'entry_index': j,
                        'entry_price': entry_price,
                        'stop_loss': sl,
                        'take_profit': tp,
                        'result': result
                    })
                    i = j + 1
                    break
            else:
                i += 1

        # Short Breakout Setup
        elif current['close'] < recent_low:
            breakout_level = recent_low
            entry_candle = candles[i + 1]
            entry_price = breakout_level

            for j in range(i + 1, len(candles)):
                retest_candle = candles[j]
                if retest_candle['high'] >= breakout_level:
                    sl = breakout_level + 1
                    tp = entry_price - (sl - entry_price) * risk_reward_ratio
                    result = 'win' if retest_candle['low'] <= tp else 'loss'

                    trades.append({
                        'type': 'short',
                        'entry_index': j,
                        'entry_price': entry_price,
                        'stop_loss': sl,
                        'take_profit': tp,
                        'result': result
                    })
                    i = j + 1
                    break
            else:
                i += 1
        else:
            i += 1

    return trades
