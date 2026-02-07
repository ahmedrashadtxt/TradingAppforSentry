# 📈 ProTrade Sentry Demo

A mock desktop trading application built with **Python (Tkinter)** to demonstrate how **Sentry.io** handles error tracking, performance monitoring, and crash reporting in a desktop environment.

<br>
<img width="400" alt="image" src="https://github.com/user-attachments/assets/cd31a9cf-eac2-4f68-9dbf-6bd9ecea9758" />
</br>


This project serves as a Proof of Concept (POC) to validate Sentry's capabilities for:
- 🐞 Capturing **Unhandled Crashes** (Desktop to Cloud).
- 🐢 Tracing **Performance Bottlenecks** (Spans & Transactions).
- 👣 Tracking **User Actions** (Breadcrumbs) prior to errors.
- 🔧 Handling **"Silent" UI Exceptions** in frameworks like Tkinter/WPF.

## 🚀 Prerequisites

* **Python 3.x** installed on your machine.
* A free **[Sentry.io](https://sentry.io)** account.
* A created **Sentry Project** (Choose "Python" as the platform - Vanilla option).

## 📦 Installation

1.  **Clone the repository** (or download the source code):
    ```bash
    git clone https://github.com/yourusername/TradingAppforSentry.git
    cd TradingAppforSentry
    ```

2.  **Install the Sentry SDK**:
    ```bash
    pip install sentry-sdk
    ```

## ⚙️ Configuration

1.  Open `trading_app.py` in your code editor.
2.  Locate the Sentry initialization block at the top of the file:
    ```python
    sentry_sdk.init(
        dsn="https://examplePublicKey@o0.ingest.sentry.io/0",  # <--- REPLACE THIS
        enable_tracing=True,
        traces_sample_rate=1.0,
        send_default_pii=True
    )
    ```
3.  Replace `"YOUR_DSN_GOES_HERE"` with your actual DSN key found in **Sentry > Settings > Projects > [Your Project] > Client Keys (DSN)**.

## 🖥️ Usage & Demo Script

Run the application from your terminal:
```bash
python trading_app.py
```

Use the application buttons to demonstrate specific Sentry features to stakeholders:

| Button Name | Action Performed | Sentry Feature Demonstrated |
| :--- | :--- | :--- |
| **Buy 100 Gold** | Logs a "Success" message. | **Breadcrumbs:** Shows the "Story" of user actions leading up to a crash. |
| **Apply Margin** | Triggers a handled logic error. | **Captured Exceptions:** Demonstrates logging errors (`try/catch`) without crashing the app. |
| **High Freq. Trade** | Crashes the app (Division by Zero). | **Global Handler:** Shows how Sentry catches hard crashes that usually kill the desktop process. |
| **Load Charts** | Freezes app for 3 seconds. | **Performance Tracing:** Demonstrates **Waterfalls & Spans** to identify *why* an operation is slow. |

## 🔍 Key Technical Concepts
1. The "Tkinter Trap" (Global Error Hook)
Standard Python try/catch blocks do not always catch UI thread errors in Tkinter. This project implements a bridge to forward Tkinter's internal errors to Sentry:

```
# Forces Tkinter to report errors to Sentry instead of just printing to console
def on_tkinter_error(exc_type, exc_value, exc_traceback):
    sentry_sdk.capture_exception((exc_type, exc_value, exc_traceback))

root.report_callback_exception = on_tkinter_error
```

2. Distributed Tracing (Performance)
The "Load Charts" feature demonstrates how to break down a slow process into Child Spans to isolate bottlenecks:

```
with sentry_sdk.start_transaction(name="load_charts"):
    with sentry_sdk.start_span(op="db.query", description="Fetch Data"):
        time.sleep(3) # <--- Sentry highlights this span as the cause of slowness
```

## 📊 Dashboard Guide
After triggering the errors in the app, navigate to your Sentry Dashboard:

1. **Issues Tab:** View grouped errors (e.g., `ZeroDivisionError`).
   * *Look for:* The **Breadcrumbs** section at the bottom to see your "Buy Gold" clicks.
   * *Look for:* The **Tags** section to see User Info (`username: pro_trader_x`).

2. **Explore Tab:** View the `load_charts` transaction under Traces.
   * *Look for:* The **Waterfall Chart** showing the 3-second plus duration bars.
  
List of errors captured by Sentry:
<img width="3168" height="1646" alt="image" src="https://github.com/user-attachments/assets/97da8e7a-cfcf-45e4-9c18-ae16081c5c2e" />

Breadcrumbs showing step-by-step action performed by user before getting error:
<img width="3146" height="1642" alt="image" src="https://github.com/user-attachments/assets/f83c7d54-6b11-4a94-8634-6846ee1ee1ff" />

Performance issue detected by Sentry are logged here under Explore --> Traces:
<img width="3162" height="1670" alt="image" src="https://github.com/user-attachments/assets/fb4bb16f-9704-49eb-bfb2-18cdc1dc9be5" />



  
## 🤝 Contributing
This is a demo repository. Feel free to open a PR to add more crash scenarios (e.g., Memory Leaks, HTTP Timeouts).

## 📄 License
MIT
