import regex as re
import maskpass

import databasefunctions as dbf

class EntryError(Exception):
    "Raised when input value is not usable"
    pass


def validate_email(email_address: str) -> bool:
    """Check using regex if the string resembles the form of an email address.

        Arguments:
            email_address (str): The prospective email address.

        Returns:
            A boolean for whether email_address resembles the form of an email address.
    """
    match = re.match(r"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$", email_address)
  
    return bool(match)


def create_new_user():
    """Prompts the user to enter the information neede to create a new user profile, adding the verified information to the database.
    """
    username = ""
    email = ""
    passcode = ""
    while True:
        try:
            username = input("\nEnter the username for the new account: ")
            if len(username) < 4 or len(username) > 28 or username[0] == " ":
                print("Error. Username must be within 4-28 characters. Please try again with a different username.")
                raise EntryError
            elif not dbf.is_username_unique(username):
                print("Error. Username already registered. Please try again with a different username.")
                raise EntryError

            email = input("Enter your email: ")
            if not validate_email(email) or " " in email:
                print("Error. Invalid email address. Please try again.")
                raise EntryError
            elif not dbf.is_email_unique(email):
                print("Error. Email already registered. Please try again with a different email.")
                raise EntryError
            
            # uses maskpass to hide digits entered
            passcode = maskpass.askpass(prompt="Enter the 4-digit passcode: ", mask="*")
            int(passcode)
            if len(passcode) != 4 or passcode[0] == " " or passcode[-1] == " ":
                print("Error. Passcode must be 4 digits. Please try again.")
                raise EntryError
            
            break

        except ValueError:
            print("Error, passcode must be numeric. Please try again.")

        except EntryError:
            pass

    # add verified input to file
    dbf.add_user(username, email, passcode)


def add_account_to_user(user_id: int):
    """Prompts the user to enter the information to add an account to their user, adding the verified information to the database.

        Arguments:
            user_id (int): The number corresponding to the user's account. Used to link the created account with their user.
    """
    account_name = ""
    account_password = ""
    while True:
        try:
            account_name = input("\nEnter the name for the new account: ")
            if len(account_name) < 1 or len(account_name) > 28 or ';' in account_name:
                print("Error. Invalid account name. Name must be less than 28 characters and not contain ';'")
                account_name = ""
                raise EntryError
            if not dbf.is_account_name_unique(user_id, account_name):
                print("Error. Account name is not unique.")
                raise EntryError
            
            account_password = maskpass.askpass(prompt="Enter the password for the new account: ", mask="*")
            if len(account_password) < 1 or len(account_password) > 28 or ';' in account_password:
                print("Error. Invalid password. Password must be less than 28 characters and not contain ';'")
                account_password = ""
                raise EntryError

            dbf.add_account_to_user(user_id, account_name, account_password)
            go_next = input("Would you like to add another account? (y/n) ").lower()
            if go_next != "y":
                break
                
        except EntryError:
            pass
        

def edit_user_password(user_id: int):
    """Prompts the user to enter a new passcode for their user. Adds the verified 4-digit passcode to the database.

        Arguments:
            user_id (int): The number corresponding to the user. Used to change the correct user's passcode in the database.
    """
    print("\nChanging passcode.")

    passcode = ""
    while True:
        try:
            passcode = maskpass.askpass(prompt="Please enter the new 4-digit passcode: ", mask="*")
            int(passcode)
            if len(passcode) != 4 or passcode[0] == " " or passcode[-1] == " ":
                print("Error. Passcode must be 4 digits. Please try again.")
                raise EntryError

            break

        except ValueError:
            print("Error, passcode must be numeric. Please try again.")

        except EntryError:
            pass

    dbf.set_user_passcode(user_id, passcode)

    print("Password reset successful. Please continue input on the Arduino.")
    

def edit_account_password(user_id, account_id):
    """Prompts the user to enter a new password for their account. Adds the verified password to the database.

        Arguments:
            user_id (int): A number corresponding to the user. 
            account_id (int): A number corresponding to the account which needs its password changed.
    """
    print("\nChanging password.")

    new_account_password = ""
    while True:
        try:
            new_account_password = maskpass.askpass(prompt="Enter the new password for the account: ", mask="*")
            if len(new_account_password) < 1 or len(new_account_password) > 28 or ';' in new_account_password:
                print("Error. Invalid password. Password must be less than 28 characters and not contain ';'")
                new_account_password = ""
                raise EntryError
            
            break

        except EntryError:
            pass
    
    dbf.set_account_password(user_id, account_id, new_account_password)
