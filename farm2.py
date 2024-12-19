import tkinter as tk
from tkinter import simpledialog, messagebox

import sqlite3

# Connect to SQLite database (create a new one if it doesn't exist)
conn = sqlite3.connect("farmers_marketplace.db")
cursor = conn.cursor()

# Create a table to store user details
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        user_type TEXT NOT NULL,
        city TEXT NOT NULL,
        pincode TEXT NOT NULL,
        mobile_number TEXT NOT NULL
    )
''')
conn.commit()

# Create a table to store products
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        price REAL NOT NULL,
        description TEXT,
        seller_username TEXT NOT NULL,
        FOREIGN KEY (seller_username) REFERENCES users (username)
    )
''')
conn.commit()

class FarmerMarketplace:
    def __init__(self, root, user_management_system):
        self.root = root
        self.user_management_system = user_management_system
        self.root.title("Farmer's Marketplace")

        self.products = []

        # Labels
        tk.Label(root, text="Product Name:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        tk.Label(root, text="Price:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        tk.Label(root, text="Description:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        # Entry Widgets
        self.product_name_entry = tk.Entry(root)
        self.product_name_entry.grid(row=0, column=1, padx=10, pady=10)
        self.price_entry = tk.Entry(root)
        self.price_entry.grid(row=1, column=1, padx=10, pady=10)
        self.description_entry = tk.Entry(root)
        self.description_entry.grid(row=2, column=1, padx=10, pady=10)

        # Buttons
        tk.Button(root, text="List Product", command=self.list_product).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(root, text="View Products", command=self.view_products).grid(row=4, column=0, columnspan=2, pady=10)

    def list_product(self):
        if self.user_management_system.current_user:
            product_name = self.product_name_entry.get()
            price = self.price_entry.get()
            description = self.description_entry.get()

            if product_name and price:
                try:
                    price = float(price)
                    seller_username = self.user_management_system.current_user
                    self.products.append({"Product": product_name, "Price": price, "Description": description, "Seller": seller_username})
                    
                    # Insert product details into the database
                    cursor.execute('''
                        INSERT INTO products (product_name, price, description, seller_username)
                        VALUES (?, ?, ?, ?)
                    ''', (product_name, price, description, seller_username))
                    conn.commit()

                    messagebox.showinfo("Success", f"{product_name} listed successfully!")
                    self.clear_entries()
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid price.")
            else:
                messagebox.showerror("Error", "Please enter both product name and price.")
        else:
            messagebox.showerror("Error", "Please login before listing a product.")

    def get_user_type(self, username):
        cursor.execute('SELECT user_type FROM users WHERE username = ?', (username,))
        user_type = cursor.fetchone()

        if user_type:
            return user_type[0]
        return None

    def view_products(self):
        if self.user_management_system.current_user:
            user_type = self.user_management_system.get_user_type(self.user_management_system.current_user)
            if user_type in ["Customer", "Farmer"]:
                current_user_city = self.user_management_system.get_user_city(self.user_management_system.current_user)

            # Fetch available products from the database based on the user's city
                cursor.execute('''
                    SELECT * FROM products
                    WHERE seller_username IN (
                    SELECT username FROM users WHERE city = ?
                    )
                ''', (current_user_city,))

                available_products = cursor.fetchall()

                if available_products:
                    product_details = "\n".join([f"Product: {product[1]}\nSeller: {product[4]}\nPrice: ${product[2]:.2f}\nDescription: {product[3]}\n" for product in available_products])
                    messagebox.showinfo("Available Products", product_details)
                else:
                    messagebox.showinfo("No Products", "No products listed in your city.")
            else:
                messagebox.showerror("Error", "Only customers and farmers can view products.")
        else:
            messagebox.showerror("Error", "Please login before viewing products.")



    def clear_entries(self):
        self.product_name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

class RegistrationPage:
    def __init__(self, root, user_management_system):
        self.root = root
        self.user_management_system = user_management_system
        self.root.title("Registration Page")

        # Labels
        tk.Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        tk.Label(root, text="User Type:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        tk.Label(root, text="City:").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        tk.Label(root, text="Pincode:").grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        tk.Label(root, text="Mobile Number:").grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)

        # Entry Widgets
        self.username_entry = tk.Entry(root)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.password_entry = tk.Entry(root, show='*')
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Dropdown for User Type
        self.user_type_var = tk.StringVar(root)
        self.user_type_var.set("Select User Type")
        user_type_options = ["Farmer", "Customer"]
        self.user_type_dropdown = tk.OptionMenu(root, self.user_type_var, *user_type_options)
        self.user_type_dropdown.grid(row=2, column=1, padx=10, pady=10)

        self.city_entry = tk.Entry(root)
        self.city_entry.grid(row=3, column=1, padx=10, pady=10)
        self.pincode_entry = tk.Entry(root)
        self.pincode_entry.grid(row=4, column=1, padx=10, pady=10)
        self.mobile_number_entry = tk.Entry(root)
        self.mobile_number_entry.grid(row=5, column=1, padx=10, pady=10)

        # Button
        tk.Button(root, text="Register", command=self.register_user).grid(row=6, column=0, columnspan=2, pady=10)

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_type = self.user_type_var.get()
        city = self.city_entry.get()
        pincode = self.pincode_entry.get()
        mobile_number = self.mobile_number_entry.get()

        if user_type == "Select User Type":
            messagebox.showerror("Error", "Please select a valid user type.")
            return

        if username and password and user_type and city and pincode and mobile_number:
            try:
                # Insert user details into the database
                cursor.execute('''
                    INSERT INTO users (username, password, user_type, city, pincode, mobile_number)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (username, password, user_type, city, pincode, mobile_number))
                conn.commit()

                messagebox.showinfo("Success", "Registration successful!")

                if user_type == "Farmer":
                    self.user_management_system.current_user = username
                    self.show_farmer_marketplace()
                else:
                    messagebox.showinfo("Information", "You have registered as a Customer.")

                self.root.destroy()  # Close the registration window after successful registration
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists. Please choose another username.")
        else:
            messagebox.showerror("Error", "Please fill in all the registration details.")

    def show_farmer_marketplace(self):
        farmer_marketplace_window = tk.Toplevel(self.root)
        farmer_marketplace = FarmerMarketplace(farmer_marketplace_window, self.user_management_system)

class UserManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("User Management System")

        self.users = {}
        self.current_user = None

        # Labels
        tk.Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        # Entry Widgets
        self.username_entry = tk.Entry(root)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.password_entry = tk.Entry(root, show='*')
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Buttons
        tk.Button(root, text="Register", command=self.show_registration_page).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(root, text="Login", command=self.login).grid(row=3, column=0, columnspan=2, pady=10)

    def show_registration_page(self):
        registration_window = tk.Toplevel(self.root)
        registration_page = RegistrationPage(registration_window, self)

    def register_user(self, username, password, user_type, city, pincode, mobile_number):
        self.users[username] = {
            "password": password,
            "user_type": user_type,
            "city": city,
            "pincode": pincode,
            "mobile_number": mobile_number
        }

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
        # Fetch user details from the database
            cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user_data = cursor.fetchone()

            if user_data:
                self.current_user = username

                if user_data[3] == "Farmer":  # Check the correct index for user type in the database
                    self.show_farmer_marketplace()
                else:
                    messagebox.showinfo("Information", "You have logged in as a Customer.")
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        else:
            messagebox.showerror("Error", "Please enter both username and password.")

    def show_farmer_marketplace(self):
        farmer_marketplace_window = tk.Toplevel(self.root)
        farmer_marketplace = FarmerMarketplace(farmer_marketplace_window, self)

    def get_user_city(self, username):
        if username in self.users:
            return self.users[username]["city"]
        return None

if __name__ == "__main__":
    root = tk.Tk()
    user_management_system = UserManagementSystem(root)
    root.mainloop()
