import psycopg2
import os
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

try:
    print("Connecting to database...")
    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()

    print("Clearing userinfo table...")
    c.execute("TRUNCATE TABLE visits RESTART IDENTITY")
    conn.commit()

    print("Table cleared successfully!")
    conn.close()

except Exception as e:
    print("Error:", e)
