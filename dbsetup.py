import psycopg2

DATABASE_URL = "postgresql://fargodb_user:pYQQq6hrXsYfoQ7a4HlgpwVs0ItUL8xx@dpg-d21qmoidbo4c73eh4g50-a.ohio-postgres.render.com/fargodb"

conn = psycopg2.connect(DATABASE_URL)
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS userinfo (
        id SERIAL PRIMARY KEY,
        ip TEXT,
        user_agent TEXT,
        referrer TEXT,
        timestamp TEXT
    )
''')

conn.commit()
conn.close()
print("Table created!")