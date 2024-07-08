import sqlite3
import random

connection = sqlite3.connect('testing.db')

cursor = connection.cursor()

cursor.execute(""" 
CREATE TABLE IF NOT EXISTS purchase (
    list_of_items TEXT
)
""")

list_of_items = ['headphones', 'keyboard', 'computer mouse', 'CPU','keyboard', 'graphics card', 'RAM', 'SSD', 'hard drive disk','headphones', 'computer fan', 'controller','computer mouse']

for _ in range(10000):
    ran = random.randint(1,10)
    list_for_db = []
    if ran == 10:
        list_for_db = list(set(list_of_items.copy()))
    else:
        for x in range(ran):
            while True:
                ran_item = random.randint(0,13)
                if list_of_items[ran_item] not in list_for_db:
                    list_for_db.append(list_of_items[ran_item])
                    break
    
    upload = ''
    for x in list_for_db: upload += x +'|'

    query = "INSERT INTO purchase  VALUES (?)"
    cursor.execute(query, [upload])

    
cursor.execute(""" 
SELECT * FROM purchase
""")
rows = cursor.fetchall()
print(rows)

connection.commit()
connection.close()