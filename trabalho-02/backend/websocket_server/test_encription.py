from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import json

message = {
    'request_type': 'message',
    'sender_id': 'some sender',
    'receiver_id': 'some receiver',
    'receiver': 'fkme'
}

key = get_random_bytes(32)  
key_str=base64.b64encode(key).decode('utf-8')
print(key_str)
iv = get_random_bytes(16)   

cipher = AES.new(key, AES.MODE_CBC, iv)

bin_msg = json.dumps(message).encode('utf-8')

padded_data = pad(bin_msg, AES.block_size)
ciphertext = cipher.encrypt(padded_data)


cipher_dec = AES.new(key, AES.MODE_CBC, iv)
decrypted_padded_data = cipher_dec.decrypt(ciphertext)

decrypted_data = unpad(decrypted_padded_data, AES.block_size)

print(f"Ciphertext: {ciphertext}")
print(f"Decrypted Data: {decrypted_data.decode('utf-8')}")