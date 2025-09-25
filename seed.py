import sqlite3

data = [
    ("elucidate", "make (something) clear; explain", "She asked him to elucidate his remarks."),
    ("gregarious", "fond of company; sociable", "He was a popular and gregarious man."),
    ("cogent", "clear, logical, and convincing", "Her argument was both cogent and compelling."),
]

conn = sqlite3.connect('vocab.db') # makes the connection 
c = conn.cursor() # creates the tunnel between the database and the program, opens the door so to say 
c.execute("DROP TABLE IF EXISTS vocabulary") # commands similar to a CRUD method 
c.execute(open("schema.sql").read())
c.executemany("INSERT INTO vocabulary (word, meaning, example) VALUES (?, ?, ?)", data)
conn.commit()
conn.close()