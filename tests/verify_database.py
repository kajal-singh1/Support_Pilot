import sqlite3

connection = sqlite3.connect("tickets.db")
cursor = connection.cursor()

cursor.execute("""
    SELECT ticket_id, title, category, severity,
           business_impact, priority, status
    FROM tickets
""")

records = cursor.fetchall()

for record in records:
    print(record)

connection.close()