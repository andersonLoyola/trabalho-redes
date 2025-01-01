from Crypto.Cipher import AES

class CryptoService(): 

    def __init__(self, secret_key):
        self.secret_key = secret_key

    def encrypt(self, data):
        cipher = AES.new(self.secret_key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return ciphertext, tag, cipher.nonce
    
    def decrypt(self, ciphertext, tag, nonce):
        cipher = AES.new(self.secret_key, AES.MODE_EAX, nonce=nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        return data