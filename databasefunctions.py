# 2.1
import sqlite3 as sql
import numpy as np

# 2.2
import encryptionfunctions as ef

# 2.3
def init_database():
    """Initialize the empty database. For development only.
    """
    conn = sql.connect("database.sqlite3")

    conn.execute("""CREATE TABLE Users(
                    ID          INTEGER PRIMARY KEY AUTOINCREMENT,
                    Username    TEXT                NOT NULL,
                    Email       TEXT                NOT NULL,
                    Passcode    TEXT                NOT NULL
                    );""")
    
    conn.execute("""CREATE TABLE Accounts(
                    ID              INTEGER PRIMARY KEY AUTOINCREMENT,
                    AccountOwner    TEXT                NOT NULL,
                    AccountName     TEXT                NOT NULL,
                    AccountPassword TEXT                NOT NULL
                    );""")
    
    conn.close()


# 2.4
def reset_database():
    """Empty the database. For development only.
    """
    conn = sql.connect("database.sqlite3")

    conn.execute("DROP TABLE Users;")
    conn.execute("DROP TABLE Accounts;")

    conn.close()
    

# 2.5
def is_username_unique(user_name: str) -> bool:
    """Checks if a username already exists in the database.

        Arguments:
            user_name (str): The username to check.
        
        Returns:
            A boolean for whether the username does exist in the database.
    """
    conn = sql.connect("database.sqlite3")
    cur = conn.cursor()

    # attempt to find all instances of the user_name
    entry = cur.execute("SELECT Username FROM Users WHERE Username=?", [user_name]).fetchall()

    conn.close()
    if entry != []:
        return False
    else:
        return True
    

# 2.6
def is_email_unique(email: str) -> bool:
    """Checks if an email already exists in the database.

        Arguments:
            email (str): The email to check.

        Returns:
            A boolean for whether the email does exist in the database.
    """
    conn = sql.connect("database.sqlite3")
    cur = conn.cursor()

    # attempt to find all instances of the email
    entry = cur.execute("SELECT Email FROM Users WHERE Email=?", [email]).fetchall()

    conn.close()
    if entry != []:
        return False
    else:
        return True


# 2.7
def is_account_name_unique(user_id: int, account_name: str) -> bool:
    """Checks if an account name is unique for a particular user.

        Arguments:
            user_id (int): A number corresponding to the user.
            account_name (str): The account name to check.

        Returns:
            A boolean for whether the user does have that account name.
    """
    user_id += 1

    conn = sql.connect("database.sqlite3")
    cur = conn.cursor()

    user_name = cur.execute(f"SELECT Username FROM Users WHERE ID=?", [user_id])
    user_name = user_name.fetchall()[0][0]

    # attempt to find all instances of the account name
    entry = cur.execute("SELECT AccountName FROM Accounts WHERE AccountName=? AND AccountOwner=?", [account_name, user_name]).fetchall()

    conn.close()
    if entry != []:
        return False
    else:
        return True


# 2.8
def add_user(user_name: str, user_email: str, user_passcode: str):
    """Create a user in the database from verified information.

        Arguments:
            user_name (str): The new user's username.
            user_email (str): The new user's email.
            user_passcode (str): The new user's passcode.
    """
    user_passcode = ef.encrypt_string(user_passcode)

    conn = sql.connect("database.sqlite3")

    conn.execute("INSERT INTO Users (Username,Email,Passcode) VALUES (?, ?, ?);", [user_name, user_email, user_passcode])

    conn.commit()
    conn.close()


# 2.9
def add_account_to_user(user_id: int, account_name: str, account_password: str):
    """Create an account in the database from verified information, corresponding to a user.

        Arguments:
            user_id (int): Integer corresponding to the user, used to set the user as the created account owner.
            account_name (str): The name of the new account to create.
            account_password (str): The password of the new account to create.
    """
    user_id += 1
    account_password = ef.encrypt_string(account_password)

    conn = sql.connect("database.sqlite3")
    cur = conn.cursor()

    user_name = cur.execute(f"SELECT Username FROM Users WHERE ID=?", [user_id])
    user_name = user_name.fetchall()[0][0]

    conn.execute("INSERT INTO Accounts (AccountOwner,AccountName,AccountPassword) VALUES (?, ?, ?);", [user_name, account_name, account_password])

    conn.commit()
    conn.close()


