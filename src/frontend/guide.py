import tkinter as tk

import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class Guide:

    def center_window(self, window, width, height):
        window.update_idletasks()

        x = (window.winfo_screenwidth() - width) // 2
        y = (window.winfo_screenheight() - height) // 2

        window.geometry(f"{width}x{height}+{x}+{y}")

    def show_guide(self):

        win = ttk.Toplevel(self)

        win.title("User Guide")

        self.center_window(win, 760, 540)

        win.resizable(False, False)
        win.grab_set()

        frame = ttk.Frame(win, padding=15)
        frame.pack(fill=BOTH, expand=True)

        ttk.Label(
            frame,
            text="راهنمای استفاده",
            font=("Tahoma", 13, "bold"),
            bootstyle="primary"
        ).pack(anchor="e", pady=(0, 10))

        text = tk.Text(
            frame,
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
            spacing1=5,
            spacing3=8
        )
        RLM = "\u200F"
        guide = f"""در حال آماده سازی...
"""

        text.insert("1.0", guide, "rtl")

        text.config(state="disabled")