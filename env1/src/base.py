from binance import Client
import logging

logger = logging.getLogger(__name__)

API_KEY = '3Ky0TSOXuYJrg6touX5gAKwoac8106VhQ1FooTAncsla5RoALjEfr9qGGIzUF56k'
API_SECRET ='s6b0mo3gO3IIZKdGjo0pGgbPYTTS84EJRxq7hO0Ah81btVP7MyuiiiqwaziTUN3q'

#connect to binance client
class BasicBot:
    def __init__(self, api_key=API_KEY, api_secret=API_SECRET, testnet=True):
        self.client = Client(api_key, api_secret, testnet=testnet)
       