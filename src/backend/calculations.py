
import MetaTrader5 as mt5


BUY_ORDER_TYPES = {"buy", "buy limit"}
SELL_ORDER_TYPES = {"sell", "sell limit"}


def _get_mt5_order_type(order_type):
    """Convert a supported order type to its MetaTrader 5 constant."""
    normalized_type = order_type.strip().lower()

    if normalized_type in BUY_ORDER_TYPES:
        return mt5.ORDER_TYPE_BUY

    if normalized_type in SELL_ORDER_TYPES:
        return mt5.ORDER_TYPE_SELL

    raise ValueError(f"Unsupported order type: {order_type!r}")


def calculate_profit_loss(
    order_type,
    symbol,
    lot,
    entry_price,
    stop_loss_price,
    take_profit_price,
):
    """Calculate estimated profit and loss using MetaTrader 5."""
    mt5_order_type = _get_mt5_order_type(order_type)

    if lot <= 0:
        raise ValueError("Lot size must be greater than zero.")

    if entry_price <= 0 or stop_loss_price <= 0 or take_profit_price <= 0:
        raise ValueError("Prices must be greater than zero.")

    profit = mt5.order_calc_profit(
        mt5_order_type, symbol, lot, entry_price, take_profit_price
    )
    loss = mt5.order_calc_profit(
        mt5_order_type, symbol, lot, entry_price, stop_loss_price
    )

    if profit is None or loss is None:
        error = mt5.last_error()
        raise RuntimeError(
            f"MetaTrader 5 could not calculate profit/loss: {error}"
        )

    return profit, loss


def calculate_margin(symbol, order_type, lot, entry_price):
    """Calculate the estimated margin required for an order."""
    mt5_order_type = _get_mt5_order_type(order_type)

    if lot <= 0:
        raise ValueError("Lot size must be greater than zero.")

    if entry_price <= 0:
        raise ValueError("Entry price must be greater than zero.")

    margin = mt5.order_calc_margin(
        mt5_order_type, symbol, lot, entry_price
    )

    if margin is None:
        error = mt5.last_error()
        raise RuntimeError(
            f"MetaTrader 5 could not calculate margin: {error}"
        )

    return margin


def calculate_risk_reward(profit, loss):
    """Return the reward-to-risk ratio using the absolute loss."""
    if loss == 0:
        return float("inf")

    return profit / abs(loss)
