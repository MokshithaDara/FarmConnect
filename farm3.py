import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3


conn = sqlite3.connect("farmers_marketplace.db")
cursor = conn.cursor()

#table to store user details
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

#table to store products
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
        root.configure(bg='#FFA07A')

        window_width = 1100
        window_height = 400

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.products = []

        user_type = self.user_management_system.get_user_type(self.user_management_system.current_user)

        if user_type == "Farmer":
            self.root.title("Farmer's Marketplace")

            frame = tk.Frame(root,bg='#FFA07A')
            frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

            label_font = ("Arial", 12)
            tk.Label(frame, text="Product Name:", font=label_font, bg='#FFA07A').grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
            tk.Label(frame, text="Price:", font=label_font, bg='#FFA07A').grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
            tk.Label(frame, text="Description:", font=label_font, bg='#FFA07A').grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

            self.product_name_entry = tk.Entry(frame)
            self.product_name_entry.grid(row=0, column=1, padx=10, pady=10)
            self.price_entry = tk.Entry(frame)
            self.price_entry.grid(row=1, column=1, padx=10, pady=10)
            self.description_entry = tk.Entry(frame)
            self.description_entry.grid(row=2, column=1, padx=10, pady=10)

            button_font = label_font
            tk.Button(frame, text="List Product", font=button_font, command=self.list_product).grid(row=3, column=0, columnspan=2, pady=10)
            tk.Button(frame, text="View Products", font=button_font, command=self.view_products).grid(row=4, column=0, columnspan=2, pady=10)

            tk.Button(frame, text="View Orders", font=button_font, command=self.view_orders).grid(row=5, column=0, columnspan=2, pady=10)

            tk.Button(frame, text="Back", font=button_font, command=self.go_back).grid(row=6, column=0, columnspan=2, pady=10)

        elif user_type == "Customer":
            self.root.title("Customer's Marketplace")
            root.configure(bg='#87CEEB')

            frame = tk.Frame(root, bg='#87CEEB')
            frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

            button_font = ("Arial", 12)

            tk.Button(frame, text="View Products", font=button_font, command=self.view_products).pack(side="top", pady=10)

            self.tree = ttk.Treeview(frame, columns=("Product Name", "Price", "Description", "Seller", "Add to Cart"))
            self.tree.pack(side="top", pady=10)

            self.tree.heading("#0", text="ID")
            self.tree.heading("#1", text="Product Name")
            self.tree.heading("#2", text="Price")
            self.tree.heading("#3", text="Description")
            self.tree.heading("#4", text="Seller")

            self.tree.heading("#5", text="Add to Cart")
            self.tree.column("#5", width=100, anchor="center"
            )

            tk.Button(frame, text="Back", font=button_font, command=self.go_back).pack(side="top", pady=10)
            tk.Button(frame, text="Go to cart", font=button_font, command=self.cart).pack(side="top", pady=10)

    def view_orders(self):
                print("View Orders functionality will be implemented here.")
    def cart(self):
                print("Go to cart functionality will be implemented here.")                    

    def go_back(self):

        self.root.destroy()
        self.user_management_system.root.deiconify()    

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

    def view_products(self):
        if self.user_management_system.current_user:
            user_type = self.user_management_system.get_user_type(self.user_management_system.current_user)
            if user_type == "Farmer":

                cursor.execute('''
                    SELECT * FROM products
                    WHERE seller_username = ?
                ''', (self.user_management_system.current_user,))
                farmer_products = cursor.fetchall()

                if farmer_products:
                    product_details = "\n".join([f"Product: {product[1]}\nPrice: ${product[2]:.2f}\nDescription: {product[3]}\n" for product in farmer_products])
                    messagebox.showinfo("Your Products", product_details)
                else:
                    messagebox.showinfo("No Products", "You have not listed any products yet.")
            elif user_type == "Customer":
                current_user_city = self.user_management_system.get_user_city(self.user_management_system.current_user)

                cursor.execute('''
                    SELECT product_name, price, description, seller_username FROM products
                    WHERE seller_username IN (
                        SELECT username FROM users WHERE city = ? AND user_type = 'Farmer'
                    )
                ''', (current_user_city,))

                available_products = cursor.fetchall()

                if available_products:

                    for item in self.tree.get_children():
                        self.tree.delete(item)

                    for product in available_products:
                        price = f"${float(product[1]):.2f}" if isinstance(product[1], str) else product[1]

                        add_to_cart_button = ttk.Button(self.tree, text="Add to Cart", command=lambda product=product: self.add_to_cart(product))

                        item_id = self.tree.insert("", "end", values=(product[0], f"${price}", product[2], product[3], ""))
                    
                        self.tree.set(item_id, "#5", "add_to_cart_tag")

                    self.tree.tag_bind("add_to_cart_tag", "<ButtonRelease-1>", self.handle_add_to_cart_click)


                    messagebox.showinfo("Available Products", "Products listed below:")

                else:
                    messagebox.showinfo("No Products", "No products listed in your city by farmers.")
            else:
                messagebox.showerror("Error", "Only customers and farmers can view products.")
        else:
            messagebox.showerror("Error", "Please login before viewing products.")

    def add_to_cart(self, product):

        print("Product added to cart:")
        print(f"Product Name: {product[0]}")
        print(f"Price: ${product[1]:.2f}")
        print(f"Description: {product[2]}")
        print(f"Seller: {product[3]}")

    def handle_add_to_cart_click(self, event):
        item = self.tree.selection()[0]
        product_name = self.tree.item(item, 'values')[0]
        seller_username = self.tree.item(item, 'values')[3]

        messagebox.showinfo("Add to Cart", f"Product: {product_name}\nSeller: {seller_username}")

    def clear_entries(self):
        self.product_name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

