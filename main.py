import consolefunctions as cf
import arduinofunctions as af

while True:
    try:
        print("Welcome to the password manager!\n1) Sign into your account\n2) Create a new account\n3) Exit")
        choice = int(input("Enter your choice (1, 2, or 3): "))

        # sign into account
        if choice == 1:
            user_id = af.user_select() + 1
            print(f"Picked user number {user_id}")

        # create new account
        elif choice == 2:
            cf.create_new_user()
            print("User created successfully. Returning to the main menu...\n")
        
        # exit
        else:
            break

    except ValueError:
        print("Error. Invalid Input. Please Try Again.\n")
