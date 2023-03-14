from engi1020.arduino.api import *

class OledMenu:
    def get_spanned_lines(self, option: str) -> int:
        option = len(option) / self.oled_line_max_characters
        if option <= 1:
            return 1
        elif option <= 2:
            return 2


    def update_oled(self):
        oled_clear()
        for i in self.displayed_lines:
            oled_print(i)


    def update_displayed_lines(self):
        if self.displayed_line_ids == []:
            self.displayed_lines = self.lines[0:4]
            self.displayed_lines[0] = "* " + self.displayed_lines[0][2:]

            self.displayed_line_ids = self.line_ids[0:4]
            self.displayed_options_ids = self.option_ids[0:4]
        
        else:
            for i in range(len(self.displayed_line_ids)):
                line_id = self.displayed_line_ids[i]
                self.displayed_lines[i] = self.lines[line_id]

                self.displayed_options_ids[i] = self.option_ids[line_id]

            for i in range(len(self.displayed_options_ids)):
                if self.selected_option_id == self.displayed_options_ids[i]:
                    self.displayed_lines[i] = "* " + self.displayed_lines[i][2:]
                    break

        self.update_oled()
    

    def move_menu(self, direction):
        if direction == "up":
            # if the first option is currently selected
            if self.selected_option_id == self.displayed_options_ids[0]:
                # if the second absolute option is not currently selected there are two of the same option in a row
                if self.selected_option_id != 1 and self.option_ids[self.displayed_line_ids[0] - 1] == self.option_ids[self.displayed_line_ids[0] - 2]:
                    self.displayed_line_ids = [i - 2 for i in self.displayed_line_ids]
                
                else:
                    self.displayed_line_ids = [i - 1 for i in self.displayed_line_ids]

            # else, the second line is currently selected, but the function is still being called
            # therefore, the first line is the second half of one option
            else:
                self.displayed_line_ids = [i - 1 for i in self.displayed_line_ids]
            
            self.selected_option_id = self.option_ids[self.displayed_line_ids[0]]

        elif direction == "down":
            if self.selected_option_id != self.option_ids[-2] and self.option_ids[self.displayed_line_ids[-1] + 1] == self.option_ids[self.displayed_line_ids[-1] + 2]:
                self.displayed_line_ids = [i + 2 for i in self.displayed_line_ids]

            else:
                self.displayed_line_ids = [i + 1 for i in self.displayed_line_ids]

            self.selected_option_id = self.option_ids[self.displayed_line_ids[-1]]


    def move_selected_option(self, direction):
        if direction == "up":
            # if the first option being displayed is the second part of an option
            if (self.displayed_options_ids[0] == self.option_ids[self.displayed_line_ids[0] - 1] or self.displayed_line_ids[0] == - 1) and self.selected_option_id == self.displayed_options_ids[1]:
                # move the menu
                self.move_menu(direction)
            else:
                self.selected_option_id -= 1

        elif direction == "down":
            self.selected_option_id += 1


    def scroll(self, direction):
        if direction == "up" and self.selected_option_id != self.option_ids[0]:
            if self.selected_option_id != self.displayed_options_ids[0]:
                self.move_selected_option(direction)

            else:
                self.move_menu(direction)

            self.update_displayed_lines()
            

        elif direction == "down" and self.selected_option_id != self.option_ids[-1]:
            if self.selected_option_id != self.displayed_options_ids[-1]:
                self.move_selected_option(direction)

            else:
                self.move_menu(direction)

            self.update_displayed_lines()
    

    def __init__(self, all_options: list):
        self.oled_max_characters = 64
        self.oled_line_max_characters = 14

        self.lines = []
        self.option_ids = []

        scount = 0
        for i in range(len(all_options)):
            line = all_options[i]
            if self.get_spanned_lines(line) > 1:
                self.lines.append("  " + line[:14])
                self.lines.append("  " + line[14:])
                self.option_ids += [i, i]
                scount += 1

            else:
                self.lines.append("  " + line)
                self.option_ids.append(i)

        self.line_ids = [i for i in range(len(all_options) + scount)]

        self.displayed_lines = []
        self.displayed_line_ids = []
        self.displayed_options_ids = []
        self.selected_option_id = 0

        self.update_displayed_lines()


def user_select() -> int:
    with open("userdata.txt", "r") as file:
        data = file.read()
        data = data.split("\n")[:-1]

        menu = OledMenu(data)

    print("Select your username on the Arduino using the rotary dial and hit the button to proceed.")

    rotary = analog_read(0)
    while not digital_read(6):
        d_rotary = analog_read(0)
        if d_rotary - rotary > 5:
            menu.scroll("up")
        elif d_rotary - rotary < -5:
            menu.scroll("down")
        
        rotary = analog_read(0)

    oled_clear()

    return menu.selected_option_id
