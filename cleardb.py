import psycopg2

DATABASE_URL = os.environ.get('DATABASE_URL')  # Set this in Render's environment variables

try:
    print("Connecting to database...")
    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()
    
    print("Clearing userinfo table...")
    c.execute('TRUNCATE TABLE userinfo RESTART IDENTITY')
    conn.commit()
    
    print("Table cleared successfully!")
    conn.close()
    
except Exception as e:
    print("Error:", e) 