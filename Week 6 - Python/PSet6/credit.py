from cs50 import get_int


def main():
    card_number = get_int("Number: ")

    if valid_number(card_number):
        card_type = check_type(card_number)
        print(f"Card type: {card_type}")
    else:
        print("INVALID")


def valid_number(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]

    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)

    for d in even_digits:
        checksum += sum(digits_of(d * 2))

    return checksum % 10 == 0


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
        return "INVALID"


main()
