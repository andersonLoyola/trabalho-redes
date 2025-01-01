import socket

def create_socket_connection():
    host = 'localhost'
    port = 9090

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((host, port))
        print(f"Connected to {host} on port {port}")

        # Send a test message
        message = "Hello, Server!"
        client_socket.sendall(message.encode('utf-8'))

        # Receive a response
        response = client_socket.recv(1024)
        print(f"Received from server: {response.decode('utf-8')}")

    except ConnectionError as e:
        print(f"Connection error: {e}")

    finally:
        # Close the connection
        client_socket.close()

if __name__ == "__main__":
    create_socket_connection()