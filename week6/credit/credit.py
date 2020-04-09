import cs50

# get card number from user
num = cs50.get_int("Number: ")

# convert number to list
numList = [int(x) for x in str(num)]
# counter starts at 2nd last of numList
curr = len(numList) - 1
# empty array for reversed numList
revList = []

while curr >= 0:
    # reverse order of numList
    revList.append(numList[curr])
    # change counter by -1
    curr -= 1
# empty list for evens
even = []
# empty list for odds
odd = []
# reset counter to 0th index
curr = 0

while curr <= len(revList) - 1:
    if curr % 2 is not 0:
        # add each num in revList with even index to even
        odd.append(revList[curr])
    else:
        # add each num in revList with odd index to odd
        even.append(revList[curr])
    # change counter by + 1
    curr += 1

# multiply each int in odd list by 2
for i in range(0, len(odd)):
    odd[i] *= 2


def convert(list):

    # convert integer list to string list
    s = [str(j) for j in list]

    # join list items using join()
    res = int("".join(s))

    return(res)


# run convert function on odd list
oddDigits = convert(odd)
# convert integer back to list of single digits
digitList = [int(x) for x in str(oddDigits)]
# add sum of digitList to sum of even list
sumOf = sum(digitList) + sum(even)

# check for card validity
if sumOf % 10 is not 0:
    print("INVALID")
    quit()

# validate number's length - is num >= 13 and <= 16 and not 14 then:
if len(numList) >= 13 and len(numList) <= 16 and len(numList) is not 14:
    # check if VISA
    if numList[0] == 4:
        print("VISA")
    # check if AMEX
    elif numList[0] == 3 and numList[1] >= 4 and numList[1] <= 7:
        print("AMEX")
    # check if MASTERCARD
    elif numList[0] == 5 and numList[1] >= 1 and numList[1] <= 5:
        print("MASTERCARD")
    else:
        print("INVALID")
else:
    print("INVALID")