# 2.10
def set_user_passcode(user_id: int, passcode: str):
    """Change the passcode of a user in the database.

        Arguments:
            user_id (int): Integer corresponding to the user, used to select the correct user in the database.
            passcode (str): The new passcode.
    """
    user_id += 1
    passcode = ef.encrypt_string(passcode)

    conn = sql.connect("database.sqlite3")

    conn.execute("UPDATE Users SET Passcode=? WHERE ID=?", [passcode, user_id])

    conn.commit()
    conn.close()


# 2.11
def get_user_username(user_id: int) -> str:
    """Gets the username corresponding to a user id.

        Arguments:
            user_id (int): A number corresponding to a user.

        Returns:
            A string containing the username.
    """
    user_id += 1
    conn = sql.connect("database.sqlite3")
    cur = conn.cursor()

    username = cur.execute(f"SELECT Username FROM Users WHERE ID=?", [user_id]).fetchall()[0][0]
    
    conn.close()
    return username


# 2.12
def get_user_email(user_id: int) -> str:
    """Gets the email corresponding to a user id.

        Arguments:
            user_id (int): A number corresponding to a user.

        Returns:
            A string containing the email.
    """
    user_id += 1
    conn = sql.connect("database.sqlite3")
    cur = conn.cursor()

    email = cur.execute(f"SELECT Email FROM Users WHERE ID=?", [user_id]).fetchall()[0][0]
    
    conn.close()
    return email


# 2.13
def get_user_passcode(user_id: int) -> str:
    """Gets the passcode corresponding to a user id.

        Arguments:
            user_id (int): A number corresponding to a user.

        Returns:
            A string containing the passcode.
    """
    user_id += 1
    conn = sql.connect("database.sqlite3")
    cur = conn.cursor()

    passcode = cur.execute(f"SELECT Passcode FROM Users WHERE ID=?", [user_id]).fetchall()[0][0]
    
    conn.close()

    passcode = ef.decrypt_string(passcode)
    return passcode


# 2.14
def get_users() -> list:
    """Gets all users in the database.

        Returns:
            A list of all usernames.
    """
    conn = sql.connect("database.sqlite3")
    cur = conn.cursor()

    user_names = cur.execute("SELECT Username FROM Users").fetchall()

    conn.close()

    user_names = list(np.reshape(user_names, len(user_names)))

    return user_names


# 2.15
def get_user_accounts(user_id: int) -> list:
    """Gets all account names owned by a user.

        Arguments:
            user_id (int): An integer corresponding to a user.

        Returns:
            A list of account names.
    """
    user_id += 1
    conn = sql.connect("database.sqlite3")
    cur = conn.cursor()

    user_name = cur.execute(f"SELECT Username FROM Users WHERE ID=?", [user_id])
    user_name = user_name.fetchall()[0][0]

    accounts = cur.execute(f"SELECT AccountName FROM Accounts WHERE AccountOwner=?", [user_name]).fetchall()

    conn.close()

    accounts = list(np.reshape(accounts, len(accounts)))

    return accounts


# 2.16
def get_account_password(user_id: int, account_id: int) -> str:
    """Gets the password for an account.

        Arguments:
            user_id (int): An integer corresponding to a user.
            account_id (int): An integer corresponding to an account owned by a user.

        Returns:
            A string containing the account password.
    """
    user_id += 1
    conn = sql.connect("database.sqlite3")
    cur = conn.cursor()

    user_name = cur.execute(f"SELECT Username FROM Users WHERE ID=?", [user_id])
    user_name = user_name.fetchall()[0][0]

    password = cur.execute(f"SELECT AccountPassword FROM Accounts WHERE AccountOwner=?", [user_name])
    password = password.fetchall()[account_id][0]

    conn.close()

    password = ef.decrypt_string(password)

    return password


# 2.17
def set_account_password(user_id, account_id, password):
    """Change the password of an existing account in the database.

        Arguments:
            user_id (int): Integer corresponding to the user, used to select the correct username in the database.
            account_id (int): Integer corresponding to the account, used to select the correct account name in the database.
            password (str): The new password.
    """
    user_id += 1
    password = ef.encrypt_string(password)

    conn = sql.connect("database.sqlite3")
    cur = conn.cursor()

    user_name = cur.execute(f"SELECT Username FROM Users WHERE ID=?", [user_id])
    user_name = user_name.fetchall()[0][0]

    account_name = cur.execute(f"SELECT AccountName FROM Accounts WHERE AccountOwner=?", [user_name]).fetchall()[account_id][0]

    conn.execute("UPDATE Accounts SET AccountPassword=? WHERE AccountOwner=? AND AccountName=?", [password, user_name, account_name])

    conn.commit()
    conn.close()
