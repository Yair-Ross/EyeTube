# -*- coding: utf-8 -*-
import sqlite3


def create_table():
    conn = sqlite3.connect("test.db")
    print "Opened database successfully"

    conn.execute('''CREATE TABLE VIDEOS
           (ID INT PRIMARY KEY     NOT NULL,
           MOVIE_NAME     TEXT    NOT NULL,
           MOVIE_PATH     TEXT    NOT NULL,
           LEN            INT     NOT NULL,
           VIEWS          INT     NOT NULL,
           SCORE          REAL,
           HASH           TEXT    NOT NULL,
           PARTS          INT     NOT NULL,
           SIZE         REAL);''')
    print "Table created successfully"

    conn.close()


def insert_movie(id, name, path, len, views, score, hashf, parts, size):
    conn = sqlite3.connect('test.db')
    print "Opened database successfully";

    name = "'" + name + "'"
    path = "'" + path + "'"
    hashf = "'" + hashf + "'"

    conn.execute("INSERT INTO VIDEOS (ID,MOVIE_NAME,MOVIE_PATH,LEN,VIEWS,SCORE,HASH,PARTS,SIZE) \
          VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (id, name, path, len, views, score, hashf, parts, size));

    conn.commit()
    print "Records created successfully";
    conn.close()


def exists_in_base(param, value):
    conn = sqlite3.connect('test.db')
    print "Opened database successfully";
    a = conn.execute("SELECT EXISTS(SELECT 1 FROM VIDEOS WHERE %s='%s')" % (param, value)).fetchone()

    if a[0] != 0:
        print("Found!")
    else:
        print("Not found...")

    print "Search complete"
    conn.close()


def search_movie(name):
    conn = sqlite3.connect('test.db')
    cursor = conn.execute("SELECT ID, MOVIE_NAME, VIEWS, SCORE  from VIDEOS")

    return [(str(row[1]), row[2], row[3]) for row in cursor if name in str(row[1])]

    print "Operation done successfully";
    conn.close()

def get_movie(name):
    conn = sqlite3.connect('test.db')
    path = conn.execute("SELECT MOVIE_PATH FROM VIDEOS WHERE MOVIE_NAME='%s'" % (name)).fetchone()
    return path[0]


def main():
    #create_table()
    #insert_movie(8, "mashooshooshoo", "E:\\tmp\\path", 277, 3, 1, "53dfgfdgfded4ccd7d3b9195933c8", 133, 355000)
    #exists_in_base('HASH', '53dc0a1e33c70ed4ccd7d3b9195933c8')
    #print search_movie('mashoo')
    print get_movie('y7y7')
    '''conn = sqlite3.connect('test.db')
    print "Opened database successfully";

    conn.execute("DELETE from VIDEOS where ID=8;")
    conn.commit
    print "Total number of rows deleted :", conn.total_changes

    cursor = conn.execute("SELECT ID, MOVIE_NAME, VIEWS, SCORE  from VIDEOS")
    for row in cursor:
       print "ID = ", row[0]
       print "NAME = ", row[1]
       print "ADDRESS = ", row[2]
       print "SALARY = ", row[3], "\n"

    print "Operation done successfully";
    conn.close()'''



if __name__ == '__main__':
    main()