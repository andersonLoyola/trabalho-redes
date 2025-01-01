import socket
import threading

HOST = '127.0.0.1'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()
"""
 TODO: TRANSFER THIS TO A DATABASE LATER AND DO BASIC USER AUTHENTICATION
    AND IMPLEMENT THE 3 limit 
"""
clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]}")
            broadcast(message)
        except: 
            ## Adds proper handling latter
            index =  clients.index(client)
            clients.remove(index)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

"""
this function will run on the main thread whilst we will have other worker threads
to run the other functions
"""
def receive():
    while True:
        client, address = server.accept() # the client will be the socket client
        print(f"Connected with: {str(address)}")

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)
        
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} has entered the chat'.encode('utf-8'))
        client.send("connected to the server".encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server running...")
receive()