from binance.client import Client

def place_limit_order(client,symbol,quantity,side,price):
    try:
        if side.upper() == 'BUY':
            order = client.create_order(
                symbol=symbol,
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_LIMIT,
                timeInForce=Client.TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=price
            )
        elif side.upper() == 'SELL':
            order = client.create_order(
                symbol=symbol,
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_LIMIT,
                timeInForce=Client.TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=price
            )
        else:
            return "Invalid side. Please use 'BUY' or 'SELL'."
        
        return order
    except Exception as e:
        return f"An error occurred while placing market order: {e}"