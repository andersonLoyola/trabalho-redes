"""
    REMEMBER TO USE THIS AS REF:
    https://www.geeksforgeeks.org/what-is-pycryptodome-in-python/
"""
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


class CryptoSerializer(): 

    def __init__(self):
        self.secret_key = base64.b64decode('TXshgL49Sfj0GXjEU7IWjpY/9+pVHAmD3eW/29hRK1U=')

    def encrypt(self, data):
        iv = get_random_bytes(16)  
        cipher_enc = AES.new(self.secret_key, AES.MODE_CBC, iv)
        padded_data = pad(data, AES.block_size)
        ciphertext = cipher_enc.encrypt(padded_data)
        encoded_ciphertext = base64.b64encode(ciphertext).decode('utf-8')
        encoded_iv = base64.b64encode(iv).decode('utf-8')
        return { 'data': encoded_ciphertext, 'init_vector': encoded_iv }
    
    def decrypt(self, encoded_data):
        decoded_ciphertext = base64.b64decode(encoded_data['data'].encode('utf-8'))
        decoded_iv = base64.b64decode(encoded_data['init_vector'].encode('utf-8'))
        cipher_dec = AES.new(self.secret_key, AES.MODE_CBC, decoded_iv)
        decrypted_padded_data = cipher_dec.decrypt(decoded_ciphertext)
        decrypted_data = unpad(decrypted_padded_data, AES.block_size)
        return decrypted_data