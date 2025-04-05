import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os

# File to store inventory and users
INVENTORY_FILE = "inventory.json"
USERS_FILE = "users.json"
LOW_STOCK_THRESHOLD = 5

########### Helper Functions ###########

def load_data(file_path, default_data):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        return default_data

def save_data(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

########### Authentication #############

def login_screen():
    def attempt_login():
        username = entry_user.get()
        password = entry_pass.get()
        users = load_data(USERS_FILE, {})
        if username in users and users[username] == password:
            login_window.destroy()
            InventoryApp(username)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials!")

    login_window = tk.Tk()
    login_window.title("Login")

    tk.Label(login_window, text="Username:").grid(row=0, column=0, padx=10, pady=10)
    entry_user = tk.Entry(login_window)
    entry_user.grid(row=0, column=1)

    tk.Label(login_window, text="Password:").grid(row=1, column=0, padx=10, pady=10)
    entry_pass = tk.Entry(login_window, show="*")
    entry_pass.grid(row=1, column=1)

    tk.Button(login_window, text="Login", command=attempt_login).grid(row=2, column=0, columnspan=2, pady=10)
    login_window.mainloop()

############### GUI Class ##############

class InventoryApp:
    def __init__(self, username):
        self.username = username
        self.inventory = load_data(INVENTORY_FILE, {})
        self.window = tk.Tk()
        self.window.title(f"Inventory Manager - Logged in as {username}")

        self.setup_gui()
        self.refresh_inventory_list()
        self.window.mainloop()

    def setup_gui(self):
        # Inventory Treeview
        self.tree = ttk.Treeview(self.window, columns=('Name', 'Quantity', 'Price'), show='headings')
        for col in ('Name', 'Quantity', 'Price'):
            self.tree.heading(col, text=col)
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Buttons
        button_frame = tk.Frame(self.window)
        button_frame.pack()

        tk.Button(button_frame, text="Add Product", command=self.add_product).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Edit Product", command=self.edit_product).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Delete Product", command=self.delete_product).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Low Stock Report", command=self.low_stock_report).grid(row=0, column=3, padx=5)

    def refresh_inventory_list(self):
        self.tree.delete(*self.tree.get_children())
        for pid, data in self.inventory.items():
            self.tree.insert('', 'end', iid=pid, values=(data['name'], data['quantity'], f"${data['price']:0.2f}"))

    def add_product(self):
        self.product_form("Add Product")

    def edit_product(self):
        selected = self.tree.focus()
        if selected:
            self.product_form("Edit Product", selected)
        else:
            messagebox.showwarning("No Selection", "Select a product to edit.")

    def delete_product(self):
        selected = self.tree.focus()
        if selected:
            confirm = messagebox.askyesno("Confirm Delete", "Are you sure?")
            if confirm:
                self.inventory.pop(selected)
                save_data(self.inventory, INVENTORY_FILE)
                self.refresh_inventory_list()

    def product_form(self, title, product_id=None):
        def save():
            name = entry_name.get()
            try:
                quantity = int(entry_quantity.get())
                price = float(entry_price.get())
            except ValueError:
                messagebox.showerror("Invalid Input", "Quantity must be an integer and price a number.")
                return

            if not name:
                messagebox.showerror("Invalid Input", "Product name cannot be empty.")
                return

            if product_id:
                self.inventory[product_id] = {'name': name, 'quantity': quantity, 'price': price}
            else:
                new_id = str(max([int(k) for k in self.inventory.keys()] + [0]) + 1)
                self.inventory[new_id] = {'name': name, 'quantity': quantity, 'price': price}

            save_data(self.inventory, INVENTORY_FILE)
            self.refresh_inventory_list()
            form.destroy()

        form = tk.Toplevel(self.window)
        form.title(title)

        tk.Label(form, text="Product Name:").grid(row=0, column=0, padx=10, pady=5)
        entry_name = tk.Entry(form)
        entry_name.grid(row=0, column=1)

        tk.Label(form, text="Quantity:").grid(row=1, column=0, padx=10, pady=5)
        entry_quantity = tk.Entry(form)
        entry_quantity.grid(row=1, column=1)

        tk.Label(form, text="Price:").grid(row=2, column=0, padx=10, pady=5)
        entry_price = tk.Entry(form)
        entry_price.grid(row=2, column=1)

        if product_id:
            product = self.inventory[product_id]
            entry_name.insert(0, product['name'])
            entry_quantity.insert(0, str(product['quantity']))
            entry_price.insert(0, str(product['price']))

        tk.Button(form, text="Save", command=save).grid(row=3, column=0, columnspan=2, pady=10)

    def low_stock_report(self):
        low_stock_items = [
            f"{data['name']} (Qty: {data['quantity']})"
            for data in self.inventory.values()
            if data['quantity'] <= LOW_STOCK_THRESHOLD
        ]
        report = "\n".join(low_stock_items) if low_stock_items else "All stock levels are sufficient."
        messagebox.showinfo("Low Stock Report", report)

################# Default User Setup #################

def setup_default_user():
    if not os.path.exists(USERS_FILE):
        save_data({'admin': 'admin123'}, USERS_FILE)

############### Run App ####################

if __name__ == "__main__":
    setup_default_user()
    login_screen()
