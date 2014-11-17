#!python/bin/python

import csv
import os, os.path
import sqlite3
import sys

conn = sqlite3.connect('./data/names.db')
db = conn.cursor()

def create_table():
    db.execute("DROP TABLE IF EXISTS names;")
    db.execute('''
        CREATE TABLE names (
            name        TEXT NOT NULL,
            gender      TEXT NOT NULL,
            year        INTEGER NOT NULL,
            rank        INTEGER NOT NULL,
            count       INTEGER NOT NULL
        );
    ''')

def load_names():
    for path in os.listdir('./data'):
        if path[-3:] == 'txt':
            with open(os.path.join('./data', path)) as f:
                r = csv.reader(f)
                year = int(path[3:-4])
                sys.stdout.write("Year: %s\r" % (year))
                sys.stdout.flush()
                for i, row in enumerate(r):
                    db.execute("INSERT INTO names VALUES ('%s', '%s', '%s', '%s', '%s');" % (row[0], row[1], year, i, row[2]))

if __name__ == '__main__':
    create_table()
    load_names()
    db.execute('CREATE INDEX namerank_idx ON names(name,rank);')
    db.execute('CREATE INDEX nameyear_idx ON names(name,year);')
    db.execute('CREATE INDEX namegender_idx ON names(name,gender);')
    conn.commit()
    conn.close()
