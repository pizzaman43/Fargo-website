import os

import psycopg2

# Get your database URL from environment or hardcode for testing
DATABASE_URL = (
    os.getenv("DATABASE_URL") or "postgresql://user:password@host:port/dbname"
)

try:
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()

    # Fetch all tables in public schema
    cur.execute(
        """
        SELECT tablename FROM pg_tables WHERE schemaname = 'public';
    """
    )
    tables = cur.fetchall()

    if not tables:
        print("✅ No tables to drop. Database is already clean.")
    else:
        for table in tables:
            table_name = table[0]
            print(f"Dropping table: {table_name}")
            cur.execute(f'DROP TABLE IF EXISTS "{table_name}" CASCADE;')

        print("✅ All tables dropped successfully.")

except Exception as e:
    print("❌ Error:", e)

finally:
    if conn:
        cur.close()
        conn.close()
        print("✅ Database connection closed.")
