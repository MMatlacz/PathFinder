import sqlite3

# TODO: change this file to use filename from command line

DATABASE = './database/connections.sqlite'


def read_file(filename):
    content = []

    with open(filename) as f:
        lines = f.readlines()
        f.close()
    for line in lines:
        path = line.split(";")
        content.append(path)
    return content


content = read_file('miasta-kopia.txt')

link = []


# TODO: use sqlAlchemy


def connect_db():
    return sqlite3.connect(DATABASE)


for line in content:
    with connect_db() as db:
        register = "INSERT into connections (start, destination, distance) VALUES ('{}', '{}', {})".format(
                line[0].strip(),
                line[2].strip(),
                float(line[1]))
        db.execute(register)
        db.commit()
