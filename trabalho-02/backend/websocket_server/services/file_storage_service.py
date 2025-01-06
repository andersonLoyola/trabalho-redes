import base64

class FileStorageService(): 

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def _generate_attachment_link(self, file_path):
        return f'http://{self.host}:{self.port}/{file_path}'

    def save_file(self, attachment_data):
        file_name = attachment_data['file_name']
        file_data = attachment_data['file_data']

        file_path = f'uploads/{file_name}'
        decoded_file = base64.b64decode(file_data)
        with open(file_path, 'wb') as f:
            f.write(decoded_file)

        return self._generate_attachment_link(file_path)
        