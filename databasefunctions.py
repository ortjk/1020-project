import sqlite3 as sql
import numpy as np

import encryptionfunctions as ef

def init_database():
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


def reset_database():
    conn = sql.connect("database.sqlite3")

    conn.execute("DROP TABLE Users;")
    conn.execute("DROP TABLE Accounts;")

    conn.close()
    

def is_username_unique(user_name: str) -> bool:
    conn = sql.connect("database.sqlite3")
    cur = conn.cursor()

    entry = cur.execute(f"SELECT Username FROM Users WHERE Username='{user_name}'").fetchall()

    conn.close()
    if entry != []:
        return False
    else:
        return True
    

def is_email_unique(email: str) -> bool:
    conn = sql.connect("database.sqlite3")
    cur = conn.cursor()

    entry = cur.execute(f"SELECT Email FROM Users WHERE Email='{email}'").fetchall()

    conn.close()
    if entry != []:
        return False
    else:
        return True


def add_user(user_name: str, user_email: str, user_passcode: str):
    user_passcode = ef.encrypt_string(user_passcode)

    conn = sql.connect("database.sqlite3")

    conn.execute(f"INSERT INTO Users (Username,Email,Passcode) VALUES ('{user_name}', '{user_email}', '{user_passcode}');")

    conn.commit()
    conn.close()


def add_account_to_user(user_id: int, account_name: str, account_password: str):
    user_id += 1
    account_password = ef.encrypt_string(account_password)

    conn = sql.connect("database.sqlite3")
    cur = conn.cursor()

    user_name = cur.execute(f"SELECT Username FROM Users WHERE ID={user_id}")
    user_name = user_name.fetchall()[0][0]

    conn.execute(f"INSERT INTO Accounts (AccountOwner,AccountName,AccountPassword) VALUES ('{user_name}', '{account_name}', '{account_password}');")

    conn.commit()
    conn.close()


def set_user_passcode(user_id: int, passcode: str):
    user_id += 1
    passcode = ef.encrypt_string(passcode)

    conn = sql.connect("database.sqlite3")

    conn.execute(f"UPDATE Users SET Passcode='{passcode}' WHERE ID={user_id}")

    conn.commit()
    conn.close()


def get_user_username(user_id: int) -> str:
    user_id += 1
    conn = sql.connect("database.sqlite3")
    cur = conn.cursor()

    username = cur.execute(f"SELECT Username FROM Users WHERE ID={user_id}").fetchall()[0][0]
    
    conn.close()
    return username


def get_user_email(user_id: int) -> str:
    user_id += 1
    conn = sql.connect("database.sqlite3")
    cur = conn.cursor()

    email = cur.execute(f"SELECT Email FROM Users WHERE ID={user_id}").fetchall()[0][0]
    
    conn.close()
    return email


def get_user_passcode(user_id: int) -> str:
    user_id += 1
    conn = sql.connect("database.sqlite3")
    cur = conn.cursor()

    passcode = cur.execute(f"SELECT Passcode FROM Users WHERE ID={user_id}").fetchall()[0][0]
    
    conn.close()

    passcode = ef.decrypt_string(passcode)
    return passcode


def get_users() -> list:
    conn = sql.connect("database.sqlite3")
    cur = conn.cursor()

    user_names = cur.execute("SELECT Username FROM Users").fetchall()

    conn.close()

    user_names = list(np.reshape(user_names, len(user_names)))

    return user_names


def get_user_accounts(user_id: int) -> list:
    user_id += 1
    conn = sql.connect("database.sqlite3")
    cur = conn.cursor()

    user_name = cur.execute(f"SELECT Username FROM Users WHERE ID={user_id}")
    user_name = user_name.fetchall()[0][0]

    accounts = cur.execute(f"SELECT AccountName FROM Accounts WHERE AccountOwner='{user_name}'").fetchall()

    conn.close()

    accounts = list(np.reshape(accounts, len(accounts)))

    return accounts


def get_account_password(user_id: int, account_id: int) -> str:
    user_id += 1
    conn = sql.connect("database.sqlite3")
    cur = conn.cursor()

    user_name = cur.execute(f"SELECT Username FROM Users WHERE ID={user_id}")
    user_name = user_name.fetchall()[0][0]

    password = cur.execute(f"SELECT AccountPassword FROM Accounts WHERE AccountOwner='{user_name}'")
    password = password.fetchall()[account_id][0]

    conn.close()

    password = ef.decrypt_string(password)

    return password

