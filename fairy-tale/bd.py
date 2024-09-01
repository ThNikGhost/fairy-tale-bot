import sqlite3
from threading import Lock

# Создание базы данных
conn = sqlite3.connect('user_messages.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_messages
    (user_id INTEGER, previous_message TEXT, previous_user_request TEXT)
''')

lock = Lock()

def get_user_messages(user_id):
    with lock:
        cursor.execute('SELECT * FROM user_messages WHERE user_id = ?', (user_id,))
        return cursor.fetchone()

def update_user_messages(user_id, previous_message, previous_user_request):
    with lock:
        cursor.execute('SELECT * FROM user_messages WHERE user_id = ?', (user_id,))
        if cursor.fetchone():
            cursor.execute('''
                UPDATE user_messages
                SET previous_message = ?, previous_user_request = ?
                WHERE user_id = ?
            ''', (previous_message, previous_user_request, user_id))
        else:
            cursor.execute('''
                INSERT INTO user_messages (user_id, previous_message, previous_user_request)
                VALUES (?, ?, ?)
            ''', (user_id, previous_message, previous_user_request))
        conn.commit()