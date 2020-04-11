from sys import argv
from sys import exit
import csv
from cs50 import SQL
from re import split


def main():

    # check number of command-line arguments using sys.argv + check file is CSV file w/ endswith
    if len(argv) is not 2 or argv[1].endswith(".csv") == False:
        print("Usage: python import.py file.csv")
        exit(1)

    # specify database
    db = SQL("sqlite:///students.db")

    # open csv file
    with open(argv[1], "r") as students:
        # create DictReader
        reader = csv.DictReader(students)

        # iterate over CSV file
        for row in reader:
            # store each name in list using " " as separator
            name = row["name"].split(" ")
            # store each house in variable
            house = row["house"]
            # store birth date in variable as integer
            birth = int(row["birth"])

            # store names in first, middle, last - if student has only 2 names use "None" for middle name
            if len(name) == 2:
                first, middle, last = name[0], None, name[1]
            else:
                first, middle, last = name[0], name[1], name[2]

            # use db.execute to INSERT each row into the students.db table
            db.execute("INSERT INTO students (id, first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?, ?)",
                       None, first, middle, last, house, birth)


if __name__ == "__main__":
    main()
