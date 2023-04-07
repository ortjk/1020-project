# 4.1
from engi1020.arduino.api import *

# 4.2
class OledMenu:
    # 4.3
    def get_spanned_lines(self, option: str) -> int:
        """Find whether text would span 1 or 2 lines. 1 line is considered to be 14 characters.

            Arguments:
                option (str): The string which may span 1 or 2 lines

            Returns:
                An integer corresponding to the number of lines that option spans
        """
        option = len(option) / 14
        if option <= 1:
            return 1
        elif option <= 2:
            return 2


    # 4.4
    def update_oled(self):
        """Update text that is actually displayed on the oled screen.
        """
        oled_clear()
        for i in self.displayed_lines:
            oled_print(i)


    # 4.5
    def update_displayed_lines(self):
        """Update displayed_lines to match displayed_line_ids
        """
        # 4.5 a
        for i in range(len(self.displayed_line_ids)):
            line_id = self.displayed_line_ids[i]
            self.displayed_lines[i] = self.lines[line_id]

            # change displayed_options_ids to match displayed_lines
            self.displayed_options_ids[i] = self.option_ids[line_id]

        # 4.5 b
        # put cursor on correct option
        for i in range(len(self.displayed_options_ids)):
            if self.selected_option_id == self.displayed_options_ids[i]:
                self.displayed_lines[i] = "* " + self.displayed_lines[i][2:]
                break

        # 4.5 c
        self.update_oled()
    

    # 4.6
    def move_menu(self, direction: str):
        """Change the current position in the list of menu options.

            Arguments:
                direction (str): The direction to move the position. Either 'up' or 'down'.
        """
        # 4.6 a
        if direction == "up":
            # if the first option is currently selected
            if self.selected_option_id == self.displayed_options_ids[0]:
                # if the second absolute option is not currently selected and the above option spans two lines
                if self.selected_option_id != 1 and self.option_ids[self.displayed_line_ids[0] - 1] == self.option_ids[self.displayed_line_ids[0] - 2]:
                    # so move the position up two spaces
                    self.displayed_line_ids = [i - 2 for i in self.displayed_line_ids]
                
                else:
                    # otherwise move the position up one space
                    self.displayed_line_ids = [i - 1 for i in self.displayed_line_ids]

            # else, the second line is currently selected, but the function is still being called
            # therefore, the first line is the second half of one option
            else:
                # move up the position by one space to show the full next option
                self.displayed_line_ids = [i - 1 for i in self.displayed_line_ids]
            
            # cursor now selects the first option
            self.selected_option_id = self.option_ids[self.displayed_line_ids[0]]

        # 4.6 b
        elif direction == "down":
            # if the current selected option spans two lines
            if self.selected_option_id != self.option_ids[-2] and self.option_ids[self.displayed_line_ids[-1] + 1] == self.option_ids[self.displayed_line_ids[-1] + 2]:
                # move the menu down twice
                self.displayed_line_ids = [i + 2 for i in self.displayed_line_ids]

            else:
                # otherwise move the menu down once
                self.displayed_line_ids = [i + 1 for i in self.displayed_line_ids]

            # cursor now selects the last option
            self.selected_option_id = self.option_ids[self.displayed_line_ids[-1]]


    # 4.7
    def move_selected_option(self, direction: str):
        """Change the option which is currently selected.

            Arguments:
                direction (str): The direction to move the selection. Either 'up' or 'down'.
        """
        # 4.7 a
        if direction == "up":
            # if the first option being displayed is the second part of an option
            if (self.displayed_options_ids[0] == self.option_ids[self.displayed_line_ids[0] - 1] or self.displayed_line_ids[0] == - 1) and self.selected_option_id == self.displayed_options_ids[1]:
                # move the menu
                self.move_menu(direction)
            else:
                # otherwise just move the cursor up
                self.selected_option_id -= 1

        # 4.7 b
        elif direction == "down":
            # no check is needed for 2 line spanning options
            # so just move the cursor down
            self.selected_option_id += 1


    # 4.8
    def scroll(self, direction: str):
        """Start the process to 'scroll' the menu in a specified direction.

            Arguments:
                direction (str): The direction to scroll. Can be either 'up' or 'down'.
        """
        # if you want to scroll up and the currently selected option is not at the very top of the option list
        if direction == "up" and self.selected_option_id != self.option_ids[0]:
            # if the first displayed option is not selected
            if self.selected_option_id != self.displayed_options_ids[0]:
                # simply move the selected option
                self.move_selected_option(direction)

            else:
                # otherwise, the menu position needs to be moved
                self.move_menu(direction)

            # update lines being displayed to new values
            self.update_displayed_lines()
            
        # if you want to scroll down and the currently selected option is not at the very bottom of the option list
        elif direction == "down" and self.selected_option_id != self.option_ids[-1]:
            # if the last displayed option is not selected
            if self.selected_option_id != self.displayed_options_ids[-1]:
                # simply move the selected option
                self.move_selected_option(direction)

            else:
                # otherwise, the menu position needs to be moved
                self.move_menu(direction)

            # update lines being displayed to new values
            self.update_displayed_lines() # both of these calls are inside the if statements to prevent the oled from refreshing if the first option is being selected (better for ux)
    

    # 4.9
    def __init__(self, all_options: list):
        """A class which handles the creation and state management of a menu system to be displayed onto the Arduino OLED screen.

            Arguments:
                all_options (list): List of strings which is all of the options to be displayed.
        """
        self.lines = []
        self.option_ids = []

        # break all of the options into 14-line blocks, and add 2 characters of indentation at their beginning
        scount = 0
        for i in range(len(all_options)):
            line = all_options[i]
            # if the option spans multiple lines it must be split
            if self.get_spanned_lines(line) > 1:
                self.lines.append("  " + line[:14])
                self.lines.append("  " + line[14:])
                self.option_ids += [i, i]
                scount += 1

            # otherwise just add the indentation
            else:
                self.lines.append("  " + line)
                self.option_ids.append(i)

        # the line_ids variable is simply a variable of indexes which correspond to the lines variable
        self.line_ids = [i for i in range(len(all_options) + scount)]

        self.displayed_lines = []
        self.displayed_line_ids = []
        self.displayed_options_ids = []
        self.selected_option_id = 0

        # initialize the OLED display
        self.displayed_lines = self.lines[0:4]
        self.displayed_lines[0] = "* " + self.displayed_lines[0][2:]

        self.displayed_line_ids = self.line_ids[0:4]
        self.displayed_options_ids = self.option_ids[0:4]

        self.update_oled()
