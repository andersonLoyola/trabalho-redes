import os
import tkinter as tk
# from dotenv import load_dotenv
from views.chat_screen import ChatScreen
from views.login_screen import LoginScreen
from controllers.login_controller import LoginController

"""
 def gui_loop(self):
        def gui_loop(self):
        self.gui_done = True
        self.root.protocol("WM_DELETE_WINDOW", self.stop)
        self.root.mainloop()

"""
class ClientApp:
    def __init__(self):
        # load_dotenv()
        self.root = tk.Tk()
        self.root.title("Client Application")
        # self.chatuba_api_url = os.getenv("CHATUBA_API_URL")
        self.chatuba_api_url = "http://localhost:8080"
        self.show_login_screen()

    def show_login_screen(self):
        self.clear_screen()
        LoginScreen(self.root, self.chatuba_api_url, self.show_chat_screen)
       
    def show_chat_screen(self, nickname):
        self.clear_screen()
        ChatScreen(self.root, nickname)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ClientApp()
    app.run()