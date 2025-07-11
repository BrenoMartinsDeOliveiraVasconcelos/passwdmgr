import password_manager 
import consts
import os
import console


def register(manager: password_manager.PasswordManager):
    input_list = console.multiple_inputs([
        "Entity: ",
        "Username: ",
        "Password: "
    ])
    manager.register_password(input_list[0], input_list[1], input_list[2])


def get_password(manager: password_manager.PasswordManager):
    all_passwords = manager.get_list()
    passwords = all_passwords[0]

    entities = all_passwords[1]

    index = console.index_selection("ID", entities)

    password = passwords[index]

    output_list = [f"Entity: {password['entity']}", f"Username: {password['username']}", f"Password: {manager.get_password(password['id'])}"]

    console.output(output_list)
    console.enter_to_continue()


def delete_password(manager: password_manager.PasswordManager):
    all_passwords = manager.get_list()
    passwords = all_passwords[0]

    options = [f"{data['entity']} (User: {data['username']})" for data in passwords]

    index = console.index_selection("Password", options)
    manager.delete_password(passwords[index]["id"])


def modify_password(manager: password_manager.PasswordManager):
    all_passwords = manager.get_list()
    passwords = all_passwords[0]

    options = [f"{data['entity']} (User: {data['username']})" for data in passwords]

    index = console.index_selection("Password", options)

    console.output(["Press ENTER to keep unchanged"])
    keys = ["entity", "username", "password"]

    for key in keys:
        val = input(f"{key}: ")
        if val:
           passwords[index][key] = val

    manager.modify_password(passwords[index]["id"], passwords[index]["entity"], passwords[index]["username"], passwords[index]["password"])


def reset(manager: password_manager.PasswordManager):
    manager.reset()


def main() -> int:
    console.clear()
    master_password = input("Master key: ")
    try:
        manager = password_manager.PasswordManager(consts.DB_PATH, os.path.join(consts.PROGRAM_PATH, "key"), master_password.encode(consts.ENCODING))
    except password_manager.excepts.InvalidKey:
        console.log(2, "Invalid master key")
        return 1
    
    if manager.first_start:
        console.log(0, "Master key saved. All passwords will be encrypted and decrypted using it. Do not lose it.")
        console.enter_to_continue()
        console.clear()

    options = {
        "register": register,
        "get password": get_password,
        "delete password": delete_password,
        "modify password": modify_password,
        "reset": reset,
        "exit": "EXIT"
    }

    while True:
        console.clear()
        keys = [x for x in options.keys()]

        val = keys[console.index_selection("Option", keys)]

        if val == "exit":
            return 0

        options[val](manager)

    return 0