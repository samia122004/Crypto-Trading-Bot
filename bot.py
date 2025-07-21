# bot.py

from binance.client import Client
from binance.enums import *
from dotenv import load_dotenv
import os
import logging

# Load API keys from .env
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Logging setup
logging.basicConfig(
    filename='spot_trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SpotTradingBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret)

        if testnet:
            self.client.API_URL = 'https://testnet.binance.vision/api'

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            if order_type == 'MARKET':
                order = self.client.create_order(
                    symbol=symbol,
                    side=SIDE_BUY if side == 'BUY' else SIDE_SELL,
                    type=ORDER_TYPE_MARKET,
                    quantity=quantity
                )
            elif order_type == 'LIMIT':
                order = self.client.create_order(
                    symbol=symbol,
                    side=SIDE_BUY if side == 'BUY' else SIDE_SELL,
                    type=ORDER_TYPE_LIMIT,
                    quantity=quantity,
                    price=price,
                    timeInForce=TIME_IN_FORCE_GTC
                )
            else:
                raise ValueError("Unsupported order type")

            logging.info(f"✅ Order placed: {order}")
            return order

        except Exception as e:
            logging.error(f"❌ Error placing order: {e}")
            return {"error": str(e)}
