import sqlite3
import uuid

dict_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

connection = sqlite3.connect('../chatuba_db.sqlite3')
connection.row_factory = dict_factory
cursor = connection.cursor()
user_id = uuid.uuid4()
query = """
    INSERT INTO users (
        id,
        username,
        password 
    )
    VALUES (
       ?,
       ?,
       ?
    )
"""


cursor.execute(query, (str(user_id), 'username_2', 'password'))
connection.commit()

query  = f"""
    SELECT * 
    FROM users
    WHERE username = ?
"""
cursor.execute(query, ('username_2',))
user = cursor.fetchone()
print(user)

