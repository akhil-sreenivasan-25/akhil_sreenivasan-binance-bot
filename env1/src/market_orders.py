from binance.client import Client
import logging

logger = logging.getLogger(__name__)
def place_market_order(client,symbol,quantity,side):
    try:
        if side.upper() == 'BUY':            
            order = client.create_order(
                symbol=symbol,
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
        elif side.upper() == 'SELL':
            order = client.create_order(
                symbol=symbol,
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
        else:
            logger.error(f"Invalid side provided for Market order: {side}")
            return "Invalid side. Please use 'BUY' or 'SELL'."
        logger.info(f"Market order placed successfully: {order}")
        
        return order
    except Exception as e:
        logger.error(f"An error occurred while placing Market order: {e}")
        return f"An error occurred while placing market order: {e}"