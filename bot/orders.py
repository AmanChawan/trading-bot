import logging
from bot.client import BinanceFuturesClient

logger = logging.getLogger(__name__)

# Initialize client for futures testnet
client = BinanceFuturesClient()

def print_order_summary(params):
    print("\n--- ORDER REQUEST ---")
    for k, v in params.items():
        print(f"{k}: {v}")
    print("---------------------\n")

def place_order(symbol, side, order_type, quantity, price=None):
    """Place an order using the BinanceFuturesClient."""
    try:
        response = client.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
        logger.info(f"Order placed successfully: {response}")
        return response
    except Exception as e:
        logger.error(f"Error placing order: {e}")
        raise

def print_order_response(response):
    print("\n--- ORDER RESPONSE ---")
    for field in ['orderId', 'symbol', 'side', 'type', 'status', 'executedQty', 'avgPrice']:
        if field in response:
            print(f"{field}: {response[field]}")
    print("----------------------\n")