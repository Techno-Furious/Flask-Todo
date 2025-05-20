import sqlite3
import os

db_path = os.path.join('instance', 'todos.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get table info
cursor.execute("PRAGMA table_info(todo)")
columns = cursor.fetchall()

print("Todo Table Structure:")
for col in columns:
    print(f"Column: {col[1]}, Type: {col[2]}, Nullable: {col[3] == 0}")

# Get a sample row
cursor.execute("SELECT * FROM todo LIMIT 1")
row = cursor.fetchone()
if row:
    print("\nSample Row:")
    for i, col in enumerate(columns):
        print(f"{col[1]}: {row[i]}")

conn.close()