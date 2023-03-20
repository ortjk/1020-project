import consolefunctions as cf
import arduinofunctions as af
import emailfunctions as ef

while True:
    try:
        print("Welcome to the password manager!\n1) Sign into existing user\n2) Create new user\n3) Forgot user password\n4) Exit")
        choice = int(input("Enter your choice (1, 2, 3, or 4): "))

        # sign into user
        if choice == 1:
            user_id = af.user_select()
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
                        af.redirect_to_console()
                        cf.reset_user_password(user_id)

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

        elif choice == 3:
            print("Please select your username using the arduino")
            user_id = af.user_select()
            ef.send_password_to_user(user_id)
            print("You have been sent an email containing your password.\n")
        
        # exit
        else:
            break

    except ValueError:
        print("Error. Invalid Input. Please Try Again.\n")
