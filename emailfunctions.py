import smtplib as sm
import ssl
import os
from dotenv import load_dotenv

import databasefunctions as dbf

def send_password_to_user(user_id: int):
    """Sends an email to a specefied user's email.

        Arguments:
            user_id (int): A number corresponding to a user in the database.
    """
    port = 465

    # get email sender login information from the .env file
    load_dotenv()
    sender_email = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")

    # get receiver email data from the database
    receiver_username = dbf.get_user_username(user_id)
    receiver_email = dbf.get_user_email(user_id)
    receiver_passcode = dbf.get_user_passcode(user_id)

    message = f"Hello {receiver_username},\n\nYour passcode is {receiver_passcode}"

    context = ssl.create_default_context()

    # login and send the email
    with sm.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        