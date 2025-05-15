import sqlite3

# Connect to your database
conn = sqlite3.connect("cloudaccess.db")
cursor = conn.cursor()

# Run PRAGMA to see table info
cursor.execute("PRAGMA table_info(users);")
columns = cursor.fetchall()

print("Users table columns:")
for column in columns:
    print(column)

conn.close()
