import os
import psycopg2
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()
EXTDATABASE_URL = os.getenv("EXTDATABASE_URL")

conn = psycopg2.connect(EXTDATABASE_URL)
c = conn.cursor()

c.execute("SELECT * FROM visits")
rows = c.fetchall()

for row in rows:
    id, ip, location, device, browser, os, referrer, timestamp = row
    formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    if location == "?, ?, ?":
        location = "Location Missing"

    print(f"[{formatted_time}] {ip} ({location}) - {browser} on {os} via {device}")


conn.close()
