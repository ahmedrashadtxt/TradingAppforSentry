import tkinter as tk
from tkinter import messagebox
import time
import sentry_sdk

# --- 1. SENTRY CONFIGURATION ---
# Paste your DSN here (found in Sentry -> Settings -> Client Keys)
sentry_sdk.init(
    dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
    
    # This enables "Distributed Tracing" to see slow performance
    enable_tracing=True,
    
    # 1.0 means capture 100% of transactions for testing
    traces_sample_rate=1.0, 
    
    # Capture info about the user (e.g., username, IP)
    send_default_pii=True
)

# Set a fake user context (Simulating a logged-in trader)
sentry_sdk.set_user({"id": "42", "email": "trader@example.com", "username": "pro_trader_x"})

class TradingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ProTrade v1.0 (Sentry Demo)")
        self.root.geometry("400x300")

        # Label
        self.label = tk.Label(root, text="Market Status: OPEN", font=("Arial", 14))
        self.label.pack(pady=10)

        # Button 1: Successful Action (Breadcrumb)
        self.btn_buy = tk.Button(root, text="Buy 100 Gold (GLD)", command=self.buy_stock, bg="#d4f7d4")
        self.btn_buy.pack(pady=5, fill=tk.X, padx=20)

        # Button 2: Logic Error (Handled Exception)
        self.btn_margin = tk.Button(root, text="Apply Margin (Logic Error)", command=self.apply_margin, bg="#fff3cd")
        self.btn_margin.pack(pady=5, fill=tk.X, padx=20)

        # Button 3: CRASH (Unhandled Exception)
        self.btn_crash = tk.Button(root, text="Execute High Frequency Trade (CRASH)", command=self.crash_app, bg="#f8d7da")
        self.btn_crash.pack(pady=5, fill=tk.X, padx=20)

        # Button 4: Performance Issue (Slow Transaction)
        self.btn_slow = tk.Button(root, text="Load Historical Charts (Slow)", command=self.slow_operation, bg="#e2e3e5")
        self.btn_slow.pack(pady=5, fill=tk.X, padx=20)

    def buy_stock(self):
        # Sentry automatically records "Breadcrumbs" (user actions)
        sentry_sdk.add_breadcrumb(
            category="trade",
            message="User purchased 100 GLD",
            level="info"
        )
        messagebox.showinfo("Success", "Order Executed: Bought 100 GLD")

    def apply_margin(self):
        # Simulating a logic error we want to track but not crash the app
        try:
            limit = 5000
            balance = 1000
            if balance < limit:
                raise ValueError("Insufficient equity for margin call")
        except Exception as e:
            # We catch it, but send it to Sentry anyway
            sentry_sdk.capture_exception(e)
            messagebox.showwarning("Error", "Margin application failed (Logged to Sentry)")

    def crash_app(self):
        # This will crash the app entirely (Division by Zero)
        # Sentry's global handler will catch this automatically
        calculation = 100 / 0 

    def slow_operation(self):
        # Starts a transaction to measure performance
        with sentry_sdk.start_transaction(name="load_charts"):
            # Simulate a slow API call or DB query
            time.sleep(3) 
            messagebox.showinfo("Done", "Charts Loaded (That took too long!)")

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingApp(root)

    def on_tkinter_error(exc_type, exc_value, exc_traceback):
        # 1. Send the error to Sentry
        sentry_sdk.capture_exception((exc_type, exc_value, exc_traceback))
        
        # 2. (Optional) Print it to the terminal like normal so you still see it locally
        import traceback
        traceback.print_exception(exc_type, exc_value, exc_traceback)

    # --- TELL TKINTER TO USE THE FUNCTION ---
    root.report_callback_exception = on_tkinter_error
    root.mainloop()