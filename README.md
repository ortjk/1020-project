# 1020-project

This is a project for the class "ENGI 1020 - Introduction to programming", by Thomas Porter and Ethan Smith. It is a password manager created using Python which uses a Grove Beginner Kit for Arduino. 

Generally, the console on the computer running the code is used for inputting user information such as usernames and passwords. This information is stored in a SQLite database. The kit is used to sign in and view the information. Sensitive user information such as passwords are encrypted using Fernet, with the hash key stored locally in a .env file. 
