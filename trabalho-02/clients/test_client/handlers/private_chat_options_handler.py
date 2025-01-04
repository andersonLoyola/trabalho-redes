import  os

class PrivateChatOptionsHandler:
    def __init__(self, conn, msg_service):
        self.conn = conn
        self.msg_service = msg_service

    def _print_chat_options(self,  response):
        os.system('cls')
        print('0. go back')
        for index in range(len(response['connections'])):
            print(f'{index +1 }. {response['connections'][index]['chat_name']}')

        choose = int(input('choose chat: '))
        if (choose == 0): 
            return
        elif choose > len(response['connections']):
            print('invalid choise') # this is not gonna  work, deal with this once the project is dosne maybe TODO:
        else:
            return response['connections'][choose-1]
        
       
    def handle_chat_options(self, user_info):
          while True:
            message = {
                'user_id': user_info['user_id'],
                'request_type': 'available_users'
            }
            self.msg_service.send_message(self.conn, message)
            response = self.msg_service.receive_message(self.conn)

            if not response:
                continue
            if 'success' in response and response['response_type'] == 'available_users':
                return self._print_chat_options(response)
            elif response and 'error' in response:
                print(response['error'])
                


