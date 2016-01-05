import sqlite3

import Dijkstra

DATABASE = './database/connections.sqlite'

content = Dijkstra.read_file('miasta-kopia.txt')

link = []

def connect_db():
    return sqlite3.connect(DATABASE)

for line in content:
    with connect_db() as db:
            register = "INSERT into connections (start, finish, distance) VALUES ('{}', '{}', {})".format(line[0].strip(), line[2].strip(), float(line[1]))
            db.execute(register)
            db.commit()



