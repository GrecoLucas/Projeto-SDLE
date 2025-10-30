import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from src import client, list as list_mod, item as item_mod


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

        # top bar (login/user)
        top = ttk.Frame(self)
        top.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        top.columnconfigure(2, weight=1)

        self.lbl_user = ttk.Label(top, text="Não autenticado")
        self.lbl_user.grid(row=0, column=0, padx=(0, 10))

        self.entry_name = ttk.Entry(top, width=24)
        self.entry_name.insert(0, "Seu nome")
        self.entry_name.grid(row=0, column=1)

        self.btn_login = ttk.Button(top, text="Entrar", command=self.on_login)
        self.btn_login.grid(row=0, column=2, padx=10, sticky="w")

        self.btn_logout = ttk.Button(top, text="Sair", command=self.on_logout, state=tk.DISABLED)
        self.btn_logout.grid(row=0, column=3)

        # main split: lists (left) | items (right)
        main = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # left panel: lists
        left = ttk.Frame(main)
        left.columnconfigure(0, weight=1)
        left.rowconfigure(1, weight=1)

        lbl_lists = ttk.Label(left, text="Listas (minhas e compartilhadas)")
        lbl_lists.grid(row=0, column=0, sticky="w")

        self.lbx_lists = tk.Listbox(left, exportselection=False)
        self.lbx_lists.grid(row=1, column=0, sticky="nsew")
        self.lbx_lists.bind("<<ListboxSelect>>", self.on_select_list)

        lists_btns = ttk.Frame(left)
        lists_btns.grid(row=2, column=0, sticky="ew", pady=5)
        lists_btns.columnconfigure(2, weight=1)

        self.btn_create_list = ttk.Button(lists_btns, text="Criar lista", command=self.create_list, state=tk.DISABLED)
        self.btn_create_list.grid(row=0, column=0)

        self.btn_remove_list = ttk.Button(lists_btns, text="Remover lista", command=self.remove_list, state=tk.DISABLED)
        self.btn_remove_list.grid(row=0, column=1, padx=5)

        main.add(left, weight=1)

        # right panel: items
        right = ttk.Frame(main)
        right.columnconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)

        lbl_items = ttk.Label(right, text="Itens da lista selecionada")
        lbl_items.grid(row=0, column=0, sticky="w")

        self.tree = ttk.Treeview(right, columns=("name", "checked", "target", "acquired"), show="headings", selectmode="browse")
        self.tree.heading("name", text="Nome")
        self.tree.heading("checked", text="Marcado")
        self.tree.heading("target", text="Desejado")
        self.tree.heading("acquired", text="Adquirido")
        self.tree.column("name", width=250)
        self.tree.column("checked", width=80, anchor="center")
        self.tree.column("target", width=80, anchor="center")
        self.tree.column("acquired", width=90, anchor="center")
        self.tree.grid(row=1, column=0, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self.on_select_item)

        items_controls = ttk.Frame(right)
        items_controls.grid(row=2, column=0, sticky="ew", pady=5)
        items_controls.columnconfigure(6, weight=1)

        ttk.Label(items_controls, text="Nome:").grid(row=0, column=0, padx=(0, 5))
        self.entry_item_name = ttk.Entry(items_controls, width=24)
        self.entry_item_name.grid(row=0, column=1)

        ttk.Label(items_controls, text="Qtd. desejada:").grid(row=0, column=2, padx=(10, 5))
        self.sp_target = ttk.Spinbox(items_controls, from_=1, to=999, width=5)
        self.sp_target.set("1")
        self.sp_target.grid(row=0, column=3)

        self.btn_add_item = ttk.Button(items_controls, text="Adicionar", command=self.add_item, state=tk.DISABLED)
        self.btn_add_item.grid(row=0, column=4, padx=5)

        self.btn_remove_item = ttk.Button(items_controls, text="Remover", command=self.remove_item, state=tk.DISABLED)
        self.btn_remove_item.grid(row=0, column=5, padx=5)

        ttk.Label(items_controls, text="Qtd. adquirida:").grid(row=0, column=6, padx=(10, 5), sticky="e")
        self.sp_acquired = ttk.Spinbox(items_controls, from_=0, to=999, width=5, state="disabled")
        self.sp_acquired.grid(row=0, column=7)

        self.btn_set_acquired = ttk.Button(items_controls, text="Atualizar", command=self.set_acquired, state=tk.DISABLED)
        self.btn_set_acquired.grid(row=0, column=8, padx=5)

        self.btn_toggle = ttk.Button(items_controls, text="Alternar marcado", command=self.toggle_item, state=tk.DISABLED)
        self.btn_toggle.grid(row=0, column=9, padx=5)

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

    def refresh_lists(self):
        if not self.user:
            return
        res = list_mod.get_lists_for_user(self.user["id"])
        self.lbx_lists.delete(0, tk.END)
        # add owned
        for l in res["owned"]:
            self.lbx_lists.insert(tk.END, f"[OWN] id={l['id']} owner={l['owner_id']}")
            self.lbx_lists.itemconfig(tk.END, foreground="#1f6feb")
        # add shared
        for l in res["shared"]:
            self.lbx_lists.insert(tk.END, f"[SHR] id={l['id']} owner={l['owner_id']}")
        self.selected_list_id = None
        self.refresh_items()

    def parse_selected_list_id(self):
        sel = self.lbx_lists.curselection()
        if not sel:
            return None
        text = self.lbx_lists.get(sel[0])
        try:
            # text like: [OWN] id=3 owner=1
            part = text.split("id=")[1]
            list_id = int(part.split()[0])
            return list_id
        except Exception:
            return None

    def refresh_items(self):
        # clear tree
        for i in self.tree.get_children():
            self.tree.delete(i)
        if not self.selected_list_id:
            self.enable_item_controls(False)
            return
        items = item_mod.list_items(self.selected_list_id)
        for it in items:
            self.tree.insert("", tk.END, iid=str(it["id"]), values=(
                it["name"],
                "✔" if it["checked"] else "",
                it["target_quantity"],
                it["acquired_quantity"],
            ))
        self.enable_item_controls(True)
        self.selected_item_id = None

    def enable_item_controls(self, enabled: bool):
        state = tk.NORMAL if enabled else tk.DISABLED
        self.entry_item_name.configure(state=state)
        self.sp_target.configure(state=state)
        self.btn_add_item.configure(state=state)
        self.btn_remove_item.configure(state=state if self.selected_item_id else tk.DISABLED)
        self.btn_toggle.configure(state=state if self.selected_item_id else tk.DISABLED)
        self.sp_acquired.configure(state=state if self.selected_item_id else tk.DISABLED)
        self.btn_set_acquired.configure(state=state if self.selected_item_id else tk.DISABLED)

    # ---------- callbacks ----------
    def on_login(self):
        name = self.entry_name.get().strip()
        if not name:
            messagebox.showwarning("Nome inválido", "Digite um nome de usuário.")
            return
        self.user = client.get_or_create_user(name)
        self.lbl_user.configure(text=f"Usuário: {self.user['name']} (id={self.user['id']})")
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, "")
        self.btn_login.configure(state=tk.DISABLED)
        self.btn_logout.configure(state=tk.NORMAL)
        self.btn_create_list.configure(state=tk.NORMAL)
        self.btn_remove_list.configure(state=tk.NORMAL)
        self.set_status("Login realizado")
        self.refresh_lists()

    def on_logout(self):
        self.user = None
        self.lbl_user.configure(text="Não autenticado")
        self.btn_login.configure(state=tk.NORMAL)
        self.btn_logout.configure(state=tk.DISABLED)
        self.btn_create_list.configure(state=tk.DISABLED)
        self.btn_remove_list.configure(state=tk.DISABLED)
        self.lbx_lists.delete(0, tk.END)
        self.selected_list_id = None
        self.refresh_items()
        self.set_status("Sessão encerrada")

    def on_select_list(self, _event=None):
        self.selected_list_id = self.parse_selected_list_id()
        self.refresh_items()

    def on_select_item(self, _event=None):
        sel = self.tree.selection()
        self.selected_item_id = int(sel[0]) if sel else None
        # update controls
        has = self.selected_item_id is not None
        self.btn_remove_item.configure(state=(tk.NORMAL if has else tk.DISABLED))
        self.btn_toggle.configure(state=(tk.NORMAL if has else tk.DISABLED))
        self.sp_acquired.configure(state=(tk.NORMAL if has else tk.DISABLED))
        self.btn_set_acquired.configure(state=(tk.NORMAL if has else tk.DISABLED))
        if has:
            vals = self.tree.item(sel[0], "values")
            # values: name, checked, target, acquired
            try:
                self.sp_acquired.set(str(vals[3]))
            except Exception:
                pass

    def create_list(self):
        if not self.require_login():
            return
        name = simpledialog.askstring("Nome da lista", "Nome da nova lista:", parent=self.master)
        if not name or not name.strip():
            messagebox.showwarning("Nome inválido", "Informe um nome para a lista.")
            return
        lid = list_mod.create_list(self.user["id"], name.strip())
        self.set_status(f"Lista criada id={lid} name={name.strip()}")
        self.refresh_lists()

    def remove_list(self):
        if not self.require_login():
            return
        lid = self.parse_selected_list_id()
        if not lid:
            messagebox.showinfo("Seleção necessária", "Selecione uma lista para remover.")
            return
        if messagebox.askyesno("Confirmar", f"Remover lista id={lid}? Isto excluirá também os itens."):
            list_mod.remove_list(lid)
            self.set_status("Lista removida")
            self.refresh_lists()

    def add_item(self):
        if not self.selected_list_id:
            messagebox.showinfo("Seleção necessária", "Selecione uma lista.")
            return
        name = self.entry_item_name.get().strip()
        if not name:
            messagebox.showwarning("Nome inválido", "Informe um nome para o item.")
            return
        try:
            target = int(self.sp_target.get())
        except Exception:
            target = 1
        iid = item_mod.add_item(self.selected_list_id, name, target)
        self.entry_item_name.delete(0, tk.END)
        self.sp_target.set("1")
        self.set_status(f"Item adicionado id={iid}")
        self.refresh_items()

    def remove_item(self):
        if not self.selected_item_id:
            return
        if messagebox.askyesno("Confirmar", f"Remover item id={self.selected_item_id}?"):
            item_mod.remove_item(self.selected_item_id)
            self.set_status("Item removido")
            self.refresh_items()

    def toggle_item(self):
        if not self.selected_item_id:
            return
        ok = item_mod.toggle_checked(self.selected_item_id)
        if ok:
            self.set_status("Item alternado")
        else:
            self.set_status("Item não encontrado")
        self.refresh_items()

    def set_acquired(self):
        if not self.selected_item_id:
            return
        try:
            acquired = int(self.sp_acquired.get())
        except Exception:
            acquired = 0
        item_mod.set_acquired(self.selected_item_id, acquired)
        self.set_status("Quantidade atualizada")
        self.refresh_items()


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
