import os
import psycopg2
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
c = conn.cursor()

c.execute('SELECT * FROM userinfo')
rows = c.fetchall()

for row in rows:
    print(row)

conn.close()