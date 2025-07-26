import os
import psycopg2

DATABASE_URL = os.environ.get('DATABASE_URL')  # Set this in Render's environment variables

conn = psycopg2.connect(DATABASE_URL)
c = conn.cursor()

c.execute('SELECT * FROM userinfo')
rows = c.fetchall()

for row in rows:
    print(row)

conn.close()