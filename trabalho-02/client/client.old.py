# TODO
#  - conexao com o servidor para implementar as funcionalidades e requisitos do projeto

# - cada cliente se comunica com o servidor, que gerenciara a comunicacao entre clientes
# - cada cliente deve se cadastrar junto ao servidor como um usuario
# - cada cliente deve poder se comunicar com outro cliente usando o nome de usuario (semelhante ao que ocorre no WhatsApp atraves do numero de telefone)
# - (OPCIONAL) clientes podem se juntar a grupos multicast (semelhante ao que ocorre no whatsapp)
import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

"""
THE WINDOW THREAD IS THE MAIN THREAD
THE CONNECTIONTHREAD WILL BE A DAEMON THREAD
WHENEVER THE WINDOW IS CLOSED THE CONNECTION IS CLOSED TOO
"""


##TODO: CHANGE TO THE PUBLIC IP ADDRESS AND ALSO LEAVE THE PORT OPEN
HOST = '127.0.0.1'
PORT = 9090


class Client: 
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TODO: look for explanation about what is this later
        self.sock.connect((host, port))

        msg = tkinter.Tk() # user imput for nick (we will need to add one from password)
        msg.withdraw()
        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickme", parent=msg)
        self.gui_done = False # TODO take a look at this later
        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        receive_thread.start()

    # builds the front end
    # see the styling later
    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")
        
        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="lightgray")
        self.chat_label.config(font=("Arial",12))
        self.chat_label.pack(padx=20,  pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20,  pady=5)
        self.text_area.config(state='disabled')

        self.message_label = tkinter.Label(self.win, text="Message:", bg="lightgray")
        self.message_label.config(font=("Arial",12))
        self.message_label.pack(padx=20,  pady=5)

        self.input_area = tkinter.Text(self.win)
        self.input_area.pack(padx=20,  pady=5)

        self.send_button = tkinter.Button(self.win, text='send', command=self.write)
        self.send_button.config(font=("Arial",12))
        self.send_button.pack(padx=20, pady=5)
        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        
        self.win.mainloop()

    # Deals with the server things
    def receive(self):
        while self.running:
            try:
                # what would happen if the message is a file? or exceeds 1024bytes
                # TODO: change this later
                message = self.sock.recv(1024)
                """
                    THIS NICK APPROACH IS BEING DONE TO HANDLE THE NICKNAME OF THE USER
                    TODO: CHANGE THIS LATER TO BE MORE COHERENT, MAYBE USING THE DATABASE
                """
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    """
                        BASICALLY handles the update of the text area where the messages
                        are being display, it appends each message at the end, scrolls down
                        and then disable editt
                    """
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                """
                    FOR NOW ITS JUST BREAKING,
                    TODO: add a exponential backoff retry function to attempt to reconnect with
                    the server
                """
                break
            except:
                print("Error")
                self.sock.close()
                break

     
    """
    sends the msg per say
    currently we are doing the nickname mapping on the client
    TODO: change to do it on server side
    """
    def write(self):
        message = f'{self.nickname}: {self.input_area.get('1.0', 'end')}' # basically instructs the client to get the whole message
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')
    
    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)
Client(HOST, PORT)