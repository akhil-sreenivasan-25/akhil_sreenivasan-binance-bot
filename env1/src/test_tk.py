import tkinter as tk
from tkinter import messagebox,ttk
from binance import Client
from base import BasicBot
import logging
from market_orders import place_market_order
from limit_order import place_limit_order
from advanced.stop_limit_order import place_stop_limit_order



class TradingBotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Trading Bot")
        self.root.geometry("500x600")

        #login frame
        self.login_frame = tk.Frame(root)
        self.login_frame.pack(pady=20)

        # API Key input
        tk.Label(self.login_frame, text="Enter API Key: ").pack(pady=5)
        self.api_key_entry = tk.Entry(self.login_frame, width=50)
        self.api_key_entry.pack(pady=5)

        # API Secret input
        tk.Label(self.login_frame, text="Enter API Secret: ").pack(pady=5)
        self.api_secret_entry = tk.Entry(self.login_frame, width=50)
        self.api_secret_entry.pack(pady=5)

        # Connect button
        tk.Button(self.login_frame, text="Connect", command=self.connect).pack(pady=10)
        tk.Button(self.login_frame, text="Connect default account", command=self.connect_default).pack(pady=10)
    # connecting to binance testnet
    def connect(self):
        api_key = self.api_key_entry.get().strip()
        api_secret = self.api_secret_entry.get().strip()
        if not api_key or not api_secret:
            messagebox.showerror("Error", "API Key and Secret are required!")
            return
        try:
            self.bot = BasicBot(api_key=api_key, api_secret=api_secret)
            if self.bot.client.get_account():
                logger.info("Binance Testnet connection successful.")
                messagebox.showinfo("Success", "Connection successful!")
                self.inital_block()
        except Exception as e:
            logger.error("Binance Testnet connection failed : " + str(e))
            messagebox.showerror("Connection Failed", f"Error: {e}")

    # Connecting with default API key and secret
    def connect_default(self):
        try:
            self.bot = BasicBot()
            if self.bot.client.get_account():
                logger.info("Binance Testnet connection successful.")
                messagebox.showinfo("Success", "Connection successful!")
                #call trading block
                self.inital_block()
        except Exception as e:
            logger.error("Binance Testnet connection failed : " + str(e))
            messagebox.showerror("Connection Failed", f"Error: {e}")

    def inital_block(self):
        #hide login frame
        self.login_frame.destroy()

        #inital frame
        self.inital_frame = tk.Frame(root)
        self.inital_frame.pack(pady=20)

        # --- Dropdown for trade type ---
        tk.Label(self.inital_frame, text="Select Trade Type").pack(pady=5)
        self.trade_type = tk.StringVar(value="Market")
        trade_options = ["Market", "Limit", "Stop-Limit"]
        self.dropdown = tk.OptionMenu(self.inital_frame, self.trade_type, *trade_options, command=self.update_fields)
        self.dropdown.pack(pady=5)

        # Frame for dynamic input fields
        self.fields_frame = tk.Frame(self.inital_frame)
        self.fields_frame.pack(pady=10, fill="both", expand=True)

        # Order history listbox
        self.history_frame = tk.Frame(self.inital_frame)
        self.history_frame.pack(side="bottom", fill="x", pady=10)

        tk.Label(self.history_frame, text="Executed orders").pack(pady=5)
        self.order_listbox = tk.Listbox(self.history_frame, width=60, height=10)
        self.order_listbox.pack(pady=5)

        # Show initial fields
        self.update_fields("Market")


    def clear_fields(self):
        for widget in self.fields_frame.winfo_children():
            widget.destroy()

    def update_fields(self, choice):
        self.clear_fields()

        if choice == "Market":
            self.pairs=self.market_pair()
            self.pair_var = tk.StringVar()
            self.pair_combo = ttk.Combobox(self.fields_frame, textvariable=self.pair_var, values=self.pairs, state="readonly")
            self.pair_combo.current(0)
            self.pair_combo.pack(pady=10)

            # Label to show price
            self.price_label = tk.Label(self.fields_frame, text="Price: ")
            self.price_label.pack(pady=5)

            # Bind event when selection changes
            self.pair_combo.bind("<<ComboboxSelected>>", self.update_price)
            self.update_price()  # Initial price update

            self.side_var = tk.StringVar(value="BUY")
            tk.Radiobutton(self.fields_frame, text="Buy", variable=self.side_var, value="BUY").pack()
            tk.Radiobutton(self.fields_frame, text="Sell", variable=self.side_var, value="SELL").pack()
            tk.Label(self.fields_frame, text="Quantity").pack(pady=5)
            self.qty_entry = tk.Entry(self.fields_frame)
            self.qty_entry.pack()

            # Submit button
            tk.Button(self.fields_frame, text="Place Order", command=self.tk_place_market_order).pack(pady=10)

        elif choice == "Limit":
            self.pairs=self.market_pair()
            self.pair_var = tk.StringVar()
            self.pair_combo = ttk.Combobox(self.fields_frame, textvariable=self.pair_var, values=self.pairs, state="readonly")
            self.pair_combo.current(0)
            self.pair_combo.pack(pady=10)

            # Label to show price
            self.price_label = tk.Label(self.fields_frame, text="Price: ")
            self.price_label.pack(pady=5)

            # Bind event when selection changes
            self.pair_combo.bind("<<ComboboxSelected>>", self.update_price)
            self.update_price()  # Initial price update

            # tk.Label(self.fields_frame, text="Trading Pair").pack(pady=5)
            # self.pair_entry = tk.Entry(self.fields_frame)
            # self.pair_entry.pack()

            self.side_var = tk.StringVar(value="BUY")
            tk.Radiobutton(self.fields_frame, text="Buy", variable=self.side_var, value="BUY").pack()
            tk.Radiobutton(self.fields_frame, text="Sell", variable=self.side_var, value="SELL").pack()

            tk.Label(self.fields_frame, text="Quantity").pack(pady=5)
            self.qty_entry = tk.Entry(self.fields_frame)
            self.qty_entry.pack()

            tk.Label(self.fields_frame, text="Limit Price").pack(pady=5)
            self.price_entry = tk.Entry(self.fields_frame)
            self.price_entry.pack()

            # Submit button
            tk.Button(self.fields_frame, text="Place Order", command=self.tk_place_limit_order).pack(pady=10)

        elif choice == "Stop-Limit":
            self.pairs=self.market_pair()
            self.pair_var = tk.StringVar()
            self.pair_combo = ttk.Combobox(self.fields_frame, textvariable=self.pair_var, values=self.pairs, state="readonly")
            self.pair_combo.current(0)
            self.pair_combo.pack(pady=10)

            # Label to show price
            self.price_label = tk.Label(self.fields_frame, text="Price: ")
            self.price_label.pack(pady=5)

            # Bind event when selection changes
            self.pair_combo.bind("<<ComboboxSelected>>", self.update_price)
            self.update_price()  # Initial price update


            self.side_var = tk.StringVar(value="BUY")
            tk.Radiobutton(self.fields_frame, text="Buy", variable=self.side_var, value="BUY").pack()
            tk.Radiobutton(self.fields_frame, text="Sell", variable=self.side_var, value="SELL").pack()            

            tk.Label(self.fields_frame, text="Quantity").pack(pady=5)
            self.qty_entry = tk.Entry(self.fields_frame)
            self.qty_entry.pack()

            tk.Label(self.fields_frame, text="Stop Price").pack(pady=5)
            self.stop_entry = tk.Entry(self.fields_frame)
            self.stop_entry.pack()

            tk.Label(self.fields_frame, text="Limit Price").pack(pady=5)
            self.limit_entry = tk.Entry(self.fields_frame)
            self.limit_entry.pack()

            # Submit button
            tk.Button(self.fields_frame, text="Place Order", command=self.tk_place_stop_limit_order).pack(pady=10)

        # elif choice == "OCO":
        #     tk.Label(self.fields_frame, text="Trading Pair").pack(pady=5)
        #     self.pair_entry = tk.Entry(self.fields_frame)
        #     self.pair_entry.pack()

        #     self.side_var = tk.StringVar(value="BUY")
        #     tk.Radiobutton(self.fields_frame, text="Buy", variable=self.side_var, value="BUY").pack()
        #     tk.Radiobutton(self.fields_frame, text="Sell", variable=self.side_var, value="SELL").pack()            

        #     tk.Label(self.fields_frame, text="Quantity").pack(pady=5)
        #     self.qty_entry = tk.Entry(self.fields_frame)
        #     self.qty_entry.pack()

        #     tk.Label(self.fields_frame, text="Price").pack(pady=5)
        #     self.price_entry = tk.Entry(self.fields_frame)
        #     self.price_entry.pack()

        #     tk.Label(self.fields_frame, text="Stop Price").pack(pady=5)
        #     self.stop_entry = tk.Entry(self.fields_frame)
        #     self.stop_entry.pack()

        #     tk.Label(self.fields_frame, text="Stop Limit Price").pack(pady=5)
        #     self.stop_limit_entry = tk.Entry(self.fields_frame)
        #     self.stop_limit_entry.pack()

        #     # Submit button
        #     tk.Button(self.fields_frame, text="Place Order", command=self.place_oco_order).pack(pady=10)
    
    def update_price(self, event=None):
            pair = self.pair_var.get()
            price = self.bot.client.get_symbol_ticker(symbol=pair)['price']  # Replace with API call
            self.price_label.config(text=f"Price: {price}")

    def market_pair(self):
        try:
            symbols = [s['symbol'] for s in self.bot.client.get_exchange_info()['symbols']]
            return symbols
        except Exception as e:
            logger.error(f"Error fetching market pairs: {e}")
            messagebox.showerror("Error", f"Could not fetch market pairs: {e}")
            return []

    def tk_place_market_order(self):
        # Placeholder for order placement logic
        try:
            pair = self.pair_var.get().strip().upper()
            qty = float(self.qty_entry.get().strip())
            side = self.side_var.get().upper()
            if pair not in self.market_pair():
                messagebox.showerror("Error", "Invalid Trading Pair!")
                return
            order = place_market_order(self.bot.client, pair, qty, side)
            # Check if order looks like an error response
            if isinstance(order, dict) and 'orderId' in order:
                 # Success case
                self.order_listbox.insert(tk.END, str(" orderId :"+str( order['orderId']) +"    "+" Pair :"+ str(order['symbol'])+"    "+" Side :"+ str(order['side'])+"    "+" Qty :"+ str(order['origQty'])))
                logger.info(f"Order placed successfully: {order}")
                messagebox.showinfo("Order Placed", "Market order placed successfully!")

            elif 'code' in order or 'msg' in order:
                # Error payload from API
                logger.error(f"Order failed: {order['msg']}")
                messagebox.showerror("Order Error", "check the quantity is valid.")

            else:
                logger.error(f"Unexpected order response: {order}")
                messagebox.showerror("Order Error", "check the quantity is valid.")
            self.qty_entry.delete(0, tk.END)

        except Exception as e:
            logger.error(f"Error placing market order: {e}")
            messagebox.showerror("Order Error", f"Error: value error")
            self.qty_entry.delete(0, tk.END)

    def tk_place_limit_order(self):
        # Placeholder for limit order placement logic
        try:
            pair = self.pair_var.get().strip().upper()
            qty = float(self.qty_entry.get().strip())
            side = self.side_var.get().upper()
            price = float(self.price_entry.get().strip())
            if pair not in self.market_pair():
                messagebox.showerror("Error", "Invalid Trading Pair!")
                return
            current_price = float(self.bot.client.get_symbol_ticker(symbol=pair)['price'])
            if (side == "BUY" and price >= current_price):
                messagebox.showerror("Error", "For BUY limit orders, the limit price must be below the current market price.")
                return
            elif (side == "SELL" and price <= current_price):
                messagebox.showerror("Error", "For SELL limit orders, the limit price must be above the current market price.")
                return
            order = place_limit_order(self.bot.client, pair, qty, side, price)
            # Check if order looks like an error response
            if isinstance(order, dict) and 'orderId' in order:
                 # Success case
                self.order_listbox.insert(tk.END, str(" orderId :"+str( order['orderId']) +"    "+" Pair :"+ str(order['symbol'])+"    "+" Side :"+ str(order['side'])+"    "+" Qty :"+ str(order['origQty'])))
                logger.info(f"Order placed successfully: {order}")
                messagebox.showinfo("Order Placed", "Market order placed successfully!")

            elif 'code' in order or 'msg' in order:
                # Error payload from API
                logger.error(f"Order failed: {order['msg']}")
                messagebox.showerror("Order Error", "check the quantity is valid.")

            else:
                logger.error(f"Unexpected order response: {order}")
                messagebox.showerror("Order Error", "check the quantity is valid.")
            self.qty_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)         

        except Exception as e:
            logger.error(f"Error placing market order: {e}")
            messagebox.showerror("Order Error", f"Error: value error")
            self.qty_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            

    def tk_place_stop_limit_order(self):
        # Placeholder for stop limit order placement logic
        try:
            pair = self.pair_var.get().strip().upper()
            qty = float(self.qty_entry.get().strip())
            side = self.side_var.get().upper()
            price = float(self.limit_entry.get().strip())
            stop_price = float(self.stop_entry.get().strip())
            if pair not in self.market_pair():
                messagebox.showerror("Error", "Invalid Trading Pair!")
                return
            current_price = float(self.bot.client.get_symbol_ticker(symbol=pair)['price'])
            if (side == "BUY" ):
                if (current_price >=  stop_price) or (stop_price >= price):
                    messagebox.showerror("Error", "For BUY stop-limit orders, the stop price must be above the current market price and limit price must be above stop price.")
                    return    
            elif (side == "SELL"):
                if (current_price <=  stop_price) or (stop_price <= price):
                    messagebox.showerror("Error", "For SELL stop-limit orders, the stop price must be below the current market price and limit price must be below stop price.")
                    return   
            else:
                messagebox.showerror("Error", "Invalid side! Choose BUY or SELL.")
                return
            # messagebox.showinfo("Info", f"Placing {side} stop-limit order for {qty} {pair} with stop price {stop_price} and limit price {price}.")
            order = place_stop_limit_order(self.bot.client, pair, qty, side, stop_price, price)
            # messagebox.showinfo("Info", f"Order response: {order}")
            # Check if order looks like an error response
            if isinstance(order, dict) and 'orderId' in order:
                 # Success case
                self.order_listbox.insert(tk.END, str(" orderId :"+str( order['orderId']) +"    "+" Pair :"+ str(order['symbol'])))
                logger.info(f"Order placed successfully: {order}")
                messagebox.showinfo("Order Placed", "Market order placed successfully!")

            elif 'code' in order or 'msg' in order:
                # Error payload from API
                logger.error(f"Order failed: {order['msg']}")
                messagebox.showerror("Order Error", "check the quantity is valid.")

            else:
                logger.error(f"Unexpected order response: {order}")
                messagebox.showerror("Order Error", "check the quantity is valid.")
            self.qty_entry.delete(0, tk.END)
            self.stop_entry.delete(0, tk.END)
            self.limit_entry.delete(0, tk.END)        

        except Exception as e:
            logger.error(f"Error placing market order: {e}")
            messagebox.showerror("Order Error", f"Error: value error {e}")
            self.qty_entry.delete(0, tk.END)
            self.stop_entry.delete(0, tk.END)
            self.limit_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingBotUI(root)
    logger = logging.getLogger(__name__)
    root.mainloop()