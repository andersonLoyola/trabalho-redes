import os
import base64

class FileStorageService(): 

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def _generate_attachment_link(self, file_path):
        return f'http://{self.host}:{self.port}/{file_path}'

    def save_file(self, user_id, attachment_data):
        file_name = attachment_data['file_name']
        file_data = attachment_data['file_data']
        # Create the directory if it does not exist
        directory_path = f'uploads/{user_id}'
        os.makedirs(directory_path, exist_ok=True)
        file_path = f'{directory_path}/{file_name}'
        decoded_file = base64.b64decode(file_data)
        with open(file_path, 'wb') as f:
            f.write(decoded_file)

        return self._generate_attachment_link(file_path)
        
        