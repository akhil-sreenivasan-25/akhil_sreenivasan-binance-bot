from binance import Client
import logging

logger = logging.getLogger(__name__)
def place_stop_limit_order(client, symbol, quantity, side, stop_price, limit_price):
    try:
        if side.upper() == 'BUY':
            order = client.create_order(
                symbol=symbol,
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_STOP_LOSS_LIMIT,
                timeInForce=Client.TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=limit_price,
                stopPrice=stop_price
            )
        elif side.upper() == 'SELL':
            order = client.create_order(
                symbol=symbol,
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_STOP_LOSS_LIMIT,
                timeInForce=Client.TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=limit_price,
                stopPrice=stop_price
            )
        else:
            logger.error(f"Invalid side provided for stop limit order: {side}")
            return "Invalid side. Please use 'BUY' or 'SELL'."
        logger.info(f"Stop limit order placed successfully: {order}")
        return order
    except Exception as e:
        logger.error(f"An error occurred while placing stop limit order: {e}")
        return f"An error occurred while placing stop limit order: {e}"