import os
import base64

class FileStorageService():

    def load_file(self, file_path):
        try:
            file_size = os.path.getsize(file_path)
            _, file_extension = os.path.splitext(file_path)
            with open(file_path, 'rb') as binary_file:
                binary_file_data = binary_file.read()
                base64_encoded_data = base64.b64encode(binary_file_data)
                base64_output = base64_encoded_data.decode('utf-8')
            
            return {
                'file_size': file_size,
                'file_data': base64_output,
                'file_extension': file_extension,
                'file_name': file_path.split('/')[-1],
            }
        except Exception as e:
            print(e)
    