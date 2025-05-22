def breakout_strategy(candles, breakout_lookback=5, risk_reward=2):
    """
    Simulates a breakout + retest strategy.

    Args:
        candles (list): List of OHLC candle dicts.
        breakout_lookback (int): Number of candles to look back for highs.
        risk_reward (float): RR ratio to target profit.

    Returns:
        dict: {
            'entries': [index of entries],
            'exits': [index of exits],
            'win_count': int,
            'loss_count': int,
            'trades': list of {entry_idx, exit_idx, result}
        }
    """

    entries = []
    exits = []
    trades = []
    win_count = 0
    loss_count = 0

    in_trade = False
    entry_price = None
    stop_loss = None
    target = None
    entry_idx = None

    for i in range(breakout_lookback, len(candles)):
        candle = candles[i]
        recent_highs = [c['high'] for c in candles[i - breakout_lookback:i]]
        max_recent_high = max(recent_highs)

        # 1. Entry condition
        if not in_trade and candle['close'] > max_recent_high:
            # Wait for retest
            retest_level = max_recent_high
            for j in range(i+1, min(i+6, len(candles))):
                retest_candle = candles[j]
                if retest_candle['low'] <= retest_level:
                    # Enter trade on retest
                    entry_price = retest_candle['close']
                    stop_loss = entry_price - (entry_price - retest_level)
                    target = entry_price + (entry_price - stop_loss) * risk_reward
                    entry_idx = j
                    in_trade = True
                    break

        # 2. Exit condition
        if in_trade:
            if candle['high'] >= target:
                # Take profit hit
                win_count += 1
                exits.append(i)
                entries.append(entry_idx)
                trades.append({'entry_idx': entry_idx, 'exit_idx': i, 'result': 'win'})
                in_trade = False
            elif candle['low'] <= stop_loss:
                # Stop loss hit
                loss_count += 1
                exits.append(i)
                entries.append(entry_idx)
                trades.append({'entry_idx': entry_idx, 'exit_idx': i, 'result': 'loss'})
                in_trade = False

    return {
        'entries': entries,
        'exits': exits,
        'win_count': win_count,
        'loss_count': loss_count,
        'trades': trades
    }
