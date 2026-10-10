import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from src.backend.calculations import calculate_profit_loss, calculate_margin, calculate_risk_reward
from src.backend.metatrader_integration import connect_to_metatrader, get_symbol_info, place_order
import MetaTrader5 as mt5
from src.frontend.about import About
from src.frontend.guide import Guide

about = About()
guide = Guide()
class TradingApp(tb.Window):
    def __init__(self):
        super().__init__(themename='darkly')
        self.order_result_dict = None
        self.title('MT5 Assistant')
        self.geometry('320x800+0+100')
        if not connect_to_metatrader():
            messagebox.showerror("Error", "Failed to connect to MetaTrader 5")
            self.quit()

        self.account_info = mt5.account_info()
        # Create menu
        self.create_menu()
        # Create input frame
        self.create_input_frame()

        # Create output frame
        self.create_calculated_lot_frame()
        self.create_profit_frame()
        self.create_loss_frame()
        self.create_risk_reward_frame()
        self.create_margin_frame()
        self.create_pip_value_frame()
        self.create_number_pip_frame()
        self.creat_order_button()
        self.creat_order_result()

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Theme menu
        theme_menu = tk.Menu(menubar, tearoff=0)
        # theme_menu.add_command(label='Light: united', command=lambda: self.set_theme('united'))
        theme_menu.add_command(label='Light: sandstone', command=lambda: self.set_theme('sandstone'))
        theme_menu.add_command(label='Dark: darkly', command=lambda: self.set_theme('darkly'))
        theme_menu.add_command(label='Dark: superhero', command=lambda: self.set_theme('superhero'))
        menubar.add_cascade(label='Theme', menu=theme_menu)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label='About', command=about.show_about)
        help_menu.add_command(label='Guide', command=guide.show_guide)
        menubar.add_cascade(label='Help', menu=help_menu)
    def create_input_frame(self):
        input_frame = tb.Frame(self)
        input_frame.pack(pady=10)

        entry_width = 20  # Fixed width for input fields
        # Balance
        tb.Label(input_frame, text='Balance:').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.balance = tb.Entry(input_frame, width=entry_width)
        self.balance.insert(0, f"{self.account_info.balance} {self.account_info.currency}")
        self.balance.config(state='readonly')
        self.balance.grid(row=0, column=1, padx=5, pady=5)

        # Equity
        tb.Label(input_frame, text='Equity:').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.equity = tb.Entry(input_frame, width=entry_width)
        self.equity.insert(0, f"{self.account_info.equity}")
        self.equity.config(state='readonly')
        self.equity.grid(row=1, column=1, padx=5, pady=5)

        # Free Margin
        tb.Label(input_frame, text='Free Margin:').grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.margin_free = tb.Entry(input_frame, width=entry_width)
        self.margin_free.insert(0, f"{self.account_info.margin_free}")
        self.margin_free.config(state='readonly')
        self.margin_free.grid(row=2, column=1, padx=5, pady=5)
        
        # Symbol
        tb.Label(input_frame, text='Symbol:').grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.symbol = tb.Combobox(input_frame, state = 'pressed', width=entry_width - 2)
        self.symbol.grid(row=3, column=1, padx=5, pady=5)
        self.symbol.bind('<KeyRelease>', self.update_symbol_suggestions)

        # Order Type
        tb.Label(input_frame, text='Order Type:').grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.order_type = tb.Combobox(input_frame, values=['Buy Limit', 'Sell Limit'], width=entry_width - 2)
        self.order_type.grid(row=4, column=1, padx=5, pady=5)
        self.order_type.bind('<KeyRelease>' , self.update_order_type_suggestions)
        
        # risk percent
        tb.Label(input_frame, text='risk percent:').grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.risk_percent = tb.Entry(input_frame, width= entry_width)
        self.risk_percent.grid(row=5, column=1, padx=5, pady=5)
        self.risk_percent.bind("<KeyRelease>", self.check_all_fields)

        # Entry Price
        tb.Label(input_frame, text='Entry Price:').grid(row=6, column=0, padx=5, pady=5, sticky='w')
        self.entry_price = tb.Entry(input_frame, width=entry_width)
        self.entry_price.grid(row=6, column=1, padx=5, pady=5)
        self.entry_price.bind("<KeyRelease>", self.check_all_fields)

        # Stop Loss Price
        tb.Label(input_frame, text='Stop Loss Price:').grid(row=7, column=0, padx=5, pady=5, sticky='w')
        self.stop_loss_price = tb.Entry(input_frame, width= entry_width)
        self.stop_loss_price.grid(row=7, column=1, padx=5, pady=5)
        self.stop_loss_price.bind("<KeyRelease>", self.check_all_fields)

        # Take Profit Price
        tb.Label(input_frame, text='Take Profit Price:').grid(row=8, column=0, padx=5, pady=5, sticky='w')
        self.take_profit_price = tb.Entry(input_frame, width= entry_width)
        self.take_profit_price.grid(row=8, column=1, padx=5, pady=5)
        self.take_profit_price.bind("<KeyRelease>", self.check_all_fields)
    
    def create_calculated_lot_frame(self):
        calculated_lot_frame = tb.Frame(self , bootstyle="info")
        calculated_lot_frame.pack(pady=5)
        self.calculated_lot_result = tb.Label(calculated_lot_frame, bootstyle="info", anchor='center', font=('Helvetica', 12))
        self.calculated_lot_result.pack()

    def create_loss_frame(self):
        loss_frame = tb.Frame(self , bootstyle="info")
        loss_frame.pack(pady=5)
        self.loss_result = tb.Label(loss_frame, anchor='center', bootstyle="danger" , font=('Helvetica', 12))
        self.loss_result.pack()

    def create_profit_frame(self):
        profit_frame = tb.Frame(self , bootstyle="info")
        profit_frame.pack(pady=5)
        self.profit_result = tb.Label(profit_frame, anchor='center', bootstyle="success", font=('Helvetica', 12))
        self.profit_result.pack()
    
    def create_margin_frame(self):
        margin_frame = tb.Frame(self)
        margin_frame.pack(pady=5)
        self.margin_result = tb.Label(margin_frame, anchor='center' , bootstyle="info", font=('Helvetica', 12))
        self.margin_result.pack()
    
    def create_risk_reward_frame(self):
        risk_reward_frame = tb.Frame(self)
        risk_reward_frame.pack(pady=5)
        self.risk_reward_result = tb.Label(risk_reward_frame, anchor='center', bootstyle="info", font=('Helvetica', 12))
        self.risk_reward_result.pack()
    
    def create_pip_value_frame(self):
        pip_value_frame = tb.Frame(self)
        pip_value_frame.pack(pady=5)
        self.pip_value_result = tb.Label(pip_value_frame, anchor='center', bootstyle="info", font=('Helvetica', 12))
        self.pip_value_result.pack()
    
    def create_number_pip_frame(self):
        number_pip_frame = tb.Frame(self)
        number_pip_frame.pack(pady=5)
        self.number_pip_result = tb.Label(number_pip_frame, anchor='center', bootstyle="info", font=('Helvetica', 12))
        self.number_pip_result.pack()
    
    def creat_order_button(self):
        order_btn_frame = tb.Frame(self)
        order_btn_frame.pack(pady=5)
        self.order_btn = tb.Button(order_btn_frame, bootstyle="info")
        self.order_btn.pack_forget()
    
    def creat_order_result(self):
        order_result_frame = tb.Frame(self)
        order_result_frame.pack(pady= 5)
        self.order_result_label = tb.Label(order_result_frame, anchor='center', bootstyle="info", font=('Helvetica', 12))
        self.order_result_label.pack()

    def set_theme(self, theme):
        self.style.theme_use(theme)

    def show_about(self):
        messagebox.showinfo("About", "MetaTrader 5 Assistant\nCreated by [Your Name]")

    def show_guide(self):
        messagebox.showinfo("Guide", "Guide content here...")
    
    def check_all_fields(self, event):
        """Check all fields and display message if empty"""
        if all([
            self.symbol.get(),
            self.order_type.get(),
            self.risk_percent.get(),
            self.entry_price.get(),
            self.stop_loss_price.get(),
            self.take_profit_price.get()
            ]):
            self.calculate_lot()
        else:
            self.calculated_lot_result.config(text = "please complete all fields")
            self.order_btn.pack_forget()
    
    def calculate_lot(self):
        default_lot = 1
        
        """Calculate and display results"""
        try:
            symbol = self.symbol.get()
            order_type = self.order_type.get()
            risk_percent = float(self.risk_percent.get())
            entry_price = float(self.entry_price.get())
            stop_loss_price = float(self.stop_loss_price.get())
            take_profit_price = float(self.take_profit_price.get())
            symbol_info = mt5.symbol_info(symbol)
            
            risk_amount = self.account_info.balance * risk_percent / 100

            if order_type == 'Buy Limit' and (stop_loss_price >= entry_price or take_profit_price <= entry_price):
                self.order_btn.config(text="Buy Limit")
                raise ValueError('Invalid prices for Buy order')
            elif order_type == 'Sell Limit' and (stop_loss_price <= entry_price or take_profit_price >= entry_price):
                self.order_btn.config(text="Sell Limit")
                raise ValueError('Invalid prices for Sell order')
            
           
            profit, loss = calculate_profit_loss(order_type , symbol, default_lot, entry_price, stop_loss_price, take_profit_price)
            number_pips = abs(entry_price - stop_loss_price) * 10 ** (symbol_info.digits -1)
            pip_value = abs(loss / number_pips)
            calculated_lot = round(risk_amount / (number_pips * pip_value) , 2)
            profit, loss = calculate_profit_loss(order_type , symbol, calculated_lot, entry_price, stop_loss_price, take_profit_price)
            margin = calculate_margin(symbol, order_type, calculated_lot, entry_price)
            risk_reward = calculate_risk_reward(profit, loss)
            self.calculated_lot_result.config(text = f"lot: {calculated_lot:.2f}")
            self.loss_result.config(text = f"Loss: {loss:.2f} {self.account_info.currency}")
            self.profit_result.config(text = f"Profit: {profit:.2f} {self.account_info.currency}")
            self.risk_reward_result.config(text = f"risk / reward: {risk_reward:.2f}")
            self.margin_result.config(text = f"margin: {margin:.2f} {self.account_info.currency}")
            # self.number_pip_result.config(text = f"number pips: {number_pips}")
            # self.pip_value_result.config(text = f"pip value: {pip_value:.2f}")
            if order_type == "Buy Limit":
                self.order_btn.config(text="Buy Limit")
            elif order_type == "Sell Limit":
                self.order_btn.config(text="Sell Limit")
            request = {
                "action": mt5.TRADE_ACTION_PENDING,
                "symbol": symbol,
                "volume": calculated_lot,
                "type": mt5.ORDER_TYPE_BUY_LIMIT,
                "price": entry_price,
                "sl": stop_loss_price,
                "tp": take_profit_price,
                "deviation": 20,
                "magic": 234000,
                "comment": "comment",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_FOK
                }
            self.order_btn.config(command= lambda:
                                  self.call_place_order(
                                                symbol ,
                                                order_type ,
                                                calculated_lot ,
                                                entry_price ,
                                                stop_loss_price ,
                                                take_profit_price
                                            )
                )
            self.order_btn.pack()
            

        except ValueError as e:
            self.calculated_lot_result.config(text = "please complete all fields")
            self.order_btn.pack_forget()

    def call_place_order(self,
                        symbol ,
                        order_type ,
                        calculated_lot ,
                        entry_price ,
                        stop_loss_price ,
                        take_profit_price):
                        # result = mt5.order_send(request)
                        result = self.place_order_internal(
                                                symbol ,
                                                order_type ,
                                                calculated_lot ,
                                                entry_price ,
                                                stop_loss_price ,
                                                take_profit_price
                                            )
                        # print("res:::\n", result)
                        
                        if result is not None:
                            self.order_result_dict = result._asdict()
                            if self.order_result_dict['retcode'] != mt5.TRADE_RETCODE_DONE:
                                self.order_result_label.config(text = f"order_send failed, {self.order_result_dict['comment']}")
                            else:
                                self.order_result_label.config(text = self.order_result_dict['comment'])

                        
        
    def update_symbol_suggestions(self, event):
        """Suggest similar symbols as you type"""
        typed_text = self.symbol.get()
        if len(typed_text) >= 3:
            all_symbols = [symbol.name for symbol in mt5.symbols_get()]
            suggestions = [s for s in all_symbols if typed_text.lower() in s.lower()]
            self.symbol['values'] = suggestions
            self.symbol.event_generate('<Down>')
        else:
            self.symbol['values'] = []
    
    def update_order_type_suggestions(self, event):
        """پیشنهاد سفارش   """
        typed_text = self.order_type.get()
        if typed_text:
            suggestions = ["Buy Limit", "Sell Limit"]
            self.order_type['values'] = suggestions
            self.order_type.event_generate('<Down>')
        else:
            self.order_type['values'] = []
    
    def place_order_internal(self, symbol, order_type, lot, price, sl, tp , comment= "mt5 asistant by irsa technology"):
        # استفاده از متدهای MetaTrader5 برای ارسال سفارش
        print("order_type",order_type)
        if order_type == "Buy":
            action = mt5.TRADE_ACTION_DEAL
            order_type = mt5.ORDER_TYPE_BUY
            price = mt5.symbol_info_tick(symbol).ask
            type_filling = mt5.ORDER_FILLING_RETURN
        elif order_type == "Sell":
            action = mt5.TRADE_ACTION_DEAL
            order_type = mt5.ORDER_TYPE_SELL
            price = mt5.symbol_info_tick(symbol).bid
            type_filling = mt5.ORDER_FILLING_RETURN
        elif order_type == "Buy Limit":
            action = mt5.TRADE_ACTION_PENDING
            order_type = mt5.ORDER_TYPE_BUY_LIMIT
            type_filling = mt5.ORDER_FILLING_FOK
        elif order_type == "Sell Limit":
            action = mt5.TRADE_ACTION_PENDING
            order_type = mt5.ORDER_TYPE_SELL_LIMIT
            type_filling = mt5.ORDER_FILLING_FOK

        # request = {
        # "action": action,
        # "symbol": symbol,
        # "volume": lot,
        # "type": order_type,
        # "price": price,
        # "sl": sl,
        # "tp": tp,
        # "deviation": 20,
        # "magic": 234000,
        # "comment": comment,
        # "type_time": mt5.ORDER_TIME_GTC,
        # "type_filling": type_filling
        # }
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
            "comment": "mt5 asistant",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": type_filling
            }        
        return mt5.order_send(request)
    
if __name__ == '__main__':
    app = TradingApp()
    app.mainloop()
