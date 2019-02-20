from cs50 import get_string, get_int
from sys import argv


def main():

    while True:
        if (int(argv[1]) > -1):
            break

    if (len(argv) != 2):
        return False

    plaintext = get_string("Plaintext: ")
    ciphertext = []

    A = ord('A')
    a = ord('a')

    for c in plaintext:
        if (c.isupper):
            c = ord(c) - A
            c = c + int(argv[1]) % 26
            c = chr(c + A)
            ciphertext.append(c)

        elif (c.islower):
            c = ord(c) - a
            c = c + int(argv[1]) % 26
            c = chr(c + a)
            ciphertext.append(c)

    print(f"ciphertext: {''.join(ciphertext)}")


main()
