"""Shopping list UI components."""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from src import list as list_mod


def attach_list_panel(parent, app):
    """Create and attach the shopping list panel to the parent frame.

    Attaches list-related handlers to the `app` instance and provides
    helper functions that operate on the app's widgets/state.
    Returns the left frame.
    """
    left = ttk.Frame(parent)
    left.columnconfigure(0, weight=1)
    left.rowconfigure(1, weight=1)

    # Lists label
    lbl_lists = ttk.Label(left, text="Listas (compartilhadas entre todos)")
    lbl_lists.grid(row=0, column=0, sticky="w")

    # Lists listbox
    lbx_lists = tk.Listbox(left, exportselection=False)
    lbx_lists.grid(row=1, column=0, sticky="nsew")

    # Button frame
    lists_btns = ttk.Frame(left)
    lists_btns.grid(row=2, column=0, sticky="ew", pady=5)
    lists_btns.columnconfigure(2, weight=1)

    # Create/Remove/Refresh buttons (commands attached later)
    btn_create_list = ttk.Button(lists_btns, text="Criar lista", state=tk.DISABLED)
    btn_create_list.grid(row=0, column=0)

    btn_remove_list = ttk.Button(lists_btns, text="Remover lista", state=tk.DISABLED)
    btn_remove_list.grid(row=0, column=1, padx=5)

    btn_refresh_lists = ttk.Button(lists_btns, text="Atualizar", state=tk.DISABLED)
    btn_refresh_lists.grid(row=0, column=2, padx=5, sticky="w")

    # Attach widgets to app instance
    app.lbx_lists = lbx_lists
    app.btn_create_list = btn_create_list
    app.btn_remove_list = btn_remove_list
    app.btn_refresh_lists = btn_refresh_lists

    # --- Helper functions bound to the app instance ---
    def _refresh_lists(_event=None):
        if not getattr(app, "user", None):
            return
        res = list_mod.get_lists_for_user(app.user["id"])
        app.lbx_lists.delete(0, tk.END)
        for l in res["shared"]:
            name = l.get("name", "")
            app.lbx_lists.insert(tk.END, f"id={l['id']} name={name}")
        app.selected_list_id = None
        # if refresh_items exists, call it
        try:
            app.refresh_items()
        except Exception:
            pass

    def _parse_selected_list_id():
        sel = app.lbx_lists.curselection()
        if not sel:
            return None
        text = app.lbx_lists.get(sel[0])
        try:
            part = text.split("id=")[1]
            list_id = int(part.split()[0])
            return list_id
        except Exception:
            return None

    def _create_list(_event=None):
        if not app.require_login():
            return
        name = simpledialog.askstring("Nome da lista", "Nome da nova lista:", parent=app.master)
        if not name or not name.strip():
            messagebox.showwarning("Nome inválido", "Informe um nome para a lista.")
            return
        lid = list_mod.create_list(name.strip())
        app.set_status(f"Lista criada id={lid} name={name.strip()}")
        _refresh_lists()

    def _remove_list(_event=None):
        if not app.require_login():
            return
        lid = _parse_selected_list_id()
        if not lid:
            messagebox.showinfo("Seleção necessária", "Selecione uma lista para remover.")
            return
        if messagebox.askyesno("Confirmar", f"Remover lista id={lid}? Isto excluirá também os itens."):
            list_mod.remove_list(lid)
            app.set_status("Lista removida")
            _refresh_lists()

    # Bindings
    app.parse_selected_list_id = _parse_selected_list_id
    app.refresh_lists = _refresh_lists
    app.create_list = _create_list
    app.remove_list = _remove_list

    # wire buttons/listbox to these handlers
    # when a list is selected, update selected_list_id and refresh items panel
    app.lbx_lists.bind(
        "<<ListboxSelect>>",
        lambda e: (setattr(app, "selected_list_id", _parse_selected_list_id()), app.refresh_items())[1],
    )
    app.btn_create_list.configure(command=app.create_list)
    app.btn_remove_list.configure(command=app.remove_list)
    app.btn_refresh_lists.configure(command=app.refresh_lists)

    return left
