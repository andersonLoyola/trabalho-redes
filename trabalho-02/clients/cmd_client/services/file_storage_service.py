import os
import base64

class FileStorageService():


    def write_file(self, user_id: str, file_name: str, text: str):
        try:
            directory_path = f'downloads/{user_id}'
            os.makedirs(directory_path, exist_ok=True)
            file_path = f'{directory_path}/{file_name}'
            with open(file_path, 'w') as file:
                file.write(text)
        except Exception as e:
            print(e)

    def load_file(self, file_path: str):
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
    
    def save_file(self, user_id, attachment_data):
        file_name = attachment_data['file_name']
        file_data = attachment_data['file_data']
        # Create the directory if it does not exist
        directory_path = f'downloads/{user_id}'
        os.makedirs(directory_path, exist_ok=True)
        file_path = f'{directory_path}/{file_name}'
        decoded_file = base64.b64decode(file_data)
        with open(file_path, 'wb') as f:
            f.write(decoded_file)
