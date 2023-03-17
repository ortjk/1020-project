import smtplib as sm
import ssl
import os
from dotenv import load_dotenv

def send_password_to_user(user_id):
    port = 465

    load_dotenv()
    sender_email = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")


    receiver_email = ""
    message = ""
    with open("userdata.txt", "r") as file:
        # get data
        data = file.read().split("\n")
        usernames = data[::3]
        emails = data[1::3]
        passwords = data[2::3]

        receiver_email = emails[user_id]
        message = f"Hello {usernames[user_id]},\n\nYour password is {passwords[user_id]}"

    context = ssl.create_default_context()

    with sm.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        