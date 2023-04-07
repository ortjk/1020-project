# 7.1 - 7.3
import consolefunctions as cf
import arduinofunctions as af
import emailfunctions as emf

# 7.4
# 7.4 a
while True:
    # 7.4 b
    try:
        # 7.4 c
        print("Welcome to the password manager!\n1) Sign into existing user\n2) Create new user\n3) Forgot user password\n4) Exit")
        choice = int(input("Enter your choice (1, 2, 3, or 4): "))

        # 7.4 d
        # sign into user
        if choice == 1:
            user_id = af.user_select()
            # 7.4 e
            if af.enter_passcode(user_id):
                while True:
                    submenu = af.signed_in_option_select()
                    # 7.4 f
                    if submenu == 0:
                        # 7.4 g
                        # view accounts
                        account_id = af.view_accounts_option_select(user_id)
                        if account_id != -1:
                            edit_password = af.view_password(user_id, account_id)
                            if edit_password:
                                af.redirect_to_console()
                                cf.edit_account_password(user_id, account_id)

                    # 7.4 h
                    elif submenu == 1:
                        # add new account
                        af.redirect_to_console()
                        cf.add_account_to_user(user_id)

                    # 7.4 i
                    elif submenu == 2:
                        # go into password reset
                        af.redirect_to_console()
                        cf.edit_user_password(user_id)

                    # 7.4 j
                    elif submenu == 3:
                        # exit
                        break

            else:
                af.redirect_to_console()

        # 7.4 k
        # create new user
        elif choice == 2:
            cf.create_new_user()
            print("User created successfully. Returning to the main menu...\n")

        # 7.4 l
        # send email with passcode
        elif choice == 3:
            print("Please select your username using the arduino")
            user_id = af.user_select()
            emf.send_password_to_user(user_id)
            print("You have been sent an email containing your passcode.\n")
            
        # 7.4 m
        # exit
        else:
            break

    except ValueError:
        print("Error. Invalid Input. Please Try Again.\n")
