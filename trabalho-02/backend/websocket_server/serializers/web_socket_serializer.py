import os
import base64
import struct
import hashlib

class WebSocketSerializer():

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

    def _extract_bit(self, byte_sequence, position):
        return (byte_sequence >> position) & 1
    
    def _extract_bit_sequence(self, byte_sequence, position, quantity):
        shifted_sequence = byte_sequence >> position
        mask = (1 << quantity) -1
        return shifted_sequence & mask

    def _generate_4_byte_key(self):
        return os.urandom(4)

    def decode_socket_frame(self, data):
        first_byte, second_byte = struct.unpack('!BB', data[:2])
        fin_bit = self._extract_bit(first_byte, 7)
        _ = self._extract_bit(first_byte, 6) # RSV1, NOT USED
        _ = self._extract_bit(first_byte, 5) # RSV2, NOT USED
        _ = self._extract_bit(first_byte, 4) # RSV3, NOT USED
        _ = self._extract_bit_sequence(first_byte, 0, 4) #  Bits 4 up to 7 are for opcode, not used since we only work with txt
      
        masking_bit = self._extract_bit(second_byte, 7) # we are always masking it
        payload_length = self._extract_bit_sequence(second_byte, 0, 7)
        masking_bit = self._extract_bit(second_byte, 7)
        
        index = 2
        if payload_length == 126:
            payload_length = struct.unpack('!H', data[index:index+2])[0]
            index += 2
        elif payload_length == 127:
            payload_length = struct.unpack('!Q', data[index:index+8])[0]
            index += 8

        if masking_bit:
            masking_key = data[index:index+4]
            index += 4
        else:
            masking_key = None
        
        payload_data = data[index:index+payload_length]
        
        if masking_key:
            decoded_payload = bytearray(payload_data)
            for i in range(len(decoded_payload)):
                decoded_payload[i] ^= masking_key[i % 4]
            payload_data = bytes(decoded_payload)

        return {
            'fin': fin_bit,
            'length': payload_length,
            'data': bytes(payload_data),
        }
            
    def encode_socket_frame(self, message, fin=True, opcode=1):
        frame = bytearray()
        first_byte = (fin << 7) | opcode 
        frame.append(first_byte)
        message_length = len(message)
        if message_length <= 125:
            second_byte = 0x80 | message_length  # Set the masking bit and the payload length
            frame.append(second_byte)
        elif message_length <= 65535:
            frame.append(0x80 | 126)  # Set the masking bit and indicate extended payload length
            frame.extend(message_length.to_bytes(2, byteorder='big'))
        else:
            frame.append(0x80 | 127)  # Set the masking bit and indicate extended payload length
            frame.extend(message_length.to_bytes(8, byteorder='big'))
        
        masking_key = self._generate_4_byte_key()
        frame.extend(masking_key)
        
        masked_message = bytearray(message)
        for i in range(len(masked_message)):
            masked_message[i] ^= masking_key[i % 4]
        
        frame.extend(masked_message)
        return bytes(frame)
