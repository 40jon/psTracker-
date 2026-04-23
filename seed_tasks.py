import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

cursor.execute("DELETE FROM tasks")

sample_tasks = [
    ("Call client about listing update", "In Progress"),
    ("Review CRM lead entries", "Pending"),
    ("Prepare dashboard notes", "Done")
]

cursor.executemany(
    "INSERT INTO tasks (title, status) VALUES (?, ?)",
    sample_tasks
)

connection.commit()
connection.close()

print("Sample tasks inserted successfully.")
