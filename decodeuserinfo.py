import os
import psycopg2

DATABASE_URL = None # set to db link

conn = psycopg2.connect(DATABASE_URL)
c = conn.cursor()

c.execute('SELECT * FROM userinfo')
rows = c.fetchall()

for row in rows:
    print(row)

conn.close()