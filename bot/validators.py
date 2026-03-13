import re

def validate_symbol(symbol: str) -> bool:
    # Simple check: alphanumeric and typically ends with USDT
    return bool(re.match(r'^[A-Z0-9]+USDT$', symbol))

def validate_side(side: str) -> bool:
    return side.upper() in ['BUY', 'SELL']

def validate_order_type(order_type: str) -> bool:
    return order_type.upper() in ['MARKET', 'LIMIT']

def validate_quantity(qty: str) -> bool:
    try:
        q = float(qty)
        return q > 0
    except ValueError:
        return False

def validate_price(price: str) -> bool:
    try:
        p = float(price)
        return p > 0
    except ValueError:
        return False