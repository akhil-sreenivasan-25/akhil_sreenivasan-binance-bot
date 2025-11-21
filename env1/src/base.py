from binance import Client

API_KEY = '3Ky0TSOXuYJrg6touX5gAKwoac8106VhQ1FooTAncsla5RoALjEfr9qGGIzUF56k'
API_SECRET = 's6b0mo3gO3IIZKdGjo0pGgbPYTTS84EJRxq7hO0Ah81btVP7MyuiiiqwaziTUN3q'

#connect to binance client
# def get_client():
#     try:
#         client = Client(API_KEY, API_SECRET, testnet=True)
#         if client:
#             print("Connected to Binance Testnet")
#             balance = client.get_asset_balance(asset='USDT')
#             print(balance)
#             return client
#         else:
#             print("Failed to connect to Binance Testnet")
            
#     except Exception as e:
#         print(f"An error occurred: {e}")

# # bot.py
# from binance.client import Client

class BasicBot:
    def __init__(self, api_key=API_KEY, api_secret=API_SECRET, testnet=True):
        self.client = Client(api_key, api_secret, testnet=testnet)
       