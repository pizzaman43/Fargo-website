import sqlite3

conn = sqlite3.connect('userinfo.db')
c = conn.cursor()

# Show all rows in the userinfo table
for row in c.execute('SELECT * FROM userinfo'):
    print(row)

conn.close()