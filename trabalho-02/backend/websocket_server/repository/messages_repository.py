import uuid
import datetime

class MessagesRepository():

    def __init__(self, connection_pool):
        self.connection_pool = connection_pool
        

    # MAYBE CREATE CONN FACTORY? OR QUERY EXECUTER TO ENCAPSULATE THE LOGIC?
    def create_private_message(self, sender, receiver, message, attachment):
        conn = self.connection_pool.get_connection()
        cursor = conn.cursor()
        create_user_message_query = """
            INSERT INTO private_messages (
                sender_id, 
                receiver_id, 
                content, 
                attachment_id, 
                timestamp
            )
            VALUES (?, ?, ?, ?, ?)
        """
        create_attachment_query = """
            INSERT INTO attachments (
                id,
                file_format,
                file_size,
                file_name,
                file_path
            ) VALUES (?, ?, ?, ?, ?)
        """
        attachment_id = ''
        cursor.execute('BEGIN;')
        try:
            if attachment != '':
                attachment_id = str(uuid.uuid4())
                cursor.execute(
                    create_attachment_query, (
                        attachment_id,
                        attachment['file_format'],
                        attachment['file_size'],
                        attachment['file_name'],
                        attachment['file_path']
                    )
            )
            cursor.execute(create_user_message_query, (
                    sender, 
                    receiver,
                    message, 
                    attachment_id, 
                    datetime.datetime.now()
                )
            )
            cursor.execute('COMMIT;')
            conn.commit()
        except Exception as e:
            print(f'create_private_message: {e}')
            raise e
        finally:
            self.connection_pool.release_connection(conn)
 
    def create_group_message(self, user_id, chat_id, receivers, message, attachment):
        conn = self.connection_pool.get_connection()
        cursor = conn.cursor()
        create_user_message_query = """
            INSERT INTO group_messages (
                sender_id, 
                chat_id, 
                receiver_id,
                content, 
                attachment_id, 
                timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """
        create_attachment_query = """
            INSERT INTO attachments (
                id,
                file_format,
                file_size,
                file_name,
                file_path
            ) VALUES (?, ?, ?, ?, ?)
        """
        attachment_id = ''
        cursor.execute('BEGIN;')
        try:
            if attachment != '':
                attachment_id = str(uuid.uuid4())
                cursor.execute(
                    create_attachment_query, (
                        attachment_id,
                        attachment['file_format'],
                        attachment['file_size'],
                        attachment['file_name'],
                        attachment['file_path']
                    )
                )
            for receiver_id in receivers:
                cursor.execute(create_user_message_query, (
                        user_id, 
                        chat_id,
                        receiver_id,
                        message, 
                        attachment_id, 
                        datetime.datetime.now()
                    )
                )
            cursor.execute('COMMIT;')
            conn.commit()
        except Exception as e:
            print(f'create_group_message: {e}')
            raise e
        finally:
            self.connection_pool.release_connection(conn)
 
    def get_user_messages(self, sender, receiver):
        pass

    def get_group_messages(self, user_id, chat_id):
        pass