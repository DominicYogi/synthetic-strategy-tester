import random

def generate_candles(price_min, price_max, volatility, num_candles, mode='trending'):
    """
    Generates synthetic OHLC candles.

    Args:
        price_min (float): Minimum base price.
        price_max (float): Maximum base price.
        volatility (int): Volatility level (1-10).
        num_candles (int): Number of candles to generate.
        mode (str): Market behavior - 'trending', 'ranging', or 'wild'.

    Returns:
        list of dicts: Each dict has 'open', 'high', 'low', 'close'
    """

    candles = []
    base_price = random.uniform(price_min, price_max)

    direction = 1  # 1 = up, -1 = down
    if mode == 'ranging':
        direction = 0
    elif mode == 'wild':
        direction = None  # Fully random direction

    for _ in range(num_candles):
        if mode == 'wild':
            direction = random.choice([-1, 1])
        elif mode == 'ranging':
            direction *= -1  # Flip direction every time
        # else: keep same direction (trending)

        move = random.uniform(0.1, volatility) * direction
        open_price = base_price
        close_price = base_price + move
        high = max(open_price, close_price) + random.uniform(0, volatility / 2)
        low = min(open_price, close_price) - random.uniform(0, volatility / 2)

        candle = {
            'open': round(open_price, 2),
            'high': round(high, 2),
            'low': round(low, 2),
            'close': round(close_price, 2)
        }

        candles.append(candle)
        base_price = close_price  # Next open = previous close

    return candles
