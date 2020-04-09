from cs50 import get_string
import sys
import re  # imported for split function


def countLetters(s):
    # return count of number of letters in a given string
    length = 0
    for i in s:
        if i.isalpha():
            length += 1
    return length


def countSentences(s):
    # splits string in list using specified separators '.?!' strip specified trailing chars to avoid new sentence
    length = re.split('[.!?]+', s.rstrip(".!?\"\'()"))
    # return number of items in length list
    return len(length)


def grade(l, s):
    # Coleman-Liau formula
    index = round(0.0588 * l - 0.296 * s - 15.8)
    # Print grade when provided with avg no. of letters per 100 words and avg no. of sentences per 100 words
    if index < 1:
        print("Before Grade 1")
    elif index > 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")


def main():
    text = get_string("Text: ")

    letterCount = countLetters(text)
    wordCount = len(text.split())
    sentenceCount = countSentences(text)

    avgLetters = (letterCount / wordCount) * 100
    avgSentences = (sentenceCount / wordCount) * 100
    grade(avgLetters, avgSentences)


if __name__ == "__main__":
    main()