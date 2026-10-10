import MetaTrader5 as mt5
def calculate_profit_loss(order_type , symbol, lot, entry_price, stop_loss_price, take_profit_price):
    if order_type == 'Buy Limit':
        profit = (take_profit_price - entry_price) * lot
        profit = mt5.order_calc_profit(mt5.ORDER_TYPE_BUY , symbol, lot, entry_price, take_profit_price)
        loss = mt5.order_calc_profit(mt5.ORDER_TYPE_BUY , symbol, lot, entry_price, stop_loss_price)
    elif order_type == 'Sell Limit':
        profit = mt5.order_calc_profit(mt5.ORDER_TYPE_SELL , symbol, lot, entry_price, take_profit_price)
        loss = mt5.order_calc_profit(mt5.ORDER_TYPE_SELL , symbol, lot, entry_price, stop_loss_price)
    return profit, loss

def calculate_margin(symbol,order_type, lot , entry_price):
    # محاسبه مارجین
    return mt5.order_calc_margin(mt5.ORDER_TYPE_BUY if order_type.lower() == "buy" else mt5.ORDER_TYPE_SELL,
                                    symbol, lot, entry_price)

def calculate_risk_reward(profit, loss):
    print(loss, "loss", round(loss , 2))
    if loss != 0:
        risk_reward = profit / abs(round(loss , 2))
    else:
        risk_reward = 'Infinity'
    return risk_reward
