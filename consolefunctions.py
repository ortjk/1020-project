class EntryError(Exception):
    "Raised when input value is not usable"
    pass


def verify_new_user_values(username="", email ="", passcode=0) -> bool:
    if username != "" and email != "" and passcode != 0:
        return False
    return True


def create_new_user():
    """Prompts the user to enter the information to create a new user profile, adding the information to userdata.txt
    
    """
    with open("userdata.txt", "r") as file:
        data = file.read()
        data = data.split("\n")
        if len(data) < 4:
            data = ["", "", "", ""]

        # get input and verify that it is valid
        username = ""
        email = ""
        passcode = 0
        while verify_new_user_values(username, email, passcode):
            try:
                username = input("\nEnter the username for the new account: ")
                if len(username) < 4 or len(username) > 28:
                    print("Error. Username must be within 4-28 characters. Please try again with a different username.")
                    raise EntryError
                elif username in data[::2]:
                    print("Error. Username already registered. Please try again with a different username.")
                    raise EntryError
                email = input("Enter your email: ")
                if len(email) < 4:
                    print("Error. Email invalid. Please try again.")
                    raise EntryError
                elif email in data[1::2]:
                    print("Error. Email already registered. Please try again with a different email.")
                    raise EntryError
                passcode = int(input("Enter the 4-digit passcode: "))
                if passcode <= 999 or passcode > 9999:
                    print("Error. Passcode must be 4 digits. Please try again.")
                    raise EntryError

            
            except ValueError:
                print("Error, passcode must be numeric. Please try again.")
                username = ""
                email = ""
                passcode = 0

            except EntryError:
                username = ""
                email = ""
                passcode = 0
    
    # add verified input to file
    with open("userdata.txt", "a") as file:
        file.write(f"{username}\n{email}\n{passcode}\n")


def add_account_to_user(user_id):
    previous_file_data = ""
    with open("accounts.txt", "r") as file:
        previous_file_data = file.read()

    user_line = previous_file_data.split("\n")[user_id]

    while True:
        try:
            account_name = input("Enter the name for the new account: ")
            if len(account_name) < 1 or len(account_name) > 28 or ';' in account_name:
                print("Error. Invalid account name. Name must be less than 28 characters and not contain ';'")
                account_name = ""
                raise EntryError
            
            account_password = input("Enter the password for the new account: ")
            if len(account_password) < 1 or len(account_password) > 28 or ';' in account_password:
                print("Error. Invalid password. Password must be less than 28 characters and not contain ';'")
                account_password = ""
                raise EntryError
            
            user_line += f"{account_name};{account_password};"

            go_next = input("Would you like to enter another password? (y/n)").lower()
            if go_next != "y":
                break
                
        except EntryError:
            pass
        
    new_file_data = previous_file_data.split("\n")
    new_file_data[user_id] = user_line

    with open("accounts.txt", "w") as file:
        file.writelines(new_file_data)
