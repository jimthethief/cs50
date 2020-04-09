from cs50 import get_string
import sys

# function to load file and save each line of file into specified word set


def load(fileName, wordSet):
    # Load file  into memory, returning true if successful else false
    file = open(fileName, "r")
    for line in file:
        wordSet.add(line.rstrip("\n"))
    file.close()
    return True


def check(word, wordSet):
    # Return true if word is in word set else false
    return word in wordSet
    

def main():

    # Accept file path to text fine via command line (if no argv is entered exit with status 1)
    if len(sys.argv) is not 2:
        print("Usage: python bleep.py dictionary")
        sys.exit(1)

    # Open and read file, storing each line in a Python data structure (i.e list/set) for access
    bannedWords = set()
    load(sys.argv[1], bannedWords)

    # Prompt user for message
    message = get_string("What message would you like to censor?\n")
    # Split message into component words using split method - store in list
    words = message.split()

    # empty list for censored message
    censored = []
    # Iterate over words list to see if entries match words in banned list (case insensitive)
    for i in words:
        if check(i.lower(), bannedWords) == True:
            # censor banned words
            i = '*' * len(i)
            censored.append('*' * len(i))
        else:
            # leave non-banned words uncensored
            censored.append(i)

    # join censored list into string
    res = " ".join(censored)
    print(f"{res}")

    return 0


if __name__ == "__main__":
    main()
