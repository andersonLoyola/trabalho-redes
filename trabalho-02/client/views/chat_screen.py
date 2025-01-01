import tkinter as tk
import threading
import socket

class ChatScreen:
    def __init__(self, root, user_profile_data):
        self.root = root
        self.username = user_profile_data['username']
        self.access_token = user_profile_data['access_token']
        self.refresh_token = user_profile_data['refresh_token']
        # self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.connect(('127.0.0.1', 9090))
        self.create_widgets()
        self.gui_done = False

  
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

    def create_widgets(self):
        self.chat_label = tk.Label(self.root, text="Chat:", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tk.Text(self.root)
        self.text_area.config(state='disabled')
        self.text_area.pack(padx=20, pady=5)

        self.msg_label = tk.Label(self.root, text="Message:", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tk.Text(self.root, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tk.Button(self.root, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.gui_done = False
        self.root.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while True:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                # print("An error occurred!")
                # self.sock.close()
                break