class RegistrationPage:
    def __init__(self, root, user_management_system):
        self.root = root
        self.user_management_system = user_management_system
        self.root.title("Registration Page")
        root.configure(bg='#98FB98')

        window_width = 1100
        window_height = 400

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        frame = tk.Frame(root,bg='#98FB98')
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        label_font = ("Arial", 12)
        tk.Label(frame, text="Username:", font=label_font,bg='#98FB98').grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.username_entry = tk.Entry(frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(frame, text="Password:", font=label_font,bg='#98FB98').grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.password_entry = tk.Entry(frame, show='*')
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(frame, text="User Type:", font=label_font,bg='#98FB98').grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.user_type_var = tk.StringVar(frame)
        self.user_type_var.set("Select User Type")
        user_type_options = ["Farmer", "Customer"]
        self.user_type_dropdown = tk.OptionMenu(frame, self.user_type_var, *user_type_options)
        self.user_type_dropdown.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        tk.Label(frame, text="City:", font=label_font,bg='#98FB98').grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        self.city_entry = tk.Entry(frame)
        self.city_entry.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)

        tk.Label(frame, text="Pincode:", font=label_font,bg='#98FB98').grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        self.pincode_entry = tk.Entry(frame)
        self.pincode_entry.grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)

        tk.Label(frame, text="Mobile Number:", font=label_font,bg='#98FB98').grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)
        self.mobile_number_entry = tk.Entry(frame)
        self.mobile_number_entry.grid(row=5, column=1, padx=10, pady=10, sticky=tk.W)

        button_frame = tk.Frame(frame, bg='#98FB98')
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)

        button_font = label_font
        tk.Button(button_frame, text="Register", font=button_font, command=self.register_user).grid(row=0, column=0, pady=10)
        tk.Button(button_frame, text="Back", font=button_font, command=self.go_back).grid(row=0, column=1, padx=10, pady=10)


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

                cursor.execute('''
                    INSERT INTO users (username, password, user_type, city, pincode, mobile_number)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (username, password, user_type, city, pincode, mobile_number))
                conn.commit()

                messagebox.showinfo("Success", "Registration successful!")

                if user_type == "Farmer":
                    self.user_management_system.current_user = username
                    self.go_back()
                else:
                    messagebox.showinfo("Information", "You have registered as a Customer.")

                self.root.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists. Please choose another username.")
        else:
            messagebox.showerror("Error", "Please fill in all the registration details.")
    def go_back(self):

        self.root.destroy()
        self.user_management_system.root.deiconify()   

class UserManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Login page")
        root.configure(bg='#98FB98')

        window_width = 1100
        window_height = 400

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.current_user = None
        
        login_frame = tk.Frame(root,bg='#98FB98')
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Adjust pady to control the vertical placement

        title_label = tk.Label(login_frame, text="FarmConnect", font=("Helvetica", 20, "bold"), bg='#98FB98')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0,100))

        label_font = ("Arial", 12)
        tk.Label(login_frame, text="Username:", font=label_font, bg='#98FB98').grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        tk.Label(login_frame, text="Password:", font=label_font, bg='#98FB98').grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        ipady_value = 2

        self.username_entry = tk.Entry(login_frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        self.password_entry = tk.Entry(login_frame, show='*')
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        button_font = label_font
        tk.Button(login_frame, text="Register", font=button_font, command=self.show_registration_page).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(login_frame, text="Login", font=button_font, command=self.login).grid(row=4, column=0, columnspan=2, pady=10)

        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def get_user_type(self, username):
        cursor.execute('SELECT user_type FROM users WHERE username = ?', (username,))
        user_type = cursor.fetchone()

        if user_type:
            return user_type[0]
        return None

    def get_user_city(self, username):
        cursor.execute('SELECT city FROM users WHERE username = ?', (username,))
        city = cursor.fetchone()

        if city:
            return city[0]
        return None    

    def show_registration_page(self):
        registration_window = tk.Toplevel(self.root)
        registration_page= RegistrationPage(registration_window, self)

        self.root.withdraw()
        registration_window.wait_window()
        self.root.deiconify()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user_data = cursor.fetchone()

            if user_data:
                self.current_user = username

                if user_data[3] == "Farmer":  # Check the correct index for user type in the database
                    self.show_farmer_marketplace()
                else:
                    self.show_customer_marketplace()
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        else:
            messagebox.showerror("Error", "Please enter both username and password.")
    
    def show_farmer_marketplace(self):
        self.root.withdraw()

        farmer_marketplace_window = tk.Toplevel(self.root)
        farmer_marketplace = FarmerMarketplace(farmer_marketplace_window, self)
    
        farmer_marketplace_window.wait_window()
        self.root.deiconify()


    def show_customer_marketplace(self):
        if self.current_user:

            self.root.withdraw()

            customer_marketplace_window = tk.Toplevel(self.root)
            customer_marketplace = FarmerMarketplace(customer_marketplace_window, self)

            customer_marketplace_window.wait_window()

            self.root.deiconify()
        else:
            messagebox.showerror("Error", "Please login before accessing the marketplace.")

if __name__ == "__main__":
    root = tk.Tk()
    user_management_system = UserManagementSystem(root)
    root.mainloop()

