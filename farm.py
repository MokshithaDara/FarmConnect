import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image,ImageTk
import sqlite3

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        self.previous_window = None
        self.region=None

        self.user_data = {"22B01A0513":"svecw","22B01A0518":"svecw","22B01A0527":"svecw","22B01A0531":"svecw","22B01A0532":"svecw","22B01A0551":"svecw","svecw":"svecw"}
# User data stored in-memory
        
        self.connection = sqlite3.connect("user_data.db")
        self.cursor = self.connection.cursor()

        # Create user_info table if not exists
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                state TEXT,
                season TEXT
            )
        ''')
        self.connection.commit()

        # Create crop_info table if not exists
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS crop_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                state TEXT NOT NULL,
                season TEXT NOT NULL,
                crop_name TEXT NOT NULL,
                crop_description TEXT
            )
        ''')
        self.connection.commit()

        self.insert_sample_crop_data()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS forum_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                message TEXT NOT NULL
            )
        ''')
        self.connection.commit()

        self.fetch_forum_messages()

    def fetch_forum_messages(self):
        self.forum_messages = []
        self.cursor.execute("SELECT * FROM forum_messages")
        messages = self.cursor.fetchall()
        for message in messages:
            self.forum_messages.append({"username": message[1], "message": message[2]})

        
        self.bg_img = Image.open('bg1.jpg')
        self.bg_img = self.bg_img.resize((600, 400))
        self.bg_img = ImageTk.PhotoImage(self.bg_img)
        self.bg_lbl = tk.Label(root, image=self.bg_img)  # Import 'Label' from 'tkinter'
        self.bg_lbl.place(x=0, y=0)
        
        self.title_of_project= tk.Label(root, text="FARMCONNECT", font=("Albertus extra bold",40))
        self.title_of_project.place(x=120,y=20)

        self.username_label = tk.Label(root, text="Username:")
        self.username_label.place(x=200,y=100)

        self.username_entry = tk.Entry(root)
        self.username_entry.place(x=300,y=100)

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.place(x=200,y=150)

        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.place(x=300,y=150)

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.place(x=250,y=200)

        self.registration_button = tk.Button(root, text="Register", command=self.show_registration_page)
        self.registration_button.place(x=350,y=200)

        
    def insert_sample_crop_data(self):
        sample_crop_data = [
        ("Andhra Pradesh", "Summer", "Rice", "Rice is a staple food."),
        ("Meghalaya", "Winter", "Potato", "Potatoes are commonly grown."),
        ("Rajasthan", "Rainy", "Wheat", "Wheat is a major cereal grain."),
        ("Telangana", "Summer", "Cotton", "Cotton is an important cash crop.")
        ]

        for data in sample_crop_data:
            state, season, crop_name, crop_description = data
            self.cursor.execute("INSERT INTO crop_info (state, season, crop_name, crop_description) VALUES (?, ?, ?, ?)",
                            (state, season, crop_name, crop_description))
    
        self.connection.commit()

    def login(self):
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()
        
        self.cursor.execute("SELECT * FROM user_info WHERE username=? AND password=?", (entered_username, entered_password))
        user = self.cursor.fetchone()

        if user:
            messagebox.showinfo("Login Successful", "Welcome, " + entered_username)
            self.open_main_window(entered_username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    def open_region_preference(self):
        region = tk.Toplevel(self.root)
        region.geometry("600x400+500+200")

        self.bg_img_main = Image.open('bg1.jpg')
        self.bg_img_main = self.bg_img_main.resize((600, 400))
        self.bg_img_main = ImageTk.PhotoImage(self.bg_img_main)
        self.bg_lbl_main = tk.Label(region, image=self.bg_img_main)
        self.bg_lbl_main.place(x=0, y=0)

        region.title("Region")

        button_back = tk.Button(region, text="Back", command=region.destroy)
        button_back.place(x=50, y=300)


        state_label = tk.Label(region, text="Select your state:")
        state_label.place(x=200, y=50)

        '''state_entry = tk.Entry(region)
        state_entry.place(x=200, y=100)'''

        states = ["Andhra Pradesh", "Meghalaya", "Rajasthan", "Telangana"]  # Add your own states

        state_var = tk.StringVar()
        state_combobox = ttk.Combobox(region, textvariable=state_var, values=states)
        state_combobox.place(x=200, y=100)


        season_label = tk.Label(region, text="Select the season:")
        season_label.place(x=200, y=150)

        season = ["Summer", "Winter", "Rainy"]  # Add your own states

        season_var = tk.StringVar()
        season_combobox = ttk.Combobox(region, textvariable=season_var, values=season)
        season_combobox.place(x=200, y=200)


        button15 = tk.Button(region, text="Save", command=lambda: self.save_and_redirect_to_main(region,state_var,season_var))
        button15.place(x=250, y=340)

    def save_and_redirect_to_main(self, region, state_var,season_var):
    # Save the selected region to the user_data dictionary (modify as needed)
        entered_username = self.username_entry.get()

        self.cursor.execute("UPDATE user_info SET state=?, season=? WHERE username=?", (state_var.get(), season_var.get(), entered_username))
        self.connection.commit()

        messagebox.showinfo("Save Successful", "Region information saved.")

    # Close the current region window
        region.destroy()

    # Open the main window
        self.display_crop_info_page(entered_username)

    def display_crop_info_page(self, username):
        crop_infor = tk.Toplevel(self.root)
        crop_infor.geometry("600x400+500+200")
        crop_infor.title("Crop Info")

        state = self.cursor.execute("SELECT state FROM user_info WHERE username=?", (username,)).fetchone()[0]
        season = self.cursor.execute("SELECT season FROM user_info WHERE username=?", (username,)).fetchone()[0]

        crop_info = self.cursor.execute("SELECT crop_name, crop_description FROM crop_info WHERE state=? AND season=?", (state, season)).fetchall()

        self.bg_img_main = Image.open('bg1.jpg')
        self.bg_img_main = self.bg_img_main.resize((600, 400))
        self.bg_img_main = ImageTk.PhotoImage(self.bg_img_main)
        self.bg_lbl_main = tk.Label(crop_infor, image=self.bg_img_main)
        self.bg_lbl_main.place(x=0, y=0)

        welcome_label = tk.Label(crop_infor, text="Welcome, " + username, font=("Impact", 10))
        welcome_label.place(x=150, y=50)

        state_var = tk.StringVar()
        state_var.set("Select State")

        crop_label = tk.Label(crop_infor, text="Crop Information for {} in {}".format(season, state), font=("Impact", 10))
        crop_label.place(x=150, y=90)

        crop_text = tk.Text(crop_infor, wrap=tk.WORD, width=40, height=10)
        crop_text.place(x=150, y=120)

        for crop_name, crop_description in crop_info:
            crop_text.insert(tk.END, "Crop: {}\nDescription: {}\n\n".format(crop_name, crop_description))

        crop_text.config(state=tk.DISABLED)

        back_button = tk.Button(crop_infor, text="Back", command=lambda: self.back_to_main_window(crop_infor, username))
        back_button.place(x=250, y=300)

    def back_to_main_window(self, current_window, username):
        current_window.destroy()
        self.open_main_window(username)


    def open_main_window(self,username):

        '''main_window = tk.Toplevel(self.root)
        main_window.geometry("600x400+500+200")
        main_window.title("Main Window")'''

        main_window = getattr(self, 'main_window', None)

        if main_window is not None and main_window.winfo_exists():
            main_window.lift()
        else:
            main_window = tk.Toplevel(self.root)
            main_window.geometry("600x400+500+200")
            main_window.title("Main Window")

        # Set the attribute to keep track of the main window instance
            self.main_window = main_window

        '''state = self.cursor.execute("SELECT state FROM user_info WHERE username=?", (username,)).fetchone()[0]
        season = self.cursor.execute("SELECT season FROM user_info WHERE username=?", (username,)).fetchone()[0]

        crop_info = self.cursor.execute("SELECT crop_name, crop_description FROM crop_info WHERE state=? AND season=?", (state, season)).fetchall()'''

        self.bg_img_main = Image.open('bg1.jpg')
        self.bg_img_main = self.bg_img_main.resize((600, 400))
        self.bg_img_main = ImageTk.PhotoImage(self.bg_img_main)
        self.bg_lbl_main = tk.Label(main_window, image=self.bg_img_main)
        self.bg_lbl_main.place(x=0, y=0)

        welcome_label = tk.Label(main_window, text="Welcome, " + username, font=("Impact",10))
        welcome_label.place(x=150,y=50)

        state_var = tk.StringVar()
        state_var.set("Select State")

        '''crop_label = tk.Label(main_window, text="Crop Information for {} in {}".format(season, state), font=("Impact", 10))
        crop_label.place(x=150, y=90)

        crop_text = tk.Text(main_window, wrap=tk.WORD, width=40, height=10)
        crop_text.pack(pady=5)

        for crop in crop_info:
            crop_name, crop_description = crop
            crop_text.insert(tk.END, "Crop: {}\nDescription: {}\n\n".format(crop_name, crop_description))

        crop_text.config(state=tk.DISABLED)'''

        '''region = tk.Toplevel(self.root)
        region.geometry("600x400+500+200")
        region.title("Region")

        # ... (Your existing code for creating widgets)

        button15 = tk.Button(region, text="Save", command=lambda: self.save_and_redirect_to_main(region, state_var))
        button15.place(x=250, y=340)'''

        button_back = tk.Button(main_window, text="Back", command=main_window.destroy)
        button_back.place(x=50, y=300)


        button1 = tk.Button(main_window, text="Crop Info",command=self.AgricultureInfo)
        button1.place(x=250,y=190)

        button2 = tk.Button(main_window, text="MHC", command=self.open_mental_health_support)
        button2.place(x=250,y=230)

        button3 = tk.Button(main_window, text="Share Insights", command=self.connect_farmers)
        button3.place(x=250,y=270)


    def AgricultureInfo(self):
        '''AgriInfo=tk.Toplevel(self.root)
        AgriInfo.geometry("600x400+500+200")
        AgriInfo.title("AGRICULTURE")
        self.bg_img_agri = Image.open('bg1.jpg')
        self.bg_img_agri = self.bg_img_agri.resize((600, 400))
        self.bg_img_agri = ImageTk.PhotoImage(self.bg_img_agri)
        self.bg_lbl_agri = tk.Label(AgriInfo, image=self.bg_img_agri)
        self.bg_lbl_agri.place(x=0, y=0)'''
        self.open_region_preference()


    
    def open_mental_health_support(self):
        support_window = tk.Toplevel(self.root)
        support_window.geometry("400x300+550+250")
        support_window.title("Mental Health Support")

        # Add content for mental health support
        support_label = tk.Label(support_window, text="Mental Health Support", font=("Arial", 16, "bold"))
        support_label.pack(pady=10)

        support_text = tk.Text(support_window, wrap=tk.WORD, width=40, height=10)
        support_text.insert(tk.END, "If you or someone you know is facing mental health issues, "
                                    "please reach out to the following helpline numbers:\n\n"
                                    "1. National Suicide Prevention Lifeline: 1-800-273-TALK (8255)\n"
                                    "2. Local Mental Health Helpline: [Your local helpline number]\n"
                                    "3. [Any other relevant helpline]\n\n"
                                    "Remember, you are not alone. Help is available.")
        support_text.config(state=tk.DISABLED)
        support_text.pack(pady=10)

        close_button = tk.Button(support_window, text="Close", command=support_window.destroy)
        close_button.pack(pady=10) 

    def connect_farmers(self):
        forum_window = tk.Toplevel(self.root)
        forum_window.geometry("800x600+450+150")
        forum_window.title("Connect Farmers Forum")

        # Add a Text widget for the forum
        forum_text = tk.Text(forum_window, wrap=tk.WORD, width=80, height=20)
        forum_text.pack(pady=10)

        # Add an entry for user input
        user_input_entry = tk.Entry(forum_window, width=80)
        user_input_entry.pack(pady=10)

        for message in self.forum_messages:
            forum_text.insert(tk.END, "{}: {}\n".format(message["username"], message["message"]))


        # Add a button to post messages
        post_button = tk.Button(forum_window, text="Post Message", command=lambda: self.post_message(forum_text, user_input_entry))
        post_button.pack(pady=10)

        # Add a button to close the forum window
        close_button = tk.Button(forum_window, text="Close", command=forum_window.destroy)
        close_button.pack(pady=10)

    '''def post_message(self, forum_text, user_input_entry):
        message = user_input_entry.get()
        if message:
            forum_text.insert(tk.END, "User: " + message + "\n")
            user_input_entry.delete(0, tk.END)

            # Save the message to the dictionary
            username = self.username_entry.get()
            if username not in self.forum_messages:
                self.forum_messages[username] = []
            self.forum_messages[username].append(message)
        else:
            messagebox.showwarning("Empty Message", "Please enter a message.")'''

    def post_message(self, forum_text, user_input_entry):
        message = user_input_entry.get()
        if message:
            username = self.username_entry.get()
            self.cursor.execute("INSERT INTO forum_messages (username, message) VALUES (?, ?)", (username, message))
            self.connection.commit()

            forum_text.insert(tk.END, "User: " + message + "\n")
            user_input_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Empty Message", "Please enter a message.")


    def show_registration_page(self):
        registration_window = tk.Toplevel(self.root)

        registration_window.geometry("600x400+500+200")

        registration_window.title("Registration Page")

        self.bg_img_reg = Image.open('bg1.jpg')
        self.bg_img_reg = self.bg_img_reg.resize((600, 400))
        self.bg_img_reg = ImageTk.PhotoImage(self.bg_img_reg)
        self.bg_lbl_reg = tk.Label(registration_window, image=self.bg_img_reg)
        self.bg_lbl_reg.place(x=0, y=0)

        button_back = tk.Button(registration_window, text="Back", command=registration_window.destroy)
        button_back.place(x=50, y=250)

        
        registration_label = tk.Label(registration_window, text="Registration")
        registration_label.place(x=250,y=40)

        new_username_label = tk.Label(registration_window, text="New Username:")
        new_username_label.place(x=200,y=100)

        new_username_entry = tk.Entry(registration_window)
        new_username_entry.place(x=300,y=100)

        new_password_label = tk.Label(registration_window, text="New Password:")
        new_password_label.place(x=200,y=150)

        new_password_entry = tk.Entry(registration_window, show="*")
        new_password_entry.place(x=300,y=150)

        confirm_password_label = tk.Label(registration_window, text="Confirm Password:")
        confirm_password_label.place(x=200, y=200)

        confirm_password_entry = tk.Entry(registration_window, show="*")
        confirm_password_entry.place(x=300, y=200)

        register_button = tk.Button(registration_window, text="Register", command=lambda :self.register(registration_window, new_username_entry, new_password_entry,confirm_password_entry))
        register_button.place(x=270,y=250)



    def register(self, registration_window, new_username_entry, new_password_entry,confirm_password_entry):
        new_username = new_username_entry.get()
        new_password = new_password_entry.get()
        confirm_password = confirm_password_entry.get()

        if new_password != confirm_password:
            messagebox.showerror("Registration Error", "Passwords do not match.")
            return

        if new_username and new_password:

            self.cursor.execute("SELECT * FROM user_info WHERE username=?", (new_username,))
            existing_user = self.cursor.fetchone()

            if existing_user:
                messagebox.showerror("Registration Error", "Username already exists.")
            else:
                # Insert the new user into the database
                self.cursor.execute("INSERT INTO user_info (username, password) VALUES (?, ?)", (new_username, new_password))
                self.connection.commit()

                messagebox.showinfo("Registration Successful", "Registration complete. You can now log in.")
                registration_window.destroy()
        else:
            messagebox.showerror("Registration Error", "Both username and password are required.")  

    def add_crop_info(self, state, season, crop_name, crop_description):
        # Save crop information to the crop_info table
        self.cursor.execute("INSERT INTO crop_info (state, season, crop_name, crop_description) VALUES (?, ?, ?, ?)",
                            (state, season, crop_name, crop_description))
        self.connection.commit()
        messagebox.showinfo("Crop Information Added", "Crop information added successfully.")



root = tk.Tk()
app = LoginPage(root)
root.geometry("600x400+500+200")
root.mainloop() 
