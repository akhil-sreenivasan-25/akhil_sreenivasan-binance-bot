from binance import Client
import logging

logger = logging.getLogger(__name__)

def place_oco_order(client, symbol, quantity, side, price, stop_price, stop_limit_price):
    try:
        if side.upper() == 'BUY':
            order = client.create_oco_order(
                symbol=symbol,
                side=Client.SIDE_BUY,
                quantity=quantity,
                price=price,                #limit order price
                stopPrice=stop_price,       #triggering price of stop limit order                                                    
                stopLimitPrice=stop_limit_price,  #actual limit price of stop limit order
                stopLimitTimeInForce=Client.TIME_IN_FORCE_GTC
            )
        elif side.upper() == 'SELL':
            order = client.create_oco_order(
                symbol=symbol,
                side=Client.SIDE_SELL,
                quantity=quantity,
                price=price,
                stopPrice=stop_price,
                stopLimitPrice=stop_limit_price,
                stopLimitTimeInForce=Client.TIME_IN_FORCE_GTC
            )
        else:
            logger.error(f"Invalid side provided for OCO order: {side}")
            return "Invalid side. Please use 'BUY' or 'SELL'."
        logger.info(f"OCO order placed successfully: {order}")
        return order
    except Exception as e:
        logger.error(f"An error occurred while placing OCO order: {e}")
        return f"An error occurred while placing OCO order: {e}"