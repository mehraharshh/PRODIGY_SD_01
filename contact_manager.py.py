import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

CONTACTS_FILE = "contacts.json"

class ContactManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📇 Contact Manager")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.contacts = self.load_contacts()
        self.create_gui()

    def load_contacts(self):
        if os.path.exists(CONTACTS_FILE):
            with open(CONTACTS_FILE, "r") as f:
                return json.load(f)
        return []

    def save_contacts(self):
        with open(CONTACTS_FILE, "w") as f:
            json.dump(self.contacts, f, indent=4)

    def create_gui(self):
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10))

        # Treeview (Table)
        columns = ("Name", "Phone", "Email")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=12)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=180)
        self.tree.pack(pady=10)

        self.load_tree_data()

        # Buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="➕ Add Contact", command=self.add_contact).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="✏️ Edit Contact", command=self.edit_contact).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="❌ Delete Contact", command=self.delete_contact).grid(row=0, column=2, padx=10)
        ttk.Button(btn_frame, text="🔄 Refresh", command=self.refresh_tree).grid(row=0, column=3, padx=10)

    def load_tree_data(self):
        for contact in self.contacts:
            self.tree.insert("", "end", values=(contact["name"], contact["phone"], contact["email"]))

    def refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.load_tree_data()

    def get_selected_index(self):
        selected = self.tree.selection()
        if not selected:
            return None
        values = self.tree.item(selected[0])["values"]
        for index, contact in enumerate(self.contacts):
            if contact["name"] == values[0] and contact["phone"] == values[1] and contact["email"] == values[2]:
                return index
        return None

    def add_contact(self):
        self.open_contact_window("Add Contact")

    def edit_contact(self):
        index = self.get_selected_index()
        if index is None:
            messagebox.showwarning("No Selection", "Please select a contact to edit.")
            return
        self.open_contact_window("Edit Contact", self.contacts[index], index)

    def delete_contact(self):
        index = self.get_selected_index()
        if index is None:
            messagebox.showwarning("No Selection", "Please select a contact to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Delete '{self.contacts[index]['name']}'?")
        if confirm:
            del self.contacts[index]
            self.save_contacts()
            self.refresh_tree()
            messagebox.showinfo("Deleted", "Contact deleted.")

    def open_contact_window(self, title, contact=None, index=None):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("350x220")
        window.resizable(False, False)

        ttk.Label(window, text="Name:").pack(pady=(20, 5))
        name_entry = ttk.Entry(window, width=35)
        name_entry.pack()

        ttk.Label(window, text="Phone:").pack(pady=(10, 5))
        phone_entry = ttk.Entry(window, width=35)
        phone_entry.pack()

        ttk.Label(window, text="Email:").pack(pady=(10, 5))
        email_entry = ttk.Entry(window, width=35)
        email_entry.pack()

        if contact:
            name_entry.insert(0, contact["name"])
            phone_entry.insert(0, contact["phone"])
            email_entry.insert(0, contact["email"])

        def submit():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            email = email_entry.get().strip()

            if not name or not phone or not email:
                messagebox.showwarning("Input Error", "All fields are required.")
                return

            new_contact = {"name": name, "phone": phone, "email": email}
            if index is None:
                self.contacts.append(new_contact)
                messagebox.showinfo("Added", "Contact added.")
            else:
                self.contacts[index] = new_contact
                messagebox.showinfo("Updated", "Contact updated.")

            self.save_contacts()
            self.refresh_tree()
            window.destroy()

        ttk.Button(window, text="Save", command=submit).pack(pady=15)

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManagerApp(root)
    root.mainloop()
