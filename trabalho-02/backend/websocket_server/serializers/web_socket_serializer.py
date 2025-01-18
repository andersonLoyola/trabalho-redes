import base64
import hashlib

class WebSocketSerializer():

    FIN_EXTRACTION_MASK = 0b10000000 
    MASK_EXTRACTION_BYTE = 0b10000000
    OPCODE_EXTRACTION_MASK = 0b00001111
    PAYLOAD_LENGTH_EXTRACTION_BYTE = 0b01111111 

    def parse_headers(self, request):
        headers = {}
        request_chunks = request.split('\r\n')
        for chunk in request_chunks[1:]:
            if chunk:
                key, value = chunk.split(': ', 1)
                headers[key] = value
        return headers

    def handshake(self, client_socket):
        request = client_socket.recv(1024).decode('utf-8')
        headers = self.parse_headers(request)
        websocket_key = headers['Sec-WebSocket-Key']
        websocket_accept = base64.b64encode(hashlib.sha1((websocket_key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode('utf-8')).digest()).decode('utf-8')
        response = (
            'HTTP/1.1 101 Switching Protocols\r\n'
            'Upgrade: websocket\r\n'
            'Connection: Upgrade\r\n'
            f'Sec-WebSocket-Accept: {websocket_accept}\r\n\r\n'
        )
        client_socket.send(response.encode('utf-8'))

    def decode_socket_frame(self, data):
        first_byte = data[0]
        fin = first_byte & self.FIN_EXTRACTION_MASK 
        opcode = first_byte & self.OPCODE_EXTRACTION_MASK #opcode
        if opcode == 8: 
            return None
        
        second_byte = data[1]
        payload_length = second_byte & self.PAYLOAD_LENGTH_EXTRACTION_BYTE
        if payload_length == 126:
            extended_payload_length = data[2:4] 
            payload_length = int.from_bytes(extended_payload_length, byteorder='big')
            masking_key = data[4:8]
            payload_data = data[8:]
        elif payload_length == 127:
            extended_payload_length =data[2:10]
            payload_length = int.from_bytes(extended_payload_length, byteorder='big')
            masking_key = data[10:14]
            payload_data = data[14: ]
        else:
            masking_key = data[2:6] 
            payload_data = data[6:] 
        message_bytes = bytearray([payload_data[i] ^ masking_key[i % 4] for i in range(payload_length)])
        return message_bytes
    
    def encode_socket_frame(self, message, fin=True, opcode=1):
        frame =  bytearray()
        first_byte = (fin << 7) | opcode 
        frame.append(first_byte)
        message_length = len(message)
        if message_length <= 125:
            frame.append(message_length)
        elif message_length <= 65535:
            frame.append(126)
            frame.extend(message_length.to_bytes(2, byteorder='big'))
        else:
            frame.append(127)
            frame.extend(message_length.to_bytes(8, byteorder='big'))
        masking_key = [0,0,0,0] # currently set to 0, meaning no mask for now
        frame.extend(masking_key)
        frame.extend(message)
        return bytes(frame)
