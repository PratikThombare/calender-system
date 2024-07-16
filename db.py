import psycopg2

class DBConnection:
    def __enter__(self):
        self.conn = psycopg2.connect(dbname='calender', user='postgres', password='postgres', host='localhost')
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.cursor.close()
        self.conn.close()

def create_tables():
    with DBConnection() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                capacity INTEGER NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS meetings (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP NOT NULL,
                room_id INTEGER,
                FOREIGN KEY(room_id) REFERENCES rooms(id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS participants (
                meeting_id INTEGER,
                user_id INTEGER,
                FOREIGN KEY(meeting_id) REFERENCES meetings(id),
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')

create_tables()
