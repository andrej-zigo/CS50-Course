from cs50 import get_int


def main():
    n = pyramid_height()
    if n is not None:
        pyramid_print(n)


def pyramid_height():
    while True:
        n = get_int("Height: ")
        if n > 0 and n < 9:
            return n
        else:
            print("Wrong usage. Use only integers between 1 and 8.")


def pyramid_print(n):
    for i in range(1, n + 1):
        left_half = " " * (n - i) + "#" * i
        right_half = "#" * i
        print(f"{left_half}  {right_half}")


main()
