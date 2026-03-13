import os
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

load_dotenv()  # Load .env file

logger = logging.getLogger(__name__)

class BinanceFuturesClient:
    def __init__(self):
        self.api_key = os.getenv("BINANCE_TESTNET_API_KEY")
        self.api_secret = os.getenv("BINANCE_TESTNET_API_SECRET")
        if not self.api_key or not self.api_secret:
            raise ValueError("API keys not found. Set BINANCE_TESTNET_API_KEY and BINANCE_TESTNET_API_SECRET environment variables.")
        
        # Initialize client for futures testnet
        self.client = Client(self.api_key, self.api_secret, futures_testnet=True)
        logger.info("Binance Futures Testnet client initialized.")

    def place_order(self, symbol, side, order_type, quantity, price=None):
        """
        Place an order on Binance Futures Testnet.
        Returns the order response dictionary.
        """
        try:
            # Convert side and type to uppercase
            side = side.upper()
            order_type = order_type.upper()

            # Prepare parameters
            params = {
                'symbol': symbol,
                'side': side,
                'type': order_type,
                'quantity': quantity,
            }
            if order_type == 'LIMIT':
                if price is None:
                    raise ValueError("Price is required for LIMIT orders.")
                params['price'] = price
                params['timeInForce'] = 'GTC'  # Good till cancelled

            logger.info(f"Placing order: {params}")
            response = self.client.futures_create_order(**params)
            logger.info(f"Order response: {response}")
            return response

        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise