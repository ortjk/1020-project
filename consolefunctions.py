def verify_new_user_values(username="", email ="", password="", file_content="") -> bool:
    if username != "":
        return False
    return True


def create_new_user():
    with open("userdata.txt", "r") as file:
        # get input and verify that it is valid
        username = ""
        email = ""
        password = ""
        file_content = file.read().splitlines()
        while verify_new_user_values(username, email, password, file_content):
            try:
                username = input("\nEnter the username for the new account: ")
                email = input("Enter your email: ")
                password = int(input("Enter the password (must be numeric): "))

            except ValueError:
                print("Error, password must be numeric. Please try again.")
    
    # add verified input to file
    with open("userdata.txt", "a") as file:
        file.write(f"{username};{email};{password}\n")