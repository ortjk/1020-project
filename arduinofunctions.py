from oledmenu import *

def rotary_scroll(menu):
    rotary = analog_read(0)
    while not digital_read(6):
        d_rotary = analog_read(0)
        if d_rotary - rotary > 5:
            menu.scroll("up")
        elif d_rotary - rotary < -5:
            menu.scroll("down")
        
        rotary = analog_read(0)
    
    oled_clear()


def convert_rotary_value(reading: int) -> int:
    return 9 - (reading // 102)


def display_passcode_options(selected_value, entered_digits):
    oled_clear()
    if selected_value == -1:
        oled_print(f"{entered_digits}_" + " " * (31 - len(entered_digits)) + f"    EXIT ->")
    elif selected_value == 9:
        oled_print(f"{entered_digits}_" + " " * (31 - len(entered_digits)) + f"    <- {selected_value}")
    else:
        oled_print(f"{entered_digits}_" + " " * (31 - len(entered_digits)) + f"    <- {selected_value} ->")


def user_select() -> int:
    data = ""
    with open("userdata.txt", "r") as file:
        data = file.read()
        # read every 3rd line, starting at the first
        data = data.split("\n")[:-1:3]

    menu = OledMenu(data)

    print("Select your username on the Arduino using the rotary dial and hit the button to proceed.")
    rotary_scroll(menu)

    return menu.selected_option_id


def enter_passcode(user_id) -> bool:
    entered_digits = ""
    passcode = 0
    with open("userdata.txt", "r") as file:
        data = file.read()
        passcode = data.split("\n")[2:-1:3][user_id]

        user = data.split("\n")[:-1:3][user_id]
        print(f'\nPlease enter the passcode for user "{user}" using the rotary dial and button.')
        print("The current selected digit will be displayed on the screen, and the previously entered values will appear in the top left.")

    selected_value = -2
    while True:
        if len(entered_digits) < 4:
            # get hovered dial value
            nvalue = convert_rotary_value(analog_read(0))
            if selected_value != nvalue:
                selected_value = nvalue
                display_passcode_options(selected_value, entered_digits)
                
            if digital_read(6):
                if selected_value == -1:
                    oled_clear()
                    return False

                entered_digits += f"{nvalue}"

                while digital_read(6):
                    pass

                oled_clear()
                display_passcode_options(selected_value, entered_digits)

        else:
            oled_clear()
            if entered_digits == passcode:
                digital_write(4, True)
                return True
            else:
                return False
            

def signed_in_option_select():
    options = ["View Accounts", "Add Account", "Reset Passcode", "Sign Out"]

    menu = OledMenu(options)
    rotary_scroll(menu)

    if menu.selected_option_id == menu.option_ids[-1]:
        digital_write(4, False)

    return menu.selected_option_id


def view_accounts_option_select(user_id) -> int:
    data = ""
    with open("accounts.txt", "r") as file:
        data = file.read()
        # split account list by lines, and isolate user's accounts
        data = data.split("\n")[user_id][:-1]
        # split account names and passwords into seperate lists, and isolate names
        data = data.split(";")[::2]

    print(data)
    if data == [""]:
        data = ["Back"]
    else:
        data += ["Back"]
    
    menu = OledMenu(data)
    rotary_scroll(menu)

    if menu.selected_option_id == menu.option_ids[-1]:
        return -1

    return menu.selected_option_id


def redirect_to_console():
    oled_print("Use console to  enter           information")


def view_password(user_id, account_id):
    data = ""
    with open("accounts.txt", "r") as file:
        data = file.read()
        # split account list by lines, and isolate user's accounts
        data = data.split("\n")[user_id][:-1]
        # split account names and passwords into seperate lists, and isolate desired password
        data = data.split(";")[account_id * 2 + 1]
    
    menu = OledMenu([data, "exit"])
    rotary_scroll(menu)
    while menu.selected_option_id != menu.option_ids[-1]:
        rotary_scroll(menu)
