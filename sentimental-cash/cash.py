from cs50 import get_float, get_string


def main():
    while True:
        cash = get_float("Change owed: ")
        if cash > 0:
            break

    cash = cash*100

    counter = 0

    while cash > 0:
        if (cash >= 25):

            cash = cash-25
            counter += 1

        elif (cash >= 10):

            cash = cash-10
            counter += 1

        elif (cash >= 5):

            cash = cash - 5
            counter += 1

        elif (cash >= 1):

            cash = cash - 1
            counter += 1

    print(counter)


main()

