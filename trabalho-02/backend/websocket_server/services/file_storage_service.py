import base64
import os

class FileStorageService(): 

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def save_file(self, file, file_path):
        file_path = f'uploads/{file_path}'
        decoded_file = base64.b64decode(file)
        with open(file_path, 'wb') as f:
            f.write(decoded_file)

    def generate_attachment_link(self, file_name):
        return f'http://{self.host}:{self.port}/uploads/{file_name}'