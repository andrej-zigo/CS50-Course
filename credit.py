from cs50 import get_int
import re


def main():
    card_number = get_int("Number: ")

    if valid_number(card_number):
        card_type = check_type(card_number)
        print(f"Card type: {card_type}")
    else:
        print("INVALID")


def valid_number(card_number):
    if card_number > 0:
        total = 0
        digits = [int(digit) for digit in str(card_number)[::-1]]

        for i, digit in enumerate(digits):
            if i % 2 == 1:
                digit *= 2
                if digit > 9:
                    digit = digit // 10 + digit % 10
                total += digit

        return total % 10 == 0

    return False


def check_type(card_number):
    card_number_str = str(card_number)
    if len(card_number_str) == 15 and (
        card_number_str.startswith("34") or card_number_str.startswith("37")
    ):
        return "AMEX"
    elif len(card_number_str) == 16 and 51 <= int(card_number_str[:2]) <= 55:
        return "MASTERCARD"
    elif (
        len(card_number_str) == 13
        or len(card_number_str) == 16
        and card_number_str.startswith("4")
    ):
        return "VISA"
    else:
        return "Unknown"


main()
