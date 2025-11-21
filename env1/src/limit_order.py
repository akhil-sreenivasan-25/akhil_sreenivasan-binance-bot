from binance.client import Client
import logging

logger = logging.getLogger(__name__)
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
            logger.error(f"Invalid side provided for limit order: {side}")
            return "Invalid side. Please use 'BUY' or 'SELL'."
        logger.info(f"Limit order placed successfully: {order}")
        return order
    except Exception as e:
        logger.error(f"An error occurred while placing limit order: {e}")
        return f"An error occurred while placing market order: {e}"