import tkinter as tk
from tkinter import messagebox
from base import BasicBot
from binance import Client

class TradingBotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Trading Bot")
        self.root.geometry("500x500")

        # --- Dropdown for trade type ---
        tk.Label(root, text="Select Trade Type").pack(pady=5)
        self.trade_type = tk.StringVar(value="Market")
        trade_options = ["Market", "Limit", "Stop-Limit", "OCO"]
        self.dropdown = tk.OptionMenu(root, self.trade_type, *trade_options, command=self.update_fields)
        self.dropdown.pack(pady=5)

        # Frame for dynamic input fields
        self.fields_frame = tk.Frame(root)
        self.fields_frame.pack(pady=10, fill="both")

        # Order history listbox
        tk.Label(root, text="Order History").pack(pady=5)
        self.order_listbox = tk.Listbox(root, width=60, height=10)
        self.order_listbox.pack(pady=5)

        # Show initial fields
        self.update_fields("Market")

    def clear_fields(self):
        for widget in self.fields_frame.winfo_children():
            widget.destroy()

    def update_fields(self, choice):
        self.clear_fields()

        if choice == "Market":
            tk.Label(self.fields_frame, text="Trading Pair").pack(pady=5)
            self.pair_entry = tk.Entry(self.fields_frame)
            self.pair_entry.pack()

            tk.Label(self.fields_frame, text="Quantity").pack(pady=5)
            self.qty_entry = tk.Entry(self.fields_frame)
            self.qty_entry.pack()

        elif choice == "Limit":
            tk.Label(self.fields_frame, text="Trading Pair").pack(pady=5)
            self.pair_entry = tk.Entry(self.fields_frame)
            self.pair_entry.pack()

            tk.Label(self.fields_frame, text="Quantity").pack(pady=5)
            self.qty_entry = tk.Entry(self.fields_frame)
            self.qty_entry.pack()

            tk.Label(self.fields_frame, text="Limit Price").pack(pady=5)
            self.price_entry = tk.Entry(self.fields_frame)
            self.price_entry.pack()

        elif choice == "Stop-Limit":
            tk.Label(self.fields_frame, text="Trading Pair").pack(pady=5)
            self.pair_entry = tk.Entry(self.fields_frame)
            self.pair_entry.pack()

            tk.Label(self.fields_frame, text="Quantity").pack(pady=5)
            self.qty_entry = tk.Entry(self.fields_frame)
            self.qty_entry.pack()

            tk.Label(self.fields_frame, text="Stop Price").pack(pady=5)
            self.stop_entry = tk.Entry(self.fields_frame)
            self.stop_entry.pack()

            tk.Label(self.fields_frame, text="Limit Price").pack(pady=5)
            self.limit_entry = tk.Entry(self.fields_frame)
            self.limit_entry.pack()

        elif choice == "OCO":
            tk.Label(self.fields_frame, text="Trading Pair").pack(pady=5)
            self.pair_entry = tk.Entry(self.fields_frame)
            self.pair_entry.pack()

            tk.Label(self.fields_frame, text="Quantity").pack(pady=5)
            self.qty_entry = tk.Entry(self.fields_frame)
            self.qty_entry.pack()

            tk.Label(self.fields_frame, text="Price").pack(pady=5)
            self.price_entry = tk.Entry(self.fields_frame)
            self.price_entry.pack()

            tk.Label(self.fields_frame, text="Stop Price").pack(pady=5)
            self.stop_entry = tk.Entry(self.fields_frame)
            self.stop_entry.pack()

            tk.Label(self.fields_frame, text="Stop Limit Price").pack(pady=5)
            self.stop_limit_entry = tk.Entry(self.fields_frame)
            self.stop_limit_entry.pack()

        # Submit button
        tk.Button(self.fields_frame, text="Place Order", command=self.place_order).pack(pady=10)

    def place_order(self):
        trade_type = self.trade_type.get()
        pair = getattr(self, "pair_entry", None).get() if hasattr(self, "pair_entry") else ""
        qty = getattr(self, "qty_entry", None).get() if hasattr(self, "qty_entry") else ""
        price = getattr(self, "price_entry", None).get() if hasattr(self, "price_entry") else ""
        stop = getattr(self, "stop_entry", None).get() if hasattr(self, "stop_entry") else ""
        limit = getattr(self, "limit_entry", None).get() if hasattr(self, "limit_entry") else ""
        stop_limit = getattr(self, "stop_limit_entry", None).get() if hasattr(self, "stop_limit_entry") else ""

        # Build order summary string
        order_details = f"{trade_type} | Pair: {pair} | Qty: {qty}"
        if price: order_details += f" | Price: {price}"
        if stop: order_details += f" | Stop: {stop}"
        if limit: order_details += f" | Limit: {limit}"
        if stop_limit: order_details += f" | StopLimit: {stop_limit}"

        # Add to listbox
        self.order_listbox.insert(tk.END, order_details)

        # Show confirmation
        messagebox.showinfo("Order", f"{trade_type} order placed!")


if __name__ == "__main__":
    root = tk.Tk()
    app = TradingBotUI(root)
    root.mainloop()