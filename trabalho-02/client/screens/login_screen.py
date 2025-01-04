import tkinter as tk
from tkinter import ttk

def login():
    user_login = login_entry.get()
    user_password = password_entry.get()
    print(f"Login: {user_login}, Password: {user_password}")

# Create the main window
root = tk.Tk()
root.title("Login Screen")
root.configure(bg='black')

# Create and place the login label and entry
login_label = ttk.Label(root, text="Login:", background='black', foreground='white')
login_label.grid(row=0, column=0, padx=10, pady=10)
login_entry = ttk.Entry(root)
login_entry.grid(row=0, column=1, padx=10, pady=10)

# Create and place the password label and entry
password_label = ttk.Label(root, text="Password:", background='black', foreground='white')
password_label.grid(row=1, column=0, padx=10, pady=10)
password_entry = ttk.Entry(root, show='*')
password_entry.grid(row=1, column=1, padx=10, pady=10)

# Create and place the login button
login_button = ttk.Button(root, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2, pady=10)

# Run the application
root.mainloop()