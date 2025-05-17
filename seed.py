import sqlite3
import csv

data = []

with open('vocabularies.csv', mode='r', newline='', encoding='cp1252') as file:
    reader = csv.reader(file, delimiter='\t')
    next(reader)  # Skip header row
    for row in reader:
        if len(row) == 2:
            data.append(tuple(row))
        else:
            print("Skipping malformed row:", row)

conn = sqlite3.connect('vocab.db')
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS vocabulary")
c.execute(open("schema.sql").read())
c.executemany("INSERT INTO vocabulary (word, meaning) VALUES (?, ?)", data)
conn.commit()
conn.close()
