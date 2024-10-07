#################################################################################################################################################################
import tkinter as tk
from tkinter import messagebox
import json
import re

USERS_FILE = "users.json"
CATEGORIES_FILE = "categories.json"
CARTS_FILE = "carts.json"
ADMIN_EMAIL = 'admin@gmail.com'
ADMIN_PASSWORD = 'admin123'

def is_admin(email, password):
    return email == ADMIN_EMAIL and password == ADMIN_PASSWORD

def load_users():
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def is_valid_email(email):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email)

########################Classes for Categories, Items, and Cart#####################################

opened_pages = []
def manage_pages(action):

    global opened_pages
    if action == 'open':
        new_page = tk.Toplevel()
        opened_pages.append(new_page)

       # if len(opened_pages) > 0:
           # back_button = tk.Button(new_page, text="<-", command=lambda: manage_pages('back'))
           # back_button.pack()
    elif action == 'back':
        if len(opened_pages) >= 1:
            current_page = opened_pages.pop() # مسحتها
            current_page.destroy() #قفلت ال page
            previous_page = opened_pages[-1] # جبت ال page الي قبلها
            previous_page.deiconify()  # Make the previous window visible #مفهمتش gui اكيد
        elif len(opened_pages) < 1:
            messagebox.showinfo("Page", "You can't back any more")
class Category:
    def __init__(self):
        self.categories = self.load_categories()

    def load_categories(self):

        with open(CATEGORIES_FILE, 'r') as file:
            return json.load(file)


    def save_categories(self):
        with open(CATEGORIES_FILE, 'w') as file:
            json.dump(self.categories, file, indent=4)

    def add_category(self, category_name, user_email):
        if not is_admin(user_email, ADMIN_PASSWORD):
            messagebox.showerror("Error", "Only admin can add categories.")
            return
        if category_name in self.categories:
            messagebox.showerror("Error", f"Category {category_name} already exists.")
            return
        self.categories[category_name] = []
        self.save_categories()
        messagebox.showinfo("Success", f"Category {category_name} added successfully.")

    def delete_category(self, user_email):
        if not is_admin(user_email):
            messagebox.showerror("Error", "Only admin can delete categories.")
            return
        if self.category_name not in self.categories:
            messagebox.showerror("Error", f"Category {self.category_name} does not exist")
            return

        del self.categories[self.category_name]  # del بدل ال for loop
        self.save_categories()
        messagebox.showinfo("Success", f"Category {self.category_name} deleted successfully")

    def edit_category(self, old_category_name, new_category_name, admin_email):
        if not is_admin(admin_email, ADMIN_PASSWORD):
            messagebox.showerror("Error", "Only admin can edit categories.")
            return

        if old_category_name not in self.categories:
            messagebox.showerror("Error", f"Category '{old_category_name}' does not exist.")
            return

        if new_category_name in self.categories:
            messagebox.showerror("Error", f"Category '{new_category_name}' already exists.")
            return

        self.categories[new_category_name] = self.categories.pop(old_category_name)
        self.save_categories()
        messagebox.showinfo("Success", f"Category '{old_category_name}' renamed to '{new_category_name}' successfully.")


    def delete_category(self, category_name, admin_email):
        if not is_admin(admin_email, ADMIN_PASSWORD):
            messagebox.showerror("Error", "Only admin can delete categories.")
            return

        if category_name not in self.categories:
            messagebox.showerror("Error", f"Category '{category_name}' does not exist.")
            return

        del self.categories[category_name]
        self.save_categories()
        messagebox.showinfo("Success", f"Category '{category_name}' deleted successfully.")


    def show_categories(self):
        categories_window = tk.Toplevel()
        categories_window.title("Categories")
        if not self.categories:
            tk.Label(categories_window, text="No categories available").pack()
        else:
            tk.Label(categories_window, text="Categories").pack()
            for category_name in self.categories:
                tk.Label(categories_window, text=f"- {category_name}").pack()

        tk.Button(categories_window, text="Close",fg="red", command=categories_window.destroy).pack()


class Item:
    def __init__(self, name=None, price=None, brand=None, model_year=None,discount=0):
        self.categories = self.load_categories()
        self.name = name
        self.price = price
        self.brand = brand
        self.model_year = model_year
        self.discount = discount
        self.click_count = 0
        self.item_labels = []

    def load_categories(self):

        with open(CATEGORIES_FILE, 'r') as file:
            return json.load(file)

    def save_categories(self):
        with open(CATEGORIES_FILE, 'w') as file:
            json.dump(self.categories, file, indent=4)

    def add_item_to_category(self, category_name, admin_email):
        if not is_admin(admin_email, ADMIN_PASSWORD):
            messagebox.showerror("Error", "Only admin can add items.")
            return
        category = Category()
        if category_name not in category.categories:
            messagebox.showerror("Error", f"Category '{category_name}' does not exist.")
            return

        category.categories[category_name].append({
            'name': self.name,
            'price': self.price,
            'brand': self.brand,
            'model_year': self.model_year,
            'discount': self.discount
        })
        category.save_categories()
        messagebox.showinfo("Success", f"Item {self.name} added to {category_name}.")

    def delete_item_from_category(self, category_name, item_name, admin_email):
        if not is_admin(admin_email, ADMIN_PASSWORD):
            messagebox.showerror("Error", "Only admin can delete items from categories.")
            return
        category = Category()
        if category_name not in category.categories:
            messagebox.showerror("Error", f"Category '{category_name}' does not exist.")
            return
        category_items = category.categories[category_name]
        for item in category_items:
            if item['name'] == item_name:
                category_items.remove(item)
                category.save_categories()
                messagebox.showinfo("Success", f"Item {item_name} deleted from {category_name}.")
                return
        messagebox.showerror("Error", f"Item {item_name} not found in category {category_name}.")

    def edit_item(self, category_name, old_item_name, new_name=None, new_price=None, new_brand=None, new_year=None, new_discount = None,
                  admin_email=None):

        if not is_admin(admin_email, ADMIN_PASSWORD):
            messagebox.showerror("Error", "Only admin can edit items.")
            return

        if category_name not in self.categories:
            messagebox.showerror("Error", f"Category '{category_name}' does not exist.")
            return

        category_items = self.categories[category_name]
        item_found = False

        for item in category_items:
            if item['name'] == old_item_name:
                item_found = True
                if new_name is not None:
                    item['name'] = new_name
                if new_price is not None:
                    item['price'] = new_price
                if new_brand is not None:
                    item['brand'] = new_brand
                if new_year is not None:
                    item['model_year'] = new_year
                if new_discount is not None:
                    item['discount'] = new_discount


                self.save_categories()
                messagebox.showinfo("Success", f"Item '{old_item_name}' updated successfully.")
                return

        if not item_found:
            messagebox.showerror("Error", f"Item '{old_item_name}' not found in category '{category_name}'.")

    def quicksort(self, items, sort_by, ascending=True):
        if len(items) <= 1:
            return items

        pivot = items[len(items) // 2]  # Use middle element as pivot
        left = [x for x in items if x[sort_by] < pivot[sort_by]]
        middle = [x for x in items if x[sort_by] == pivot[sort_by]]
        right = [x for x in items if x[sort_by] > pivot[sort_by]]

        if ascending:
            return self.quicksort(left, sort_by, ascending) + middle + self.quicksort(right, sort_by, ascending)
        else:
            return self.quicksort(right, sort_by, ascending) + middle + self.quicksort(left, sort_by, ascending)

    def sort_items(self, category_name, sort_by="name", ascending=True):
        self.categories = self.load_categories()
        items = self.categories[category_name]

        sorted_items = self.quicksort(items, sort_by, ascending)
        self.show_items(category_name, sorted_items)

    def show_items(self, category_name, items):
        category_window = tk.Toplevel()
        category_window.title(f"Items in {category_name}")

        if not items:
            tk.Label(category_window, text="No items in this category yet").pack()
        else:
            for item in items:
                tk.Label(category_window,
                         text=f"{item['name']} \n {item['price']} \n {item['brand']} \n {item['model_year']}").pack()
                if item['discount'] != 0:
                    tk.Label(category_window, text=f"{item['discount']}").pack

        self.click_count += 1

        if self.click_count % 2 == 1:  # odd
            tk.Button(category_window, text="Price",
                      command=lambda: self.sort_items(category_name, "price", ascending=False)).pack()
            tk.Button(category_window, text="Model Year",
                      command=lambda: self.sort_items(category_name, "model_year", ascending=False)).pack()
            tk.Button(category_window, text="Name(Z-A)",
                      command=lambda: self.sort_items(category_name, "name", ascending=False)).pack()
        else:  # even
            tk.Button(category_window, text="Price",
                      command=lambda: self.sort_items(category_name, "price", ascending=True)).pack()
            tk.Button(category_window, text="Model Year",
                      command=lambda: self.sort_items(category_name, "model_year", ascending=True)).pack()
            tk.Button(category_window, text="Name(A-Z)",
                      command=lambda: self.sort_items(category_name, "name", ascending=True)).pack()

        tk.Button(category_window, text="Close", command=category_window.destroy).pack()

    def search(self, category_name, item_name):
        items = Category().categories.get(category_name, [])
        search_item = [item for item in items if item_name.lower() in item['name'].lower()]
        if search_item:
            for item in search_item:
                messagebox.showinfo("Search Results", f"{item['name']} - {item['price']} - {item['brand']} - {item['model_year']} - {item['discount']}")
        else:
            messagebox.showinfo("Search Results", "No items found.")



class Cart:
    def __init__(self, user_email):
        self.user_email = user_email
        self.items = self.load_items()
    def load_items(self):
            try:
                with open(CARTS_FILE, 'r') as f:
                    carts = json.load(f)
                    return carts.get(self.user_email, [])
            except (FileNotFoundError, json.JSONDecodeError):
                return []


    def save_items(self):
        try:
            with open(CARTS_FILE, 'r') as f:
                carts = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            carts = {}

        carts[self.user_email] = self.items
        with open(CARTS_FILE, 'w') as f:
            json.dump(carts, f, indent=4)


    def add_item_to_cart(self, item):
        self.items.append(item)
        self.save_items()
        messagebox.showinfo("Item Added", f"Added {item['name']} to cart.")

    def delete_item_from_cart(self, item_name, cart_window):
        self.items = [item for item in self.items if item['name'] != item_name]
        self.save_items()
        messagebox.showinfo("Item Removed", f"Removed {item_name} from cart.")

        self.display(cart_window)

    def display(self, cart_window):

        if not self.items:
            tk.Label(cart_window, text="Your cart is empty.").pack()
        else:
            for item in self.items:
                tk.Label(cart_window,
                         text=f"{item['name']} - {item['price']} - {item['brand']} - {item['model_year']}").pack()

        tk.Button(cart_window, text="Close", fg="red",font="Bold", command=cart_window.destroy).pack()

    def view_cart(self):
        cart_window = tk.Toplevel()
        cart_window.title(f"Cart for {self.user_email}")
        cart_window.attributes("-fullscreen", True)
        cart_window.configure(bg="lightblue")

        tk.Label(cart_window, text="Search Item:",bg="lightblue",font="Bold").pack(pady=5)
        search_entry = tk.Entry(cart_window)
        search_entry.pack()

        def serch():
            item_name = search_entry.get()
            self.search(item_name)

        tk.Button(cart_window, text="Search",fg="white", width=10,font="Bold",bg="gray", command=serch).pack(pady=5)

        if not self.items:
            tk.Label(cart_window, text="Your cart is empty.").pack()
        else:
            for item in self.items:
                tk.Label(cart_window, text=f"{item['name']} - {item['price']} - {item['brand']} - {item['model_year']} - {item['discount']}").pack(pady=5)
                tk.Button(cart_window, text="Delete",fg="white",font="Bold",bg="gray",command=lambda i=item['name']: self.delete_item_from_cart(i, cart_window)).pack(pady=5)
        tk.Button(cart_window, text="Calculate Total",fg="white",font="Bold",bg="gray", command=lambda: self.calculate_total("Cairo")).pack(pady=5)
        tk.Button(cart_window, text="Close", fg="red",font="Bold", command=cart_window.destroy).pack()

    def calculate_total(self, governorate):
        total = sum(item['price'] for item in self.items)
        delivery_fee = self.calculate_delivery_fee(governorate)
        total_with_delivery = total + delivery_fee
        messagebox.showinfo("Total Cost",
                            f"Total: {total}, Delivery Fee: {delivery_fee}, Total with Delivery: {total_with_delivery}")

    def calculate_delivery_fee(self, governorate):
        fees = {'Cairo': 20, 'Giza': 30, 'Alex': 40}
        return fees.get(governorate, 50)

    def search(self, item_name):
        search_item = [item for item in self.items if item_name.lower() in item['name'].lower()]

        if search_item:
            for item in search_item:
                messagebox.showinfo("Search Results", f"{item['name']} - {item['price']} - {item['brand']} - {item['model_year']} - {item['discount']}")
        else:
            messagebox.showinfo("Search Results", "No items found.")




def login():
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("300x300")
    login_window.configure(bg="lightblue")

    frame = tk.Frame(login_window,bg="lightblue")
    frame.pack(expand=True)

    tk.Label(frame, text="EMAIL",font="Bold",bg="lightblue").pack()
    email_entry = tk.Entry(frame)
    email_entry.pack(padx=10,pady=7)

    tk.Label(frame, text="Password", font="Bold",bg="lightblue").pack()
    password_entry = tk.Entry(frame, show="*")
    password_entry.pack(padx=10,pady=7)

    error_label = tk.Label(frame, text="", fg="red",bg="lightblue")
    error_label.pack()

    def validate_login():
        email = email_entry.get()
        password = password_entry.get()

        if not email or not password:
            error_label.config(text="Email and Password cannot be empty.")
            return

        users = load_users()

        if is_admin(email, password):
            login_window.destroy()
            admin_panel()
        elif email in users and users[email]['password'] == password:
            login_window.destroy()
            user_categories_panel(users[email]["name"], email)
        else:
            error_label.config(text="Invalid email or password.")

    tk.Button(frame, text="Login",font="Bold",fg="white",background="grey", command=validate_login).pack(pady=5)
    tk.Button(frame, text="Register",font="Bold",fg="white",background="grey", command=lambda: [login_window.destroy(), register()]).pack(pady=5)
    tk.Button(frame, text="Exit",fg="red",font="Bold", command=login_window.destroy).pack()

    login_window.mainloop()

def register():
    register_window = tk.Tk()
    register_window.title("Register")
    register_window.geometry("500x500")
    register_window.configure(bg="lightblue")

    frame = tk.Frame(register_window,bg="lightblue")
    frame.pack(expand=True)

    tk.Label(frame, text="Name", font="Bold",bg="lightblue").pack()
    name_entry = tk.Entry(frame)
    name_entry.pack(padx=10,pady=5)

    tk.Label(frame, text="Email", font="Bold",bg="lightblue").pack()
    email_entry = tk.Entry(frame)
    email_entry.pack(padx=10,pady=5)

    tk.Label(frame, text="National ID", font="Bold",bg="lightblue").pack()
    id_entry = tk.Entry(frame)
    id_entry.pack(padx=10,pady=5)

    tk.Label(frame, text="Password", font="Bold",bg="lightblue").pack()
    password_entry = tk.Entry(frame, show="*")
    password_entry.pack(padx=10,pady=5)

    tk.Label(frame, text="Government", font="Bold",bg="lightblue").pack()
    government_entry = tk.Entry(frame)
    government_entry.pack(padx=10,pady=5)

    tk.Label(frame, text="Address", font="Bold",bg="lightblue").pack()
    address_entry = tk.Entry(frame)
    address_entry.pack(padx=10,pady=5)

    tk.Label(frame, text="Phone", font="Bold",bg="lightblue").pack()
    phone_entry = tk.Entry(frame)
    phone_entry.pack(padx=10,pady=5)

    error_label = tk.Label(frame, text="", fg="red",bg="lightblue")
    error_label.pack()

    def save_registration():
        name = name_entry.get()
        email = email_entry.get()
        user_id = id_entry.get()
        password = password_entry.get()
        government = government_entry.get()
        address = address_entry.get()
        phone = phone_entry.get()

        if not (name and email and user_id and password and government and address and phone):
            error_label.config(text="Please fill all fields")
            return

        if not is_valid_email(email):
            error_label.config(text="Invalid email format")
            return

        users = load_users()

        if email in users:
            error_label.config(text="Email already exists")
        else:
            users[email] = {
                "name": name,
                "id": user_id,
                "password": password,
                "government": government,
                "address": address,
                "phone": phone
            }
            save_users(users)
            messagebox.showinfo("Success", "Registration successful")
            register_window.destroy()
            login()

    tk.Button(frame, text="Register",fg="white", width=10,font="Bold",bg="gray", command=save_registration).pack(pady=5)
    tk.Button(frame, text="Cancel", fg="red",font="Bold", command=lambda: [register_window.destroy(), login()]).pack()

    register_window.mainloop()

###############################################################################################
def admin_panel():
    admin_window = tk.Tk()
    admin_window.title("Welcome Admin Panel :)")
    admin_window.attributes("-fullscreen", True)
    admin_window.configure(bg="lightblue")

    tk.Label(admin_window, text="Admin Panel:", font="Arial,20",bg="lightblue",fg="blue").pack()

    category_instance = Category()

    def show_items_window(category_name):
        admin_window.destroy()
        items_window = tk.Tk()
        items_window.title(f"Items in {category_name}")
        items_window.attributes("-fullscreen", True)
        items_window.configure(bg="lightblue")

        refresh_items_window(category_name, items_window)

        items_window.mainloop()

    def go_back_to_admin_panel(current_window):
        current_window.destroy()
        admin_panel()

    def add_category():
        def submit_category():
            category_name = category_name_entry.get()
            category_instance.add_category(category_name, ADMIN_EMAIL)
            category_window.destroy()
            refresh_admin_panel()

        category_window = tk.Toplevel()
        category_window.title("Add Category")
        tk.Label(category_window, text="Category Name", font="Bold",bg="lightblue").pack()
        category_name_entry = tk.Entry(category_window)
        category_name_entry.pack()
        tk.Button(category_window, text="Add",fg="white", width=10,font="Bold",bg="gray", command=submit_category).pack(pady=5)

    def add_item(category_name, items_window):
        def submit_item():
            item_name = name_entry.get()
            item_price = int(price_entry.get())
            item_brand = brand_entry.get()
            item_year = int(year_entry.get())
            item_discount = int(discount_entry.get())
            item_instance = Item(item_name, item_price, item_brand, item_year, item_discount)
            item_instance.add_item_to_category(category_name, ADMIN_EMAIL)
            item_window.destroy()
            refresh_items_window(category_name, items_window)


        item_window = tk.Toplevel()
        item_window.title("Add Item")
        tk.Label(item_window, text="Item Name", font="Bold",bg="lightblue").pack()
        name_entry = tk.Entry(item_window)
        name_entry.pack()
        tk.Label(item_window, text="Price", font="Bold",bg="lightblue").pack()
        price_entry = tk.Entry(item_window)
        price_entry.pack()
        tk.Label(item_window, text="Brand", font="Bold",bg="lightblue").pack()
        brand_entry = tk.Entry(item_window)
        brand_entry.pack()
        tk.Label(item_window, text="Model Year", font="Bold",bg="lightblue").pack()
        year_entry = tk.Entry(item_window)
        year_entry.pack()
        tk.Label(item_window, text="Discount", font="Bold",bg="lightblue").pack()
        discount_entry = tk.Entry(item_window)
        discount_entry.pack()
        tk.Button(item_window, text="Add Item",fg="white", width=10,font="Bold",bg="gray", command=submit_item).pack(pady=5)


    def make_discount(category_name, items_window,item_name):

        def apply_discount():
            categories = Category.load_categories()

            for item in categories.items():
                if item['name'] == item_name:
                    new_price = item['price'] * (1 - item['discount'] / 100)
                    item['price'] = new_price
                    categories.save_categories()

            refresh_items_window(category_name, items_window)

        make_discount_window = tk.Toplevel()
        make_discount_window.title("Make discount")
        tk.Label(make_discount_window, text="Item Name", font="Bold",bg="lightblue").pack()
        item_name_entry = tk.Entry(make_discount_window)
        item_name_entry.pack()
        discount_entry = tk.Entry(make_discount_window)
        discount_entry.pack()

        tk.Label(make_discount_window, text="New Discount", font="Bold",bg="lightblue").pack()
        new_discount_entry = tk.Entry(make_discount_window)
        new_discount_entry.pack()
        tk.Button(make_discount_window, text="Make discount",fg="white", width=10,font="Bold",bg="gray", command=apply_discount).pack(pady=5)

    def delete_item(category_name, items_window):
        def submit_delete_item():
            item_name = item_name_entry.get()
            item_instance = Item()
            item_instance.delete_item_from_category(category_name, item_name, ADMIN_EMAIL)
            messagebox.showinfo("Success", f"Item '{item_name}' deleted from '{category_name}'")
            delete_item_window.destroy()
            refresh_items_window(category_name, items_window)

        delete_item_window = tk.Toplevel()
        delete_item_window.title("Delete Item")
        tk.Label(delete_item_window, text="Item Name", font="Bold",bg="lightblue").pack()
        item_name_entry = tk.Entry(delete_item_window)
        item_name_entry.pack()
        tk.Button(delete_item_window, text="Delete Item", fg="red",font="Bold", command=submit_delete_item).pack(pady=5)



    def edit_item(category_name,items_window):
        def submit_edit_item():
            old_item_name = old_item_name_entry.get()
            new_name = new_name_entry.get() or None
            new_price = new_price_entry.get() or None
            new_brand = new_brand_entry.get() or None
            new_year = new_year_entry.get() or None
            new_discount = new_discount_entry.get() or None

            if new_price is not None:
                new_price = int(new_price)
            if new_year is not None:
                new_year = int(new_year)

            item = Item()
            item.edit_item(category_name, old_item_name, new_name, new_price, new_brand, new_year,new_discount, ADMIN_EMAIL)
            edit_item_window.destroy()
            refresh_items_window(category_name,items_window)

        edit_item_window = tk.Toplevel()
        edit_item_window.title("Edit Item")
        tk.Label(edit_item_window, text="Old Item Name", font="Bold",bg="lightblue").pack()
        old_item_name_entry = tk.Entry(edit_item_window)
        old_item_name_entry.pack()
        tk.Label(edit_item_window, text="New Name (Leave empty to keep current)", font="Bold",bg="lightblue").pack()
        new_name_entry = tk.Entry(edit_item_window)
        new_name_entry.pack()
        tk.Label(edit_item_window, text="New Price (Leave empty to keep current)", font="Bold",bg="lightblue").pack()
        new_price_entry = tk.Entry(edit_item_window)
        new_price_entry.pack()
        tk.Label(edit_item_window, text="New Brand (Leave empty to keep current)", font="Bold",bg="lightblue").pack()
        new_brand_entry = tk.Entry(edit_item_window)
        new_brand_entry.pack()
        tk.Label(edit_item_window, text="New Model Year (Leave empty to keep current)", font="Bold",bg="lightblue").pack()
        new_year_entry = tk.Entry(edit_item_window)
        new_year_entry.pack()
        tk.Label(edit_item_window, text="New Discount (Leave empty to keep current)", font="Bold",bg="lightblue").pack()
        new_discount_entry = tk.Entry(edit_item_window)
        new_discount_entry.pack()

        tk.Button(edit_item_window, text="Edit Item", fg="red",font="Bold", command=submit_edit_item).pack(pady=5)

    def delete_category():
        def submit_delete_category():
            category_name = category_name_entry.get()
            category_instance.delete_category(category_name, ADMIN_EMAIL)
            delete_category_window.destroy()
            refresh_admin_panel()

        delete_category_window = tk.Toplevel()
        delete_category_window.title("Delete Category")
        tk.Label(delete_category_window, text="Category Name", font="Bold",bg="lightblue").pack()
        category_name_entry = tk.Entry(delete_category_window)
        category_name_entry.pack()
        tk.Button(delete_category_window, text="Delete Category", fg="red",font="Bold", command=submit_delete_category).pack(pady=5)

    def edit_category():
        def submit_edit_category():
            old_category_name = old_category_name_entry.get()
            new_category_name = new_category_name_entry.get()
            category = Category()
            category.edit_category(old_category_name, new_category_name, ADMIN_EMAIL)
            messagebox.showinfo("Success", f"Category '{old_category_name}' updated to '{new_category_name}'")
            edit_category_window.destroy()
            refresh_admin_panel()

        edit_category_window = tk.Toplevel()
        edit_category_window.title("Edit Category")
        tk.Label(edit_category_window, text="Old Category Name", font="Bold",bg="lightblue").pack()
        old_category_name_entry = tk.Entry(edit_category_window)
        old_category_name_entry.pack()
        tk.Label(edit_category_window, text="New Category Name", font="Bold",bg="lightblue").pack()
        new_category_name_entry = tk.Entry(edit_category_window)
        new_category_name_entry.pack()
        tk.Button(edit_category_window, text="Update", fg="red",font="Bold", command=submit_edit_category).pack(pady=5)


    def refresh_admin_panel():
        for widget in admin_window.winfo_children():
            widget.destroy()
        tk.Label(admin_window, text="Welcome Admin Panel :)",font="Bold",fg="blue",pady=10).pack(pady=7)
        categories = category_instance.categories.keys()
        for category in categories:
            tk.Button(admin_window, text=category,fg="white", font="Bold",bg="gray", command=lambda c=category: show_items_window(c)).pack(pady=5)
        tk.Button(admin_window, text="Add Category",fg="white", font="Bold",bg="brown", command=add_category).pack(pady=5)
        tk.Button(admin_window, text="Delete Category",fg="white", font="Bold",bg="brown", command=delete_category).pack(pady=5)
        tk.Button(admin_window, text="Edit Category",fg="white", font="Bold",bg="brown", command=edit_category).pack(pady=5)
        tk.Button(admin_window, text="Logout", fg="red",font="Bold", command=admin_window.destroy).pack()


    def refresh_items_window(category_name, items_window):
        for widget in items_window.winfo_children():
            widget.destroy()
        tk.Label(items_window, text="Items:",font="Bold",fg="blue").pack(pady=7)
        items_window
        category_instance = Category()
        items = category_instance.categories.get(category_name)

        if not items:
            tk.Label(items_window, text="No items in this category yet").pack()
        else:
            for item in items:
                tk.Label(items_window, text=f"Name is {item['name']} - Price is {item['price']} \n Brand: {item['brand']} - Model year:  {item['model_year']} \n Discount:  {item['discount']}%",font="Bold").pack(pady=5)

        tk.Button(items_window, text="Add Item",fg="white", font="Bold",bg="gray", command=lambda: add_item(category_name, items_window)).pack(pady=5)
        tk.Button(items_window, text="Delete Item",fg="white", font="Bold",bg="gray", command=lambda: delete_item(category_name, items_window)).pack(pady=5)
        tk.Button(items_window, text="Edit Item",fg="white",font="Bold",bg="gray", command=lambda: edit_item(category_name, items_window)).pack(pady=5)
        #tk.Button(items_window, text="Make Discount",fg="white",font="Bold",bg="gray", command=lambda: make_discount(category_name, items_window)).pack(pady=5)

        tk.Button(items_window, text="Back", fg="red",font="Bold", command=lambda: go_back_to_admin_panel(items_window)).pack(pady=5)
        tk.Button(items_window, text="Logout", fg="red",font="Bold", command=items_window.destroy).pack()

    refresh_admin_panel()
    admin_window.mainloop()

###############################################################################################

def user_categories_panel(user_name, user_email):
    user_window = tk.Tk()
    user_window.title(f"Welcome {user_name}")
    user_window.attributes("-fullscreen", True)
    user_window.configure(bg="lightblue")

    tk.Label(user_window, text=f"Hello, {user_name}! Here are the categories:",fg="blue",bg="lightblue",font="Arial,30",height=3).pack()

    category_instance = Category()
    categories = category_instance.categories.keys()
    cart = Cart(user_email)

    for category in categories:
        tk.Button(user_window, text=category, bg="gray", fg="white", command=lambda c=category: show_category_items(c, user_email)).pack(pady=5)

    tk.Button(user_window, text="View Cart",fg="white", width=10,font="Bold",bg="gray", command=cart.view_cart).pack(pady=5)
    tk.Button(user_window, text="Logout", fg="red",font="Bold", command=user_window.destroy).pack()

    user_window.mainloop()

def show_category_items(category_name, user_email):
    items_window = tk.Toplevel()
    items_window.title(f"Items in {category_name}")
    items_window.configure(bg="lightblue")

    category = Category()
    items = category.categories[category_name]
    cart = Cart(user_email)

    tk.Label(items_window, text="Search Item:", bg="lightblue", font="Bold").pack(pady=5)
    search_entry = tk.Entry(items_window)
    search_entry.pack()

    def search():
        item_name = search_entry.get()
        item = Item()
        item.search(category_name, item_name)

    tk.Button(items_window, text="Search", fg="white", width=10, font="Bold", bg="gray", command=search).pack(pady=5)
    items_frame = tk.Frame(items_window, bg="lightblue")
    items_frame.pack(pady=10)

    def display_items(items):
        for widget in items_frame.winfo_children():
            widget.destroy()

        if not items:
            tk.Label(items_frame, text="No items in this category yet.", bg="lightblue").pack()
        else:
            for item in items:
                tk.Label(items_frame, text=f"{item['name']} - {item['price']} - {item['brand']} - {item['model_year']} - {item['discount']}", font="Bold", bg="lightblue").pack(pady=5)
                tk.Button(items_frame, text="Add to Cart", fg="white", width=10, font="Bold", bg="gray", command=lambda i=item: cart.add_item_to_cart(i)).pack(pady=5)

    display_items(items)

    sort_states = {
        "price": True,  # True = ascending
        "model_year": True,
        "name": True
    }

    def sort_items(sort_by):
        ascending = sort_states[sort_by]
        sorted_items = sorted(items, key=lambda x: x[sort_by], reverse=not ascending)
        display_items(sorted_items)
        sort_states[sort_by] = not ascending

    tk.Button(items_window, text="Sort by Price", fg="white", width=15, font="Bold", bg="gray", command=lambda: sort_items("price")).pack(pady=5)
    tk.Button(items_window, text="Sort by Model Year", fg="white", width=15, font="Bold", bg="gray", command=lambda: sort_items("model_year")).pack(pady=5)
    tk.Button(items_window, text="Sort by Name (Z-A)", fg="white", width=15, font="Bold", bg="gray", command=lambda: sort_items("name")).pack(pady=5)

    tk.Button(items_window, text="View Cart", fg="white", width=10, font="Bold", bg="gray", command=cart.view_cart).pack(pady=6)
    tk.Button(items_window, text="Back to Categories", fg="red", font="Bold", command=items_window.destroy).pack()
login()

