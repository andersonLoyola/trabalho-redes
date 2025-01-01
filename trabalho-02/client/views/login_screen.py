import tkinter as tk
from controllers.login_controller import LoginController

class LoginScreen:
    def __init__(self, root, chatuba_enpoint_url, on_login):
        self.root = root
        self.controller = LoginController(chatuba_enpoint_url, on_login)
        self.create_widgets()

    def create_widgets(self):
        self.username_label = tk.Label(self.root, text="Enter your nickname:")
        self.username_label.pack(pady=10)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=10)
        
        self.password_label = tk.Label(self.root, text="Enter your password:")
        self.password_label.pack(pady=10)
        self.password_entry = tk.Entry(self.root)
        self.password_entry.pack(pady=10)

        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        self.login_button.pack(pady=10)

    def login(self):
        nickname = self.username_entry.get()
        password = self.password_entry.get()

        self.controller.login(nickname, password)