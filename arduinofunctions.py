# 5.1
from oledmenu import *
# 5.2
import databasefunctions as dbf

# 5.3
def rotary_scroll(menu: OledMenu):
    """Continuously takes differential readings of the rotary potentiometer, and interacts with the OledMenu based on these readings. Ends when the button is pressed.

        Arguments:
            menu (OledMenu): The OledMenu object to interact with
    """
    # the 5 and -5 can be considered the "sensitivity" of the scrolling. A lower absolute value of these increases the sensitivity

    # take an initial reading
    rotary = analog_read(0)
    # until the button is pressed
    while not digital_read(6):
        # take a differential reading
        d_rotary = analog_read(0)
        # if the difference between the readings is greater than 5
        if d_rotary - rotary > 5:
            # then the rotary potentiometer is being turned to the left, so scroll up
            menu.scroll("up")
        # if the difference between the readings is less that -5
        elif d_rotary - rotary < -5:
            # then the rotary potentiometer is being turned to the right, so scroll down
            menu.scroll("down")
        # update the initial reading
        rotary = analog_read(0)


# 5.4
def convert_rotary_value(reading: int) -> int:
    """Convert the current rotary potentiometer reading to a number between -1 and 9, where the far left is low and far right is high.

        Arguments:
            reading (int): The current reading from the rotary potentiometer

        Returns:
            An integer from -1 to 9. Only returns -1 if rotary potentiometer is at its max reading (all the way to the left).
    """
    return 9 - (reading // 102)


# 5.5
def display_passcode_options(selected_value: int, entered_digits: str):
    """Display currently selected passcode value and previously selected digits on Arduino OLED screen.

        Arguments:
            selected_value (int): The currently selected value. Can be from -1 to 9.
            entered_digits (str): The values which have been entered previously.
    """
    oled_clear()
    # all displayed text follows the same format, with the previously entered digits at the top of the screen and selection in the middle.
    # If Exit is selected there is only a right arrow, and if 9 is selected there is only a left arrow.
    if selected_value == -1:
        oled_print(f"{entered_digits}_" + " " * (31 - len(entered_digits)) + f"    EXIT ->")
    elif selected_value == 9:
        oled_print(f"{entered_digits}_" + " " * (31 - len(entered_digits)) + f"    <- {selected_value}")
    else:
        oled_print(f"{entered_digits}_" + " " * (31 - len(entered_digits)) + f"    <- {selected_value} ->")


# 5.6
def user_select() -> int:
    """Start the process for the user to select their username on the Arduino. Instantiates an OledMenu object.

        Returns:
            An integer corresponding to the selected username. Starts at 0.
    """
    data = dbf.get_users()

    menu = OledMenu(data)

    print("Select your username on the Arduino using the rotary dial and hit the button to proceed.")
    rotary_scroll(menu)
    oled_clear()

    return menu.selected_option_id


# 5.7
def enter_passcode(user_id: int) -> bool:
    """Starts the process for the user to enter their passcode on the Arduino.

        Arguments:
            user_id (int): The number corresponding to the user. Used to find the passcode in the database.

        Returns:
            A boolean for whether the correct passcode was entered.
    """
    entered_digits = ""
    passcode = dbf.get_user_passcode(user_id)

    print(f'\nPlease enter the passcode using the rotary dial and button.')
    print("The current selected digit will be displayed on the screen, and the previously entered values will appear in the top left.")

    # 5.7 a
    selected_value = -2
    while True:
        if len(entered_digits) < 4:
            # get hovered dial value
            nvalue = convert_rotary_value(analog_read(0))
            # if the hovered value is different than the previously known hovered value, change the DISPLAYED hovered value
            if selected_value != nvalue:
                selected_value = nvalue
                display_passcode_options(selected_value, entered_digits)
                
            # 5.7 b
            # if the button is pressed
            if digital_read(6):
                # if exit is hovered then exit
                if selected_value == -1:
                    oled_clear()
                    return False

                # add the hovered value to the selected digits
                entered_digits += f"{nvalue}"

                # await button release
                while digital_read(6):
                    pass

                oled_clear()
                display_passcode_options(selected_value, entered_digits)

        # 5.7 c
        # all 4 digits have been entered
        else:
            oled_clear()
            # check if entered passcode is correct
            if entered_digits == passcode:
                # light the LED as user is signed in
                digital_write(4, True)
                return True
            else:
                print("Incorrect passcode entered.")
                return False
            

# 5.8
def signed_in_option_select() -> int:
    """Instantiates a OledMenu object for the signed in user options. User can view accounts, add an account, reset passcode, or sign out.

        Returns:
            An integer corresponding to the option selected. Starts at 0.
    """
    options = ["View Accounts", "Add Account", "Reset Passcode", "Sign Out"]

    menu = OledMenu(options)
    rotary_scroll(menu)
    oled_clear()

    # turn off the LED if the user wants to exit
    if menu.selected_option_id == menu.option_ids[-1]:
        digital_write(4, False)

    return menu.selected_option_id


# 5.9
def view_accounts_option_select(user_id) -> int:
    """Starts the process to display a list of the user's account's names on the Arduino. Creates a OledMenu object.

        Arguments:
            user_id (int): The number corresponding to the user. Used to find the accounts owned by the user in the database.

        Returns:
            An integer corresponding to the account name selected. Starts at 0.
    """
    data = dbf.get_user_accounts(user_id)

    # add the back option to the list of data
    if data == []:
        data = ["Back"]
    else:
        data += ["Back"]
    
    menu = OledMenu(data)
    rotary_scroll(menu)
    oled_clear()

    # if the last option (back) was selected, then go back
    if menu.selected_option_id == menu.option_ids[-1]:
        return -1

    return menu.selected_option_id


# 5.10
def view_password(user_id, account_id) -> bool:
    """Starts the process to display the selected account's password on the Arduino. Instantiates a OledMenu.

        Arguments:
            user_id (int): The number corresponding to the signed in user. Used to find the accounts owned by the user in the database.
            account_id (int): The number corresponding to the selected account. Used to find the password of the account selected in the database.
    
        Returns:
            A boolean corresponding to whether the user selected to edit the displayed password
    """
    # 5.10 a
    data = dbf.get_account_password(user_id, account_id)
    
    # add exit to options
    menu = OledMenu([data, "Edit", "Exit"])

    # 5.10 b
    while True:
        rotary_scroll(menu)
        # exit
        if menu.selected_option_id == menu.option_ids[-1]:
            break
        elif menu.selected_option_id == menu.option_ids[-2]:
            oled_clear()
            return True

    oled_clear()
    return False


# 5.11
def redirect_to_console():
    """Prints text on the Arduino to redirect the user to input information on the console.
    """
    oled_print("Use console to  enter           information")