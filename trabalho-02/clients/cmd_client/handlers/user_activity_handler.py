import os
import json
import datetime
import threading

from .base_handler import BaseHandler
from serializers import CryptoSerializer
from services import FileStorageService, UserHistoryService


class UserActivityHandler(BaseHandler):

    crypto_serializer: CryptoSerializer
    file_storage_service: FileStorageService

    def __init__(
        self, 
        user_history_service: UserHistoryService, 
        file_storage_service: FileStorageService, 
        crypto_serializer: CryptoSerializer
    ):
        self.user_history_service = user_history_service
        self.file_storage_service = file_storage_service
        self.crypto_serializer = crypto_serializer

    def _format_timestamp(self, timestamp):
        return timestamp.strftime('%Y-%m-%d-%Hh-%Mm-%Ss')

    def _generate_report_file(self, response, current_user_data):
        decrypted_response = json.loads(self.crypto_serializer.decrypt(response))
        formated_messages = []
        if 'group_messages' not in decrypted_response:
            input('Chat not found')
            return
        if len(decrypted_response['group_messages']) == 0:
            input('No group messages were found')
            return
        chat_name = '-'.join(decrypted_response['group_messages'][0]['chat_name'])  
        file_name = f'{chat_name}-{self._format_timestamp(datetime.datetime.now())}.log'
        for message in decrypted_response['group_messages']:
            formated_message=''
            formated_message_timestamp = self._format_timestamp(datetime.datetime.fromisoformat(message['timestamp']))
            if message['message'] != None:
                decrypted_message = self.crypto_serializer.decrypt({
                    'data': message['message'],
                    'init_vector': message['message_init_vector']
                })
                formated_message = f'[{message['sender']}][{message['chat_name']}][{formated_message_timestamp}]> {decrypted_message.decode('utf-8')}'
            # if message['file_name'] != None:
            #     decrypted_file_name = self.crypto_serializer.decrypt({
            #         'data': message['file_name'],
            #         'init_vector': message['attachment_init_vector']
            #     })
            #     formated_message = f'[{message['sender']}][{message['chat_name']}][{formated_message_timestamp}]> send a file {decrypted_file_name.decode('utf-8')}'
            formated_messages.append(formated_message)
        
        self.file_storage_service.write_file(current_user_data['id'], file_name, '\n'.join(formated_messages))
        input('report generated successfully')

    def generate_group_chat_report(self, current_user_data):
        while True:
            os.system('cls')
            try:
                print('Type \\q to leave')
                option = str(input('chat name: '))
                if option == '\\q':
                    return
                response = self.user_history_service.get_group_chat_messages_from_chat(current_user_data['id'], option)
                if 'error' in response:
                    input(response['error'])
                    continue
                dthread = threading.Thread(target=self._generate_report_file, args=(response, current_user_data), daemon=True, name='process-report')
                dthread.start()
            except Exception as e:
                input(str(e))
                raise e
            