# TODO
from sys import argv
from cs50 import SQL

# check correct usage
if len(argv) != 2:
    print("Usage Error - python roster.py Gryffindor");
    exit()

# create database
db = SQL("sqlite:///students.db")

# use db.execute to select rows from the database
house = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last DESC, first", argv[1])

print(house)

# check if middle name exists
for student in house:
    if student['middle'] != None:
        print(f"{student['first']} {student['middle']} {student['last']}, born {student['birth']}")
    else:
        print(f"{student['first']} {student['last']}, born {student['birth']}")