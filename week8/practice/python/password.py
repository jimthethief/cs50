from sys import exit

word = input("Enter a word: ")

with open("large", "r") as file:
    for entry in file.readlines():
        entry = entry.rstrip()
        print(f"Checking {entry}...")
        if entry == word:
            print(f"FOUND! Password is {entry}")
            exit(1)

print("Password not found.")