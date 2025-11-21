from base import BasicBot

# bot = BasicBot(api_key='3Ky0TSOXuYJrg6touX5gAKwoac8106VhQ1FooTAncsla5RoALjEfr9qGGIzUF56k',
#                api_secret='s6b0mo3gO3IIZKdGjo0pGgbPYTTS84EJRxq7hO0Ah81btVP7MyuiiiqwaziTUN3q')
bot=BasicBot()
try:
    if bot.client:
        print("Binance Testnet connection successful.")
        balance = bot.client.get_asset_balance('BTC')
        print(balance)
except Exception as e:
    print(f"An error occurred: {e}")