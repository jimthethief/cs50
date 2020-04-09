import sys
import cs50

# check for only 2 arguments and exit if not
if len(sys.argv) is not 2:
    print("Usage: python vigenere.py k")
    sys.exit(1)

# check key is only made up of alphabetical characters and exit if not
if sys.argv[1].isalpha() == False:
    print("Usage: python vigenere.py k")
    sys.exit(1)

# convert character to positional integer value a/A = 0 b/B = 1 etc


def shift(c):
    if c.isupper() == True:
        c = ord(c) - 65
    else:
        c = ord(c) - 97
    return c


# store argument keys
keys = sys.argv[1]

keyList = []

# store each key in keyList
for i in keys:
    keyList.append(shift(i))

keyLength = len(keyList)

# get plaintext
plain = cs50.get_string("plaintext: ")

# define encode function


def encode(l, k):
    # convert letter to int from 0-26 store in val & return
    if l.isupper() == True:
        val = (((ord(l) - 65) + k) % 26) + 65
    else:
        val = (((ord(l) - 97) + k) % 26) + 97

    return chr(val)


# empty list for ciphered letters
ciphered = []
# set counter for keyList index
curr = -1

for i in plain:
    # + 1 to keyIndex for each letter of plain & return to 0th index once length of keyList reached
    keyIndex = 0
    if curr < len(keyList) - 1:
        curr += 1
        keyIndex += curr
    else:
        curr = 0
        keyIndex = 0
    # set key variable to current keyIndex
    key = keyList[keyIndex]
    # use encode function to cipher current letter by keyIndex
    c = encode(i, key)
    if i.isalpha() == True:
        ciphered.append(c)
    # if current char is not a letter do not cipher and reduce key index & counter by 1
    else:
        ciphered.append(i)
        curr -= 1
        keyIndex -= curr

# join ciphered list of letters into a single string & print
res = "".join(ciphered)
print(f"ciphertext: {res}")