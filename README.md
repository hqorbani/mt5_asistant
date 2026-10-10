# MT5 Trade Assistant

MT5 Trade Assistant is a Python desktop application designed to support risk management and simplify trade preparation for MetaTrader 5.

The application calculates position size, estimated profit and loss, risk-to-reward ratio, and required margin based on the selected trading symbol and user-defined trade parameters.

## Features

* **Position Size Calculation:** Estimates trade volume based on account balance, risk percentage, and stop-loss distance.
* **Profit and Loss Estimation:** Calculates potential profit and loss using MetaTrader 5.
* **Risk-to-Reward Ratio:** Displays the estimated reward-to-risk ratio for a trade.
* **Margin Calculation:** Estimates the margin required for the selected position.
* **Order Submission:** Supports submitting Buy Limit and Sell Limit orders through MetaTrader 5.
* **Symbol Suggestions:** Helps users find trading symbols by typing their names.
* **Customizable Interface:** Provides multiple visual themes through `ttkbootstrap`.
* **Input Validation:** Checks trading parameters before performing calculations or submitting orders.

## Requirements

* Windows
* Python 3.10 or a compatible version supported by the installed dependencies
* MetaTrader 5 desktop terminal
* A configured MetaTrader 5 account
* Python packages listed in `requirements.txt`
* Pillow, for image handling in the About window

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/hqorbani/mt5_asistant.git
   cd mt5_asistant
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .env
   ```

3. Activate the virtual environment in PowerShell:

   ```powershell
   .\.env\Scripts\Activate.ps1
   ```

4. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   python -m pip install Pillow
   ```

## Running the Application

1. Open the MetaTrader 5 desktop terminal and sign in to your account.
2. Ensure that the terminal is running and available to the Python MetaTrader 5 integration.
3. From the project root, run:

   ```bash
   python main.py
   ```

## How It Works

Enter the trading symbol, order type, risk percentage, entry price, stop-loss, and take-profit levels.

The application uses account and symbol information from MetaTrader 5 to estimate the appropriate position size and calculate the trade's potential profit, loss, risk-to-reward ratio, and margin requirement.

Review all calculated values before submitting an order.

## Risk Disclaimer

This application is a trading assistance tool, not financial advice. Trading involves significant risk, and calculated values are estimates that may differ from actual execution results.

Always verify order parameters and test changes using a demo account before trading with real funds.

## Author

**Hamzeh Qorbani**

* Email: [h.qorbani7@gmail.com](mailto:h.qorbani7@gmail.com)

---

© Hamzeh Qorbani
