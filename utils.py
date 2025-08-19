import os
import platform
from datetime import datetime


def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')


def display_banner():
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    PAYROLL MANAGEMENT SYSTEM                  ║
    ║                      Console Application                      ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def get_valid_input(prompt, valid_choices=None):
    while True:
        user_input = input(prompt).strip()

        if valid_choices is None:
            return user_input

        if user_input in valid_choices:
            return user_input
        else:
            print(f"Invalid input. Please choose from: {', '.join(valid_choices)}")


def get_valid_number(prompt, min_value=None, max_value=None):
    while True:
        try:
            number = float(input(prompt).strip())

            if min_value is not None and number < min_value:
                print(f"Number must be at least {min_value}")
                continue

            if max_value is not None and number > max_value:
                print(f"Number must be at most {max_value}")
                continue

            return number
        except ValueError:
            print("Please enter a valid number.")


def get_valid_date(prompt):
    while True:
        date_str = input(prompt).strip()

        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


def format_currency(amount):
    return f"${amount:,.2f}"


def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')
    except:
        return date_str


def center_text(text, width=60):
    return text.center(width)


def create_separator(char='-', length=60):
    return char * length


def pause():
    input("\nPress Enter to continue...")