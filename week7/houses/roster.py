from sys import argv
from sys import exit
from cs50 import SQL


def main():

    # check number of command-line arguments using sys.argv
    if len(argv) is not 2:
        print("Usage: python roster.py Gryffindor")
        exit(1)

    # specify database
    db = SQL("sqlite:///students.db")
    # save house to variable, capitalise in case entered in upper/lowercase
    house = argv[1].capitalize()

    # query database for all first, middle & last names + birth year of students in house variable
    # order query by last name, then first name
    rows = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", house)

    # print message if 0 results found i.e. house doesn't exist
    if len(rows) == 0:
        print("Sorry, we couldn't find any results for that house")
        exit(2)

    # iterate through each row returned by query
    for row in rows:
        # print first name
        print(row['first'], end=" ")
        # print middle name if it exists
        if row['middle'] is not None:
            print(row['middle'], end=" ")
        # print last name and birth year
        print(row['last'] + f", born {row['birth']}")


if __name__ == "__main__":
    main()
