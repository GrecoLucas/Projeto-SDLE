"""User authentication UI components."""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from src import client


def attach_user_bar(parent, app):
    """Create and attach the user/login bar to the parent frame.

    Attaches login/logout handlers to the `app` instance so `ui_tk` logic
    can remain minimal. Returns the top frame.
    """
    top = ttk.Frame(parent)
    top.columnconfigure(2, weight=1)

    # User label
    lbl_user = ttk.Label(top, text="Não autenticado")
    lbl_user.grid(row=0, column=0, padx=(0, 10))

    # Name entry
    entry_name = ttk.Entry(top, width=24)
    entry_name.insert(0, "Seu nome")
    entry_name.grid(row=0, column=1)

    # We'll assign the commands after we attach helper functions below
    btn_login = ttk.Button(top, text="Entrar")
    btn_login.grid(row=0, column=2, padx=10, sticky="w")

    btn_logout = ttk.Button(top, text="Sair", state=tk.DISABLED)
    btn_logout.grid(row=0, column=3)

    # Attach widgets to app instance
    app.lbl_user = lbl_user
    app.entry_name = entry_name
    app.btn_login = btn_login
    app.btn_logout = btn_logout

    # --- Handlers (bound to the app instance) ---
    def _on_login(_event=None):
        name = app.entry_name.get().strip()
        if not name:
            messagebox.showwarning("Nome inválido", "Digite um nome de usuário.")
            return
        app.user = client.get_or_create_user(name)
        app.lbl_user.configure(text=f"Usuário: {app.user['name']} (id={app.user['id']})")
        app.entry_name.delete(0, tk.END)
        app.entry_name.insert(0, "")
        app.btn_login.configure(state=tk.DISABLED)
        app.btn_logout.configure(state=tk.NORMAL)
        # enable list controls (may be attached by list module)
        try:
            app.btn_create_list.configure(state=tk.NORMAL)
            app.btn_remove_list.configure(state=tk.NORMAL)
            app.btn_refresh_lists.configure(state=tk.NORMAL)
        except Exception:
            pass
        app.set_status("Login realizado")
        # refresh lists if the function is attached
        try:
            app.refresh_lists()
        except Exception:
            pass

    def _on_logout(_event=None):
        app.user = None
        app.lbl_user.configure(text="Não autenticado")
        app.btn_login.configure(state=tk.NORMAL)
        app.btn_logout.configure(state=tk.DISABLED)
        try:
            app.btn_create_list.configure(state=tk.DISABLED)
            app.btn_remove_list.configure(state=tk.DISABLED)
            app.btn_refresh_lists.configure(state=tk.DISABLED)
        except Exception:
            pass
        try:
            app.lbx_lists.delete(0, tk.END)
        except Exception:
            pass
        app.selected_list_id = None
        try:
            app.refresh_items()
        except Exception:
            pass
        app.set_status("Sessão encerrada")

    # attach handlers to instance and to buttons
    app.on_login = _on_login
    app.on_logout = _on_logout
    app.btn_login.configure(command=app.on_login)
    app.btn_logout.configure(command=app.on_logout)

    return top
