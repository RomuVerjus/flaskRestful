import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"

create_items = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"


cursor.execute(create_table)
cursor.execute(create_items)
# cursor.execute("INSERT INTO items VALUES('test', 10.11)")


connection.commit()

connection.close()
