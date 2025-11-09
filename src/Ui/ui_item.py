"""Shopping list items UI components."""
import tkinter as tk
from tkinter import ttk, messagebox
from src import item as item_mod


def attach_item_panel(parent, app):
    """Create and attach the items panel to the parent frame.
    
    Args:
        parent: Parent tkinter widget
        app: App instance to attach widgets to
        
    Returns:
        The right frame containing item controls
    """
    right = ttk.Frame(parent)
    right.columnconfigure(0, weight=1)
    right.rowconfigure(1, weight=1)

    # Items label
    lbl_items = ttk.Label(right, text="Itens da lista selecionada")
    lbl_items.grid(row=0, column=0, sticky="w")

    # Items treeview
    tree = ttk.Treeview(
        right, 
        columns=("name", "checked", "target", "acquired"), 
        show="headings", 
        selectmode="browse"
    )
    tree.heading("name", text="Nome")
    tree.heading("checked", text="Marcado")
    tree.heading("target", text="Desejado")
    tree.heading("acquired", text="Adquirido")
    tree.column("name", width=250)
    tree.column("checked", width=80, anchor="center")
    tree.column("target", width=80, anchor="center")
    tree.column("acquired", width=90, anchor="center")
    tree.grid(row=1, column=0, sticky="nsew")

    # Item controls frame
    items_controls = ttk.Frame(right)
    items_controls.grid(row=2, column=0, sticky="ew", pady=5)
    items_controls.columnconfigure(6, weight=1)

    # Name entry
    ttk.Label(items_controls, text="Nome:").grid(row=0, column=0, padx=(0, 5))
    entry_item_name = ttk.Entry(items_controls, width=24)
    entry_item_name.grid(row=0, column=1)

    # Target quantity spinbox
    ttk.Label(items_controls, text="Qtd. desejada:").grid(row=0, column=2, padx=(10, 5))
    sp_target = ttk.Spinbox(items_controls, from_=1, to=999, width=5)
    sp_target.set("1")
    sp_target.grid(row=0, column=3)

    # Add item button
    btn_add_item = ttk.Button(
        items_controls,
        text="Adicionar",
        state=tk.DISABLED,
    )
    btn_add_item.grid(row=0, column=4, padx=5)

    # Remove item button
    btn_remove_item = ttk.Button(
        items_controls,
        text="Remover",
        state=tk.DISABLED,
    )
    btn_remove_item.grid(row=0, column=5, padx=5)

    # Acquired quantity spinbox
    ttk.Label(items_controls, text="Qtd. adquirida:").grid(row=0, column=6, padx=(10, 5), sticky="e")
    sp_acquired = ttk.Spinbox(items_controls, from_=0, to=999, width=5, state="disabled")
    sp_acquired.grid(row=0, column=7)

    # Set acquired button
    btn_set_acquired = ttk.Button(
        items_controls,
        text="Atualizar",
        state=tk.DISABLED,
    )
    btn_set_acquired.grid(row=0, column=8, padx=5)

    # Toggle checked button
    btn_toggle = ttk.Button(
        items_controls,
        text="Alternar marcado",
        state=tk.DISABLED,
    )
    btn_toggle.grid(row=0, column=9, padx=5)

    # --- Item-related helper functions attached to app ---
    def _refresh_items(_event=None):
        # clear tree
        for i in app.tree.get_children():
            app.tree.delete(i)
        if not getattr(app, "selected_list_id", None):
            try:
                app.enable_item_controls(False)
            except Exception:
                pass
            return
        items = item_mod.list_items(app.selected_list_id)
        for it in items:
            app.tree.insert("", tk.END, iid=str(it["id"]), values=(
                it["name"],
                "✔" if it["checked"] else "",
                it["target_quantity"],
                it["acquired_quantity"],
            ))
        try:
            app.enable_item_controls(True)
        except Exception:
            pass
        app.selected_item_id = None

    def _enable_item_controls(enabled: bool):
        state = tk.NORMAL if enabled else tk.DISABLED
        app.entry_item_name.configure(state=state)
        app.sp_target.configure(state=state)
        app.btn_add_item.configure(state=state)
        app.btn_remove_item.configure(state=state if getattr(app, "selected_item_id", None) else tk.DISABLED)
        app.btn_toggle.configure(state=state if getattr(app, "selected_item_id", None) else tk.DISABLED)
        app.sp_acquired.configure(state=state if getattr(app, "selected_item_id", None) else tk.DISABLED)
        app.btn_set_acquired.configure(state=state if getattr(app, "selected_item_id", None) else tk.DISABLED)

    def _on_select_item(_event=None):
        sel = app.tree.selection()
        app.selected_item_id = int(sel[0]) if sel else None
        has = app.selected_item_id is not None
        app.btn_remove_item.configure(state=(tk.NORMAL if has else tk.DISABLED))
        app.btn_toggle.configure(state=(tk.NORMAL if has else tk.DISABLED))
        app.sp_acquired.configure(state=(tk.NORMAL if has else tk.DISABLED))
        app.btn_set_acquired.configure(state=(tk.NORMAL if has else tk.DISABLED))
        if has:
            vals = app.tree.item(sel[0], "values")
            try:
                app.sp_acquired.set(str(vals[3]))
            except Exception:
                pass

    def _add_item(_event=None):
        if not getattr(app, "selected_list_id", None):
            messagebox.showinfo("Seleção necessária", "Selecione uma lista.")
            return
        name = app.entry_item_name.get().strip()
        if not name:
            messagebox.showwarning("Nome inválido", "Informe um nome para o item.")
            return
        try:
            target = int(app.sp_target.get())
        except Exception:
            target = 1
        iid = item_mod.add_item(app.selected_list_id, name, target)
        app.entry_item_name.delete(0, tk.END)
        app.sp_target.set("1")
        app.set_status(f"Item adicionado id={iid}")
        _refresh_items()

    def _remove_item(_event=None):
        if not getattr(app, "selected_item_id", None):
            return
        if messagebox.askyesno("Confirmar", f"Remover item id={app.selected_item_id}?"):
            item_mod.remove_item(app.selected_item_id)
            app.set_status("Item removido")
            _refresh_items()

    def _toggle_item(_event=None):
        if not getattr(app, "selected_item_id", None):
            return
        ok = item_mod.toggle_checked(app.selected_item_id)
        if ok:
            app.set_status("Item alternado")
        else:
            app.set_status("Item não encontrado")
        _refresh_items()

    def _set_acquired(_event=None):
        if not getattr(app, "selected_item_id", None):
            return
        try:
            acquired = int(app.sp_acquired.get())
        except Exception:
            acquired = 0
        item_mod.set_acquired(app.selected_item_id, acquired)
        app.set_status("Quantidade atualizada")
        _refresh_items()

    # attach handlers to app
    app.refresh_items = _refresh_items
    app.enable_item_controls = _enable_item_controls
    app.on_select_item = _on_select_item
    app.add_item = _add_item
    app.remove_item = _remove_item
    app.toggle_item = _toggle_item
    app.set_acquired = _set_acquired

    # bind tree selection now that handler exists
    tree.bind("<<TreeviewSelect>>", app.on_select_item)

    # wire buttons to handlers
    btn_add_item.configure(command=app.add_item)
    btn_remove_item.configure(command=app.remove_item)
    btn_set_acquired.configure(command=app.set_acquired)
    btn_toggle.configure(command=app.toggle_item)

    # Attach widgets to app instance
    app.tree = tree
    app.entry_item_name = entry_item_name
    app.sp_target = sp_target
    app.btn_add_item = btn_add_item
    app.btn_remove_item = btn_remove_item
    app.sp_acquired = sp_acquired
    app.btn_set_acquired = btn_set_acquired
    app.btn_toggle = btn_toggle

    return right
