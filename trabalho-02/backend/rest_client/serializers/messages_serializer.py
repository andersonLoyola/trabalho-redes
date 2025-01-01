class MessagesSerializer():

    def serialize_message(self, message):
        mapped_message = {}
        mapped_message['_id'] = str(message['_id'])
        mapped_message['content'] = message['content']
        mapped_message['timestamp'] = message['timestamp']
        mapped_message['sender_id'] = message['sender_id']
        mapped_message['attachment'] = message['attachment']
        mapped_message['receiver_id'] = message['receiver_id']
        return mapped_message
    
    def serialize_messages(self, messages):
        return [self.serialize_message(message) for message in messages]