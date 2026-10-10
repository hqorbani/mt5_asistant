import MetaTrader5 as mt5

def connect_to_metatrader():
    if not mt5.initialize():
        print("Initialization failed")
        return False
    return True

def get_symbol_info(symbol):
    return mt5.symbol_info(symbol)


def place_order(symbol, order_type, lot, price, sl, tp , comment= "mt5 asistant by irsa technology"):
    # استفاده از متدهای MetaTrader5 برای ارسال سفارش
    if order_type == "Buy":
        action = mt5.TRADE_ACTION_DEAL
        order_type = mt5.ORDER_TYPE_BUY
        type_filling = mt5.ORDER_FILLING_RETURN
    elif order_type == "Sell":
        action = mt5.TRADE_ACTION_DEAL
        order_type = mt5.ORDER_TYPE_SELL
        type_filling = mt5.ORDER_FILLING_RETURN
    elif order_type == "Buy_Limit":
        action = mt5.TRADE_ACTION_PENDING
        order_type = mt5.ORDER_TYPE_BUY_LIMIT
        type_filling = mt5.ORDER_FILLING_FOK
    elif order_type == "Sell_Limit":
        action = mt5.TRADE_ACTION_PENDING
        order_type = mt5.ORDER_TYPE_SELL_LIMIT
        type_filling = mt5.ORDER_FILLING_FOK

    request = {
    "action": action,
    "symbol": symbol,
    "volume": lot,
    "type": order_type,
    "price": price,
    "sl": sl,
    "tp": tp,
    "deviation": 20,
    "magic": 234000,
    "comment": comment,
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": type_filling
    }
    if  connect_to_metatrader():
        return mt5.order_send(request)
    else:
        return None
     

