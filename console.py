import os


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def log(severity: int, message: str):
    severity_list = ["INFO", "WARNING", "ERROR"]

    print(f"[{severity_list[severity]}] {message}")


def output(message: list):
    for line in message:
        print(line)


def index_selection(message: str, iterable: list):
    user_input = -1

    for index, item in enumerate(iterable):
        print(f"[{index+1}] {item}")

    while user_input not in range(len(iterable)):
        try:
            user_input = int(input(f"{message}: ")) - 1
        except ValueError:
            continue

    return user_input


def enter_to_continue():
    input("Press enter to continue...")


def multiple_inputs(message: list, allow_empty: bool = False) -> list:
    input_list = []
    for line in message:
        user_input = input(line)

        if not allow_empty and not user_input:
            while not user_input:
                log(2, "Input cannot be empty")
                user_input = input(line)

        input_list.append(user_input)

    return input_list
