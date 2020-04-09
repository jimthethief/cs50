import csv
import sys


def storePatterns(csvFile):
    with open(csvFile) as file:
        reader = csv.reader(file)
        # store STRs in list
        patterns = list(reader)[0][1:]

    return patterns


def storeData(csvFile, data):
    with open(csvFile) as file:
        reader = csv.reader(file)
        # skip title row and store remaining rows into dictionary with name as key
        next(reader)
        for row in reader:
            data[row[0]] = row[1:]


def storeSequence(txtFile):
    # Load file  into memory, returning true if successful else false
    with open(txtFile, 'r') as file:
        sequence = file.read().replace('\n', '')
    return sequence


def grabber(seq, rep):
    # storage for indexes of matching patterns
    found = []
    # count for indexes of consecutive matching patterns
    count = 1
    # count for largest run of matching patterns
    largest = 0
    # loop through sequence
    for i in range(len(seq)):
        # use find function to locate elements that match rep // returns -1 if element doesn't match
        finder = seq.find(rep, i, i + len(rep))
        # if match is found - add index of match to found
        if finder != -1:
            found.append(finder)
    # if there is only a single occurence of pattern, return 1
    if len(found) == 1:
        return 1
    # loop through array of found elements and determine which are consecutive
    for j in range(len(found)-1):
        if found[j + 1] - found[j] == len(rep):
            # add to count if occurence is consecutive (index - next index isn't equal to length of pattern)
            count += 1
            if count > largest:
                largest = count
        else:
            # reset count if occurence of pattern not consecutive
            count = 1
    # return number of consecutive occurences
    return largest


def checker(dic, seq, patt):
    # set counter
    curr = -1
    # iterate through dictionary keys and values
    for key, value in dic.items():
        for i in value:
            patternIndex = 0
            # increase counter if end of pattern list hasn't been reached
            if curr < len(patt) - 1:
                curr += 1
                patternIndex += curr
                # check each key value in dictionary against each pattern for match
                if int(i) != grabber(seq, patt[patternIndex]):
                    # if value doesn't match current STR pattern, delete entry from dictionary as no match & return 0
                    del dic[key]
                    return 0
            else:
                curr = 0
                patternIndex = 0

    # return 1 if match is found
    return 1


def main():

    # Accept file paths to csv/text files via command line (if argv length is incorrect, exit with status 1)
    if len(sys.argv) is not 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    patterns = storePatterns(sys.argv[1])
    sequence = storeSequence(sys.argv[2])
    data = {}
    storeData(sys.argv[1], data)

    # use checker function to check for matches repeatedly, deleting keys until final dictionary item
    while True:
        # break once final dictionary key is reached
        if len(data.items()) == 1:
            break
        checker(data, sequence, patterns)

    # check final dictionary key is match and print if so, else print no match
    if checker(data, sequence, patterns) == 1:
        for key in data:
            print(key)
        return 0
    else:
        print("No Match")
        return 0


if __name__ == "__main__":
    main()