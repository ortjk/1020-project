import consolefunctions as cf
import arduinofunctions as af

while True:
    try:
        print("Welcome to the password manager!\n1) Sign into your account\n2) Create a new account\n3) Exit")
        choice = int(input("Enter your choice (1, 2, or 3): "))

        # sign into user
        if choice == 1:
            user_id = af.user_select()
            print(f"Selected user number {user_id + 1}")
            if af.enter_passcode(user_id):
                while True:
                    submenu = af.signed_in_option_select()
                    if submenu == 0:
                        # view accounts
                        account_id = af.view_accounts_option_select(user_id)
                        if account_id != -1:
                            af.view_password(user_id, account_id)

                    elif submenu == 1:
                        # add new account
                        af.redirect_to_console()
                        cf.add_account_to_user(user_id)

                    elif submenu == 2:
                        # go into password reset
                        pass

                    elif submenu == 3:
                        # exit
                        break

            else:
                af.redirect_to_console()
                print("Incorrect password entered. Redirecting to main menu...\n")

        # create new user
        elif choice == 2:
            cf.create_new_user()
            print("User created successfully. Returning to the main menu...\n")
        
        # exit
        else:
            break

    except ValueError:
        print("Error. Invalid Input. Please Try Again.\n")
