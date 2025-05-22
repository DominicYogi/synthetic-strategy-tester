import random

def generate_candles(min_price, max_price, volatility, num_candles):
    candles = []
    last_close = random.uniform(min_price, max_price)

    for _ in range(num_candles):
        # Calculate price movement range based on volatility
        max_move = (max_price - min_price) * (volatility / 50)  # smaller factor to keep moves realistic

        # Open is last close
        open_price = last_close

        # Random move up or down for close price within max_move
        close_price = open_price + random.uniform(-max_move, max_move)

        # Ensure close is within min/max bounds
        close_price = max(min(close_price, max_price), min_price)

        # High is max of open, close plus random wiggle
        high_price = max(open_price, close_price) + random.uniform(0, max_move / 2)
        high_price = min(high_price, max_price)

        # Low is min of open, close minus random wiggle
        low_price = min(open_price, close_price) - random.uniform(0, max_move / 2)
        low_price = max(low_price, min_price)

        candles.append({
            'open': round(open_price, 2),
            'high': round(high_price, 2),
            'low': round(low_price, 2),
            'close': round(close_price, 2)
        })

        last_close = close_price

    return candles
