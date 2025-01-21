
import json

"""
    IMPORTANT: this initially has the socket frame parts combined  
    SEE: https://datatracker.ietf.org/doc/html/rfc6455#section-3
"""

class MessagesService(): 
    
    CHUNK_SIZE = 256 * 1024

    def __init__(self, websocket_serializer, crypto_serializer):
        self.websocket_serializer = websocket_serializer
        self.crypto_serializer = crypto_serializer

    def _chunk_message(self, message):
        msg_bytes = json.dumps(message).encode('utf-8')
        for i in range(0, len(msg_bytes), self.CHUNK_SIZE):
            yield msg_bytes[i:i + self.CHUNK_SIZE] 
   
    def send_handshake_message(self, client_socket):
            handshake_message = (
                "HTTP/1.1 101 Switching Protocols\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                "Sec-WebSocket-Accept:  dGhlIHNhbXBsZSBub25jZQ==\r\n\r\n"
                "Sec-WebSocket-Key: TZ/zHeAVk15vOSYhxVs8rA==\r\n"
            )
            client_socket.send(handshake_message.encode('utf-8'))

    def receive_handshake_message(self, client_socket):
        response = client_socket.recv(1024).decode('utf-8')
        if "HTTP/1.1 101 Switching Protocols" in response and \
        "Upgrade: websocket" in response and \
        "Connection: Upgrade" in response:
            print("Handshake successful!")
            return True
        else:
            print("Handshake failed!")
            return False
        
    def receive_message(self, receiver_socket):
        message_parts = bytearray() 
        done_reading = False
        while done_reading != True:
            part = receiver_socket.recv(self.CHUNK_SIZE)
            if not part:
                break
            web_socket_frame_data = self.websocket_serializer.decode_socket_frame(part)
            message_parts.extend(web_socket_frame_data['data'])
            done_reading = (web_socket_frame_data['fin'] == 1)
        message = message_parts.decode('utf-8')
        decrypted_message = self.crypto_serializer.decrypt(json.loads(message))
        return json.loads(decrypted_message)
        
        
    def send_message(self, client_socket, message):
        message_bytes = json.dumps(message).encode('utf-8')
        cyphered_message_bytes = self.crypto_serializer.encrypt(message_bytes)
        message_chunks = list(self._chunk_message(cyphered_message_bytes))
        for i, message_chunk in (enumerate(message_chunks)):
            fin = (i == len(message_chunks) -1)
            encoded_frame = self.websocket_serializer.encode_socket_frame(message_chunk, fin)
            client_socket.sendall(encoded_frame)
       