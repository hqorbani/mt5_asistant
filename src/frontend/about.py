import base64
import webbrowser
from io import BytesIO
import tkinter as tk
from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from PIL import Image, ImageTk

from src.frontend.logo_var import logo_base64_v2


class About:

    def center_window(self, window, width, height):
        window.update_idletasks()

        x = (window.winfo_screenwidth() - width) // 2
        y = (window.winfo_screenheight() - height) // 2

        window.geometry(f"{width}x{height}+{x}+{y}")

    def show_about(self):

        win = ttk.Toplevel(self)
        win.title("About MT5 Trade Assistant")

        self.center_window(win, 760, 540)

        win.resizable(False, False)
        win.grab_set()

        main = ttk.Frame(win, padding=15)
        main.pack(fill=BOTH, expand=True)

        left = ttk.Frame(main, width=220)
        left.pack(side=RIGHT, fill=Y)

        ttk.Separator(main, orient=VERTICAL).pack(side=RIGHT, fill=Y, padx=15)

        right = ttk.Frame(main)
        right.pack(side=LEFT, fill=BOTH, expand=True)

        try:
            image_data = base64.b64decode(logo_base64_v2)
            image = Image.open(BytesIO(image_data))
            image = image.resize((180, 180), Image.LANCZOS)

            logo = ImageTk.PhotoImage(image)

            lbl = ttk.Label(left, image=logo)
            lbl.image = logo
            lbl.pack(pady=(10, 15))

        except Exception as e:
            messagebox.showerror("Error", str(e))

        ttk.Label(
            left,
            text="MT5 Trade Assistant",
            font=("Tahoma", 12, "bold")
        ).pack()

        ttk.Label(
            left,
            text="Version 1.0",
            font=("Tahoma", 10)
        ).pack()

        ttk.Label(
            left,
            text="Developer\nHamzeh Qorbani",
            justify="center",
            font=("Tahoma", 10)
        ).pack(pady=10)

        email = ttk.Label(
            left,
            text="h.qorbani7@gmail.com",
            cursor="hand2",
            bootstyle="primary"
        )
        email.pack(pady=5)

        email.bind(
            "<Button-1>",
            lambda e: webbrowser.open("mailto:h.qorbani7@gmail.com")
        )

        ttk.Label(
            left,
            text="+98 905 636 1130",
            font=("Tahoma", 10)
        ).pack()

        text = tk.Text(
            right,
            font=("Tahoma", 10),
            wrap="word",
            relief="flat",
            borderwidth=0,
            padx=10,
            pady=10,
            cursor="arrow"
        )

        text.pack(fill=BOTH, expand=True)

        text.tag_configure(
            "rtl",
            justify="right",
            spacing1=4,
            spacing3=8
        )

        about = """
درباره برنامه

دستیار متاتریدر یک دستیار معاملاتی برای متاتریدر  است که با هدف مدیریت سرمایه و اجرای سریع‌تر سفارش‌ها توسعه یافته است.

این برنامه با دریافت نماد، نوع سفارش، درصد ریسک، قیمت ورود، حد ضرر و حد سود، حجم مناسب معامله، سود و زیان احتمالی، نسبت ریسک به ریوارد و مارجین موردنیاز را به‌صورت خودکار محاسبه می‌کند.

پس از اعتبارسنجی اطلاعات، امکان ارسال مستقیم سفارش به متاتریدر  فراهم می‌شود.

© Hamzeh Qorbani
"""

        text.insert("1.0", about, "rtl")
        text.config(state="disabled")