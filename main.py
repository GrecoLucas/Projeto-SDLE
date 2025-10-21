from src import db, client, list as list_mod, item as item_mod


def prompt_menu(options):
    for i, (key, desc) in enumerate(options, start=1):
        print(f"{i}. {desc}")
    print("0. Quit")
    choice = input("> ").strip()
    if not choice.isdigit():
        return None
    return int(choice)


def main():
    db.init_db()
    user = None
    while True:
        if not user:
            print("\nLogin: enter your name (no password).")
            name = input("Name: ").strip()
            if not name:
                continue
            user = client.get_or_create_user(name)
            print(f"Logged in as {user['name']} (id={user['id']})")
            continue

        print(f"\nUser: {user['name']} (id={user['id']})")
        options = [
            ("create_list", "Create list"),
            ("remove_list", "Remove list"),
            ("show_lists", "Show my lists"),
            ("add_item", "Add item to list"),
            ("remove_item", "Remove item"),
            ("show_items", "Show items for a list"),
            ("toggle_item", "Toggle item checked"),
            ("logout", "Logout"),
        ]
        choice = prompt_menu(options)
        if choice is None:
            print("Invalid choice")
            continue
        if choice == 0:
            print("Goodbye")
            break

        key = options[choice - 1][0]

        if key == "create_list":
            lid = list_mod.create_list(user['id'])
            print(f"Created list id={lid}")

        elif key == "remove_list":
            lid = input("List id to remove: ").strip()
            if lid.isdigit():
                list_mod.remove_list(int(lid))
                print("Removed (if existed)")

        elif key == "show_lists":
            res = list_mod.get_lists_for_user(user['id'])
            print("Owned:")
            for l in res['owned']:
                print(f" - id={l['id']} owner={l['owner_id']}")
            print("Shared:")
            for l in res['shared']:
                print(f" - id={l['id']} owner={l['owner_id']}")

        elif key == "add_item":
            lid = input("List id: ").strip()
            name = input("Item name: ").strip()
            tq = input("Target quantity (default 1): ").strip()
            tqv = int(tq) if tq.isdigit() else 1
            if lid.isdigit() and name:
                iid = item_mod.add_item(int(lid), name, tqv)
                print(f"Added item id={iid}")

        elif key == "remove_item":
            iid = input("Item id to remove: ").strip()
            if iid.isdigit():
                item_mod.remove_item(int(iid))
                print("Removed (if existed)")

        elif key == "show_items":
            lid = input("List id: ").strip()
            if lid.isdigit():
                items = item_mod.list_items(int(lid))
                for it in items:
                    print(f" - id={it['id']} name={it['name']} checked={it['checked']} target={it['target_quantity']} acquired={it['acquired_quantity']}")

        elif key == "toggle_item":
            iid = input("Item id to toggle: ").strip()
            if iid.isdigit():
                ok = item_mod.toggle_checked(int(iid))
                print("Toggled" if ok else "Item not found")

        elif key == "logout":
            user = None


if __name__ == '__main__':
    main()
