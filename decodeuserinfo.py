import os
import psycopg2
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
c = conn.cursor()

c.execute('SELECT * FROM visits')
rows = c.fetchall()

for row in rows:
    id, ip, location, device, browser, os, referrer, timestamp = row
    formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"[{formatted_time}] {ip} ({location}) - {browser} on {os} via {device}")


conn.close()