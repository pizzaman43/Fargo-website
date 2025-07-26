import psycopg2
import os
DATABASE_URL = os.environ.get('DATABASE_URL')  # Set this in Render's environment variables

conn = psycopg2.connect(DATABASE_URL)
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS userinfo (
        id SERIAL PRIMARY KEY,
        ip TEXT,
        user_agent TEXT,
        timestamp TEXT
    )
''')

conn.commit()
conn.close()
print("Table created!")