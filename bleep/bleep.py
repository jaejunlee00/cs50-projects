from cs50 import get_string
from sys import argv


def main():
    # first check if command line argument is properly given
    if (len(argv) != 2):
        print("Usage: python bleep.py dictionary")
        exit(1)

    words = set()
    # get string from a user and store each word as a string inside an array called msg
    msg = get_string("What message would you like to censor? ")
    msg = msg.split()
    # open the argv[1] text file for read
    file = open(argv[1], "r")
    # store each word in file as a string in an array called words
    for line in file:
        words.add(line.rstrip("\n"))
    # iterate over the word in msg and if the word inside msg exists in words, then iterate over the char of word and print *
    for word in msg:
        if word.lower() in words:
            for c in word:
                print("*", end="")
    # otherwise, just copy the word
        else:
            print(word, end="")
    # have a space in between each word or ****
        print(" ", end="")

    print()

    file.close()


if __name__ == "__main__":
    main()
