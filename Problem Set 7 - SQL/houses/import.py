# TODO
from sys import argv
from csv import reader, DictReader
from cs50 import SQL

if len(argv) != 2:
    print("Usage Error - python import.py characters.csv");
    exit()

# create database
db = SQL("sqlite:///students.db")

# use csv.reader
with open(argv[1], "r") as file:
    csvreader = reader(file)

    # iterate over each row in file
    for row in csvreader:

        # skip the first row
        if row[0] == 'name':
            continue

        # split the name into two (or three) separate strings
        name = row[0].split()

        # if the student has a middle name, insert it
        if len(name) == 3:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)", name[0], name[1], name[2], row[1], row[2])

        # else insert null
        else:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)", name[0], None, name[2], row[1], row[2])