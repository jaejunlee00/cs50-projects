from cs50 import get_int, get_string


def main():
    # Keep asking until the user gives a positive int
    while True:
        h = get_int("Height: ")
        if h > 0 and h < 9:
            break
    counter1 = 1
    counter2 = h-counter1
    # print empty space first and then hash
    for i in range(h):
        for j in range(h-counter1):
            print(" ", end="")
        # after each iteration, there's gonna be less empty space
        counter1 += 1
        for k in range(h-counter2):
            print("#", end="")
        # after each iteration, there's gonna be more hash space
        counter2 -= 1
        print()


main()