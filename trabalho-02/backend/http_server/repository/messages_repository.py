import uuid
import datetime

class MessagesRepository:

    def __init__(self, connection_pool):
        self.connection_pool = connection_pool
        
    def create_private_message(self, sender, receiver, message, message_init_vector, attachment):
        create_init_vector =  """
            INSERT INTO init_vectors (
                id,
                init_vector
            ) VALUES (?, ?)
        """
        create_user_message_query = """
            INSERT INTO private_messages (
                sender_id, 
                receiver_id, 
                content, 
                attachment_id, 
                timestamp,
                init_vector_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """
        create_attachment_query = """
            INSERT INTO attachments (
                id,
                file_format,
                file_size,
                file_name,
                file_path,
                init_vector_id
            ) VALUES (?, ?, ?, ?, ?, ?)
        """
        attachment_id = ''
        try:
            conn = self.connection_pool.get_connection()
            cursor = conn.cursor()
            cursor.execute('BEGIN;')
            if attachment != '':
                attachment_id = str(uuid.uuid4())
                attachment_init_vector_id = str(uuid.uuid4())
                cursor.execute(create_init_vector, (attachment_init_vector_id, attachment['init_vector']))
                cursor.execute(
                    create_attachment_query, (
                        attachment_id,
                        attachment['file_extension'],
                        attachment['file_size'],
                        attachment['file_name'],
                        attachment['file_path'],
                        attachment_init_vector_id
                    )
                )
            cursor.execute(create_user_message_query, (
                    sender, 
                    receiver,
                    message, 
                    attachment_id, 
                    message_init_vector,
                    datetime.datetime.now(),
                )
            )
            conn.commit()
        except Exception as e:
            cursor.execute('ROLLBACK;')
            print(f'create_private_message: {e}')
            raise e
        finally:
            self.connection_pool.release_connection(conn)
 
    def create_group_message(
        self, 
        user_id, 
        chat_id, 
        receivers, 
        message,
        message_init_vector, 
        attachment
    ):
        create_init_vector =  """
            INSERT INTO init_vectors (
                id,
                init_vector
            ) VALUES (?, ?)
        """
        create_user_message_query = """
            INSERT INTO group_messages (
                sender_id, 
                chat_id, 
                receiver_id,
                content, 
                attachment_id,
                init_vector_id,
                timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        create_attachment_query = """
            INSERT INTO attachments (
                id,
                file_format,
                file_size,
                file_name,
                file_path,
                init_vector_id
            ) VALUES (?, ?, ?, ?, ?, ?)
        """
        try:
            attachment_id = ''
            message_init_vector_id = str(uuid.uuid4())
            conn = self.connection_pool.get_connection()
            cursor = conn.cursor()
            cursor.execute('BEGIN;')
            cursor.execute(create_init_vector, (message_init_vector_id, message_init_vector))
            
            if attachment != '':
                attachment_id = str(uuid.uuid4())
                attachment_init_vector_id = str(uuid.uuid4())
                cursor.execute(create_init_vector, (attachment_init_vector_id, attachment['init_vector']))
                cursor.execute(
                    create_attachment_query, (
                        attachment_id,
                        attachment['file_extension'],
                        attachment['file_size'],
                        attachment['file_name'],
                        attachment['file_path'],
                        attachment_init_vector_id
                    )
                )
            for receiver_id in receivers:
                cursor.execute(create_user_message_query, (
                        user_id, 
                        chat_id,
                        receiver_id,
                        message, 
                        attachment_id, 
                        message_init_vector_id,
                        datetime.datetime.now(),
                    )
                )
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f'create_group_message: {e}')
            raise e
        finally:
            self.connection_pool.release_connection(conn)
 
    def get_private_messages(self, sender, receiver):
        get_private_messages_query = """
           WITH message
        """

    def get_group_messages(self, user_sessions, chat_id):
        group_messages_query = f"""
        WITH senders AS (
            SELECT 
                u.username AS user_name,
                us.session_id AS sender_id
            FROM user_sessions us 
            INNER JOIN users u 
            ON u.id = us.user_id
        ),
        receivers AS (
            SELECT 
                u.username AS user_name,
                us.session_id AS receiver_id,
                us.user_id
            FROM user_sessions us 
            INNER JOIN users u 
            ON u.id = us.user_id
        ),
        message_init_vectors AS (
            SELECT 
                iv.id,
                iv.init_vector
            FROM group_messages gm
            INNER JOIN init_vectors iv
            ON iv.id = gm.init_vector_id
        ),
        attachment_init_vectors AS (
            SELECT 
                iv.id ,
                iv.init_vector
            FROM attachments at
            INNER JOIN init_vectors iv
            ON iv.id = at.init_vector_id
        )
        SELECT DISTINCT 
            at.file_name,
            gm."timestamp",
            c.name AS chat_name,
            ss.user_name AS sender,
            gm.content AS message,
            rs.user_name AS receiver,
            ss.sender_id AS sender_id,
            rs.receiver_id AS receiver_id,
            miv.init_vector AS message_init_vector,
            aiv.init_vector AS attachment_init_vector
        FROM group_messages gm 
        INNER JOIN senders ss
            ON gm.sender_id = ss.sender_id
        INNER JOIN receivers rs
            ON rs.receiver_id = gm.receiver_id
        INNER JOIN chats c
            ON c.id = gm.chat_id 
        INNER JOIN message_init_vectors miv
            ON miv.id = gm.init_vector_id 
        LEFT JOIN attachments at
            ON at.id = gm.attachment_id 
        LEFT JOIN attachment_init_vectors aiv
            ON aiv.id = at.init_vector_id 
        WHERE
            gm.chat_id = ?
            AND gm.receiver_id in ({','.join(['?' for _ in user_sessions])})
        ORDER BY gm."timestamp"
        """
        try:
            conn = self.connection_pool.get_connection()
            cursor = conn.cursor() 
            cursor.execute(group_messages_query, (
                    chat_id, 
                    *user_sessions
                )
            )
            return cursor.fetchall()
        except Exception as e:
            print(f'get_group_messages: {e}')
            raise e
        finally:
            self.connection_pool.release_connection(conn)