from base import BasicBot
from market_orders import place_market_order
from limit_order import place_limit_order
from advanced.oco import place_oco_order
from advanced.stop_limit_order import place_stop_limit_order
from bot_log import setup_logging

logger = setup_logging()

# bot = BasicBot(api_key='3Ky0TSOXuYJrg6touX5gAKwoac8106VhQ1FooTAncsla5RoALjEfr9qGGIzUF56k',
#                api_secret='s6b0mo3gO3IIZKdGjo0pGgbPYTTS84EJRxq7hO0Ah81btVP7MyuiiiqwaziTUN3q')

try:
    logger.info("Starting Trading Bot")
    bot=BasicBot()
    if bot.client:
        logger.info("Binance Testnet connection successful.")
except Exception as e:
    logger.error(f"An error occurred while connecting: {e}")
    print(f"An error occurred: {e}")
choice = None
symbols = [s['symbol'] for s in bot.client.get_exchange_info()['symbols']]
logger.debug(f"Available symbols loaded : {len(symbols)} symblos")

while choice != '8':
    print("1. place market order \n2. place limit order \n3. stop limit order \n4. OCO order 8.exit")
    choice = input("Enter your choice: ")
    # Market Order
    if choice == '1':
        try:
            pair= str(input("Enter trading pair (e.g., BTCUSDT): ")).upper()
            if pair not in symbols:
                logger.warning(f"Invalid trading pair entered: {pair}") 
                print("Invalid trading pair! Please enter a valid Binance symbol."+str(pair))
            else:
                current_price= bot.client.get_symbol_ticker(symbol=pair)['price']
                logger.info(f"Placing market order for {pair} current price at {current_price}")
                print(f"Current price of {pair} is {current_price}")
                quantity= float(input("Enter quantity to buy/sell: "))
                side= str(input("Enter side (BUY/SELL): ")).upper()
                order=place_market_order(bot.client, pair, quantity, side)
                # logger.info(f"Market order placed: {order}")
                print("Order details: " + " orderId :"+str( order['orderId']) +" Pair :"+ str(order['symbol']) +" status :"+ str(order['status']) +" price :"+ str(order['fills'][0]['price']))
        except Exception as e:
            logger.error(f"An error occurred while placing market order: {e}")
            print(f"An error occurred: {e}")
    # Limit Order
    elif choice == '2':
        try:
            pair= str(input("Enter trading pair (e.g., BTCUSDT): ")).upper()
            if pair not in symbols:
                logger.warning(f"Invalid trading pair entered: {pair}")
                print("Invalid trading pair! Please enter a valid Binance symbol."+str(pair))
            else:
                current_price= bot.client.get_symbol_ticker(symbol=pair)['price']
                logger.info(f"Placing limit order for {pair} current price at {current_price}")
                print(f"Current price of {pair} is {current_price}")
                quantity= float(input("Enter quantity to buy/sell: "))
                side= str(input("Enter side (BUY/SELL): ")).upper()
                price= float(input("Enter limit price: "))  
                while True:
                    if side=='BUY' and price>=float(current_price):
                        logger.warning("For BUY limit orders, limit price must be less than current price.")
                        print("For BUY limit orders, limit price must be less than current price. Please re-enter.")
                        price= float(input("Enter limit price: "))
                    elif side=='SELL' and price<=float(current_price):
                        logger.warning("For SELL limit orders, limit price must be greater than current price.")
                        print("For SELL limit orders, limit price must be greater than current price. Please re-enter.")
                        price= float(input("Enter limit price: "))
                    else:
                        break
                order=place_limit_order(bot.client, pair, quantity, side, price)
                print("Order response: " + " orderId :"+str( order['orderId']) +" Pair :"+ str(order['symbol']) +" status :"+ str(order['status']) +" price :"+ str(order['price']))
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            print(f"An error occurred: {e}")
    # stop Limit Order
    elif choice == '3':
        try:
            pair= str(input("Enter trading pair (e.g., BTCUSDT): ")).upper()
            if pair not in symbols:
                logger.warning(f"Invalid trading pair entered: {pair}")
                print("Invalid trading pair! Please enter a valid Binance symbol."+str(pair))
            else:
                current_price= float(bot.client.get_symbol_ticker(symbol=pair)['price'])
                logger.info(f"Placing stop limit order for {pair} current price at {current_price}")
                print(f"Current price of {pair} is {current_price}")
                quantity= float(input("Enter quantity to buy/sell: "))
                side= str(input("Enter side (BUY/SELL): ")).upper()
                limit_price= 0
                stop_price=0
                if side=='BUY':
                    while True:
                        stop_price= float(input("Enter stop price: "))
                        limit_price= float(input("Enter limit price: "))
                        if current_price > stop_price or stop_price>limit_price:
                            print("For BUY limit orders, stop price must be less than limit price and current price must be less than both other prices. Please re-enter.")
                        else:
                            break
                elif side=='SELL':
                    while True:
                        stop_price= float(input("Enter stop price: "))
                        limit_price= float(input("Enter limit price: "))
                        if current_price < stop_price or stop_price<limit_price:
                            print("For SELL limit orders, stop price must be greater than limit price and current price must be greter than both other prices. Please re-enter.")
                        else:
                            break
                order=place_stop_limit_order(bot.client, pair, quantity, side, stop_price, limit_price)    
                print("Order response: " + " orderId :"+str( order['orderId']) +" Pair :"+ str(order['symbol']) + "")
        except Exception as e:
            logger.error(f"An error occurred : {e}")
            print(f"An error occurred: {e}")
    # OCO Order
    elif choice == '4':
        try:
            pair= str(input("Enter trading pair (e.g., BTCUSDT): ")).upper()
            if pair not in symbols:
                logger.warning(f"Invalid trading pair entered: {pair}")
                print("Invalid trading pair! Please enter a valid Binance symbol."+str(pair))
            else:
                current_price=float(bot.client.get_symbol_ticker(symbol=pair)['price'])
                logger.info(f"Placing OCO order for {pair} current price at {current_price}")
                print(f"Current price of {pair} is {current_price}")
                quantity= float(input("Enter quantity to buy/sell: "))
                side= str(input("Enter side (BUY/SELL): ")).upper()
                price= float(input("Enter limit price: "))
                while True:
                    if side=='BUY' and price>=float(current_price):
                        logger.warning("For BUY limit orders, limit price must be less than current price.")
                        print("For BUY limit orders, limit price must be less than current price. Please re-enter.")
                        price= float(input("Enter limit price: "))
                    elif side=='SELL' and price<=float(current_price):
                        logger.warning("For SELL limit orders, limit price must be greater than current price.")
                        print("For SELL limit orders, limit price must be greater than current price. Please re-enter.")
                        price= float(input("Enter limit price: "))
                    else:
                        break            
                limit_price= 0
                stop_price=0
                if side=='BUY':
                    while True:
                        stop_price= float(input("Enter stop price: "))
                        limit_price= float(input("Enter limit price: "))
                        if current_price > stop_price or stop_price>limit_price:
                            print("For BUY limit orders, stop price must be less than limit price and current price must be less than both other prices. Please re-enter.")
                        else:
                            break
                elif side=='SELL':
                    while True:
                        stop_price= float(input("Enter stop price: "))
                        limit_price= float(input("Enter limit price: "))
                        if current_price < stop_price or stop_price<limit_price:
                            print("For SELL limit orders, stop price must be greater than limit price and current price must be greter than both other prices. Please re-enter.")
                        else:
                            break
                order=place_oco_order(bot.client, pair, quantity, side, price, stop_price, limit_price)    
                print("Order placed:", order['orderId'])
        except Exception as e:
            print(f"An error occurred: {e}")

    elif choice == '8':
        logger.info("Exiting Trading Bot")
        print("Exiting...")
    else:
        logger.warning("Invalid choice entered, exiting.")
        print("Exiting...")
        # exit()