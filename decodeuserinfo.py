import os
import psycopg2

DATABASE_URL = "postgresql://fargodb_user:pYQQq6hrXsYfoQ7a4HlgpwVs0ItUL8xx@dpg-d21qmoidbo4c73eh4g50-a.ohio-postgres.render.com/fargodb"

conn = psycopg2.connect(DATABASE_URL)
c = conn.cursor()

c.execute('SELECT * FROM userinfo')
rows = c.fetchall()

print(rows)

conn.close()