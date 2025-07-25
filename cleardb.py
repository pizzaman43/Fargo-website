import psycopg2

DATABASE_URL = "postgresql://fargodb_user:pYQQq6hrXsYfoQ7a4HlgpwVs0ItUL8xx@dpg-d21qmoidbo4c73eh4g50-a.ohio-postgres.render.com/fargodb"

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