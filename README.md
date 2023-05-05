<h1>Password Manager</h1>

<h2>Part I - Final Design</h2>

<h3>Section 1 - Pseudocode</h3>

<h4>1.1</h4>

START

Print to the user the options to either sign in, create a new user, recover their passcode, or exit the application
If the option to sign in is chosen: **(1.2)**

If the option to create a new user is chosen: **(1.3)**

If the option to recover password is chosen:
	- Send email to the selected user
	- Loop back to original menu
If the option to exit the application is chosen:
	- Close the application
	
END

<h4>1.2</h4>

Bring user to `user_select()` menu
Get list of users from database
Create a new OLED menu display with this data
Use the arduino to scroll and select the option with rotary_scroll(menu) 
Bring user to enter_passcode(user_id) menu display
Display the selected values on the OLED menu
If not all four digits have been selected:
    (1.2 a)
If all four digits have been selected:
		(1.2 b)	
    
<h5>1.2 a</h5>

Get the converted dial value between 0 and 9
If the selected dial value is different from the previous values:
		- Update the displayed number on the OLED
      - If the button has been pressed:
- If the selected value is to exit:
  - Bring user back to original menu
  - If the selected value isn’t to exit:
	  - Loop back
	  - 
<h5>1.2 b</h5>

If the entered values don’t match the user passcode from the database:
		- Display an error message to the user
		- Loop back to `user_select()` menu
If the entered values match the user passcode from the database:
		- (1.2 c)
    
<h5>1.2 c</h5>

Display options on the OLED to either view accounts, add a new account, reset the numeric passcode, or sign out
Use the arduino to scroll and select the option with rotary_scroll(menu) 
If the option to view accounts is chosen:
	  (1.2 d)
If the option to create a new account is chosen:
	  (1.2 f)
If the option to reset the user passcode is chosen:
    (1.2 g)
If the option to sign out was chosen:
	  - Sign out of current user
	  - Loop back to the original menu
    
<h5>1.2 d</h5>

Bring the user to `view_accounts_option_select(user_id)` menu
Get list of accounts for user from database
Create a new menu display with this data and an option to go back
Use the arduino to scroll and select with `rotary_scroll(menu)`
If the option to go back was chosen:
		- Loop back to `signed_in_option_select()` menu
If the option to view one of the accounts was chosen:
		(1.2 e)
    
<h5>1.2 e</h5>

Bring user to `view_password(user_id, account_id)` menu
Get the password of the selected account from the database
Create a new menu display with this data and an option to go edit the password or go back
Use the arduino to scroll and select with `rotary_scroll(menu)`
If the option to go back was chosen:
			- Loop back to the `sign_in_option_select()` menu
If the option to edit the account password was chosen:
			- Bring user to `edit_account_password(user_id, account_id)` menu
			- Get account password input from the user
If the account password is not between 1 and 28 characters:
		- Display an error message to the user
		- Loop back to get a new account password input
If the account password is between 1 and 28 characters:
		- Add the account the database for the corresponding user
		- Loop back to `signed_in_option_select()` menu

<h5>1.2 f</h5>

Bring user to `add_account_to_user(user_id)` menu
Get account name input from user
If account name is not unique to the user and between 1 and 28 characters:
	- Display an error message to the user
	- Loop back to get a new account name input
If account name is unique to the user and between 1 and 28 characters:
	- Get account password input from the user
	- If the account password is not between 1 and 28 characters:
		- Display an error message to the user
		- Loop back to get a new account password input
	- If the account password is between 1 and 28 characters:
		- Add the account the database for the corresponding user
		- Loop back to `signed_in_option_select()` menu
    
<h5>1.2 g</h5>

Bring user to `edit_user_passcode(user_id)` menu
Get passcode input from user
If passcode isn’t numeric and four digits:
	- Display an error message to the user
	- Loop back to get a new passcode input
If the passcode is numeric and four digits: 
	- Add the passcode to the corresponding user in the database
	- Loop back to `signed_in_option_select()` menu
  
<h4>1.3</h4>

Bring user to `create_new_user()` menu
Get username input from the user
If username is not unique and between 4 and 28 characters:
    - Display an error message to user
    - Loop back to `create_new_user()` menu
If username is unique and between 4 and 28 characters:
	  - Get email input from user
	  - If email is not unique and resembles actual email address:
		  - Display an error message to the user
		  - Loop back to get new email input
    - If email is unique and resembles actual email address:
      - Get passcode input from user
      - If passcode isn’t numeric and four digits:
        - Display an error message to the user
        - Loop back to get new passcode input
      - If the passcode is numeric and four digits: 
        - Add the username, email, and passcode to the database
        - Loop back to the original menu
        
<h4>1.4</h4>

The `rotary_scroll(menu)` function call was referenced numerous times throughout the previous pseudocode. This is a complex part of the code that requires more explanation than other aspects. It is explained below:

<h5>1.4 a</h5>

Take a reading of the current value of the rotary potentiometer, and then a second one
If the button has been pressed:
	- Return the value that has been selected
If the button hasn’t been pressed:
		- (1.4 b)
    
<h5>1.4 b</h5>

If the difference between the first and second reading is less than -5:
		- (1.4 c)
If the difference between the first and second reading is greater than 5:
		- (1.4 d)
If the difference between the first and second reading is greater than -5 and less than 5:
		- Loop back to get a new rotary dial reading
    
<h5>1.4 c</h5>

The direction of scrolling is “down”
If the last option on the current menu is not selected:
		- Move the position of the cursor down on the OLED display
		- Update the displayed lines to match the current menu data
		- Loop back to get a new rotary dial reading
If the last option on the current menu is selected:
		- If the currently selected menu option spans one line:
			- Move the menu display down one line to the next option
- Update the displayed lines to match the current menu data
			- Loop back to get a new rotary dial reading
		- If the currently selected menu option spans two lines of test:
			- Move the menu displayed down two lines to the next option
- Update the displayed lines to match the current menu data
			- Loop back to get a new rotary dial reading

<h5>1.4 d</h5>

The direction of scrolling is “up”
If the first option on the current menu is not selected:
- If the second option is selected and the first option isn’t the second line of an option spanning two lines:
	- Move the position of the cursor up on the OLED display
	- Update the displayed lines to match the current menu data
	- Loop back to get a new rotary dial reading
- If the second option is selected and the first option is the second line of an option spanning two lines:
	- Move the menu display up one line to the next option
	- If the option above the selected option spans one line:
		- Move the menu display up one line to the next option
		- Update the displayed lines to match the current menu data
		- Loop back to get a new rotary dial reading
	- If the option above the selected option spans two lines:
		- Move the menu display up two lines to the next option
		- Update the displayed lines to match the current menu data
		- Loop back to get a new rotary dial reading
If the first option of the current menu is selected:
		-  If the option above the selected option spans one line:
	- Move the menu display up one line to the next option
	- Update the displayed lines to match the current menu data
	- Loop back to get a new rotary dial reading
- If the option above the selected option spans two lines:
	- Move the menu display up two lines to the next option
	- Update the displayed lines to match the current menu data
			- Loop back to get a new rotary dial reading 
