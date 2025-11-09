import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from src import client, list as list_mod, item as item_mod
from .ui_user import attach_user_bar
from .ui_list import attach_list_panel
from .ui_item import attach_item_panel


class App(ttk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)

        # state
        self.user = None  # dict: {id, name}
        self.selected_list_id = None
        self.selected_item_id = None

        # UI
        self._build_ui()

    # ---------- UI building ----------
    def _build_ui(self):
        self.master.title("Shopping List - Tkinter")
        self.master.geometry("900x550")
        self.master.minsize(780, 500)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # top bar (login/user) - delegated to ui_user module
        top = attach_user_bar(self, self)
        top.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        # main split: lists (left) | items (right)
        main = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # left panel: lists - delegated to ui_list module
        left = attach_list_panel(main, self)
        main.add(left, weight=1)

        # right panel: items - delegated to ui_item module
        right = attach_item_panel(main, self)
        main.add(right, weight=2)

        # status bar
        self.status = tk.StringVar(value="Pronto")
        bar = ttk.Label(self, textvariable=self.status, relief=tk.SUNKEN, anchor="w")
        bar.grid(row=2, column=0, sticky="ew", padx=0, pady=0)

    # ---------- helper methods ----------
    def set_status(self, msg: str):
        self.status.set(msg)
        self.master.after(4000, lambda: self.status.set("Pronto"))

    def require_login(self) -> bool:
        if not self.user:
            messagebox.showwarning("Login necessário", "Entre com um nome para continuar.")
            return False
        return True


def start_ui():
    root = tk.Tk()
    # use ttk theme if available
    try:
        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")
    except Exception:
        pass
    App(root)
    root.mainloop()
