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
