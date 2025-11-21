from base import get_client

client = get_client()
if client:
    print("Placing a market order...")
    balance = client.get_asset_balance()[:3]
    print(balance)
    
else:
    print("Cannot place order: Not connected to Binance Testnet")