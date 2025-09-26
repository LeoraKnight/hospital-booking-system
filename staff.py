#__________________________________________________________________________________________________________________
#                                               Import 
#__________________________________________________________________________________________________________________
from entities import Admin, UserManager, Staff, Account
import os
import re
import getpass

# Staff List without prompt-----------------------------------------------------------------------------------------
def display_staff_list():
    staff_list = UserManager.list_staff()

    if staff_list is not None and len(staff_list) > 0:
        print("\nStaff Members:")
        print("User ID | Username | First Name | Last Name")
        for staff in staff_list:
            print(f"{staff['User ID']} | {staff['Username']} | {staff['First Name']} | {staff['Last Name']}")
    elif staff_list == []:
        print("\nNo staff members found.")
    else:
        print("\nUnable to retrieve staff list.")
#------------------------------------------------------------------------------------------------------------------

# Staff List with prompt to return---------------------------------------------------------------------------------
def view_all_staff_accounts():
    display_staff_list()
    input("Press Enter to return")
#------------------------------------------------------------------------------------------------------------------

# Get Input--------------------------------------------------------------------------------------------------------
def get_input(prompt, validation_func=None, error_message="Invalid input"):
    while True:
        user_input = input(prompt)
        if user_input.lower() == 'cancel':
            return None
        if validation_func is None or validation_func(user_input):
            return user_input
        print(error_message)
#------------------------------------------------------------------------------------------------------------------

# Validate Generic----------------------------------------------------------------------------------------------------
def validate_generic(input_string):
    # Check the input is not empty
    return bool(input_string.strip())
#------------------------------------------------------------------------------------------------------------------

# Validate Name---------------------------------------------------------------------------------------------------
def validate_name(name):
    if not name.replace(" ", "").isalpha():
        return False
    return True
#------------------------------------------------------------------------------------------------------------------

# Validate Email---------------------------------------------------------------------------------------------------
def validate_email(email):
    return "@" in email and "." in email
#------------------------------------------------------------------------------------------------------------------

# Validate Security Question--------------------------------------------------------------------------------------
def validate_security_question(question):
    return question.endswith("?")
#------------------------------------------------------------------------------------------------------------------

# Validate Username--------------------------------------------------------------------------------------------------
def validate_username(username):
    return not UserManager.username_exists(username)
#------------------------------------------------------------------------------------------------------------------

# Validate Password-----------------------------------------------------------------------------------------------
def validate_password(password):
    if len(password) < 12 or \
       not re.search("[a-z]", password) or \
       not re.search("[A-Z]", password) or \
       not re.search("[0-9]", password) or \
       not re.search("[!@#$%^&*()_+]", password):
        return False
    return True
#------------------------------------------------------------------------------------------------------------------

# Validate Security Answer-----------------------------------------------------------------------------------------
def validate_security_answer(answer):
    if not answer.strip():
        return False  # Check the answer is not just whitespace
    if not any(char.isalnum() for char in answer):
        return False  # Check the answer contains at least one alphanumeric character
    return True
#------------------------------------------------------------------------------------------------------------------

# Create Staff------------------------------------------------------------------------------------------------------
def create_staff(admin):
    print("Create New Staff Account")

    username = get_input("Enter username or type 'cancel' to return: ", 
                         validate_username, 
                         "Invalid username. It may already exist or be empty.")
    if username is None:
        return

    while True:
        password = getpass.getpass("Enter password or type 'cancel' to return: ")
        if password.lower() == 'cancel':
            return
        if not validate_password(password):
            print("Invalid password. Must be at least 12 characters long with a mix of upper, lower, numbers, and special characters.")
            continue

        confirm_password = getpass.getpass("Confirm password: ")
        if confirm_password.lower() == 'cancel':
            return
        if password == confirm_password:
            break
        else:
            print("Passwords do not match. Please try again.")

    first_name = get_input("Enter first name or type 'cancel' to return: ", 
                           validate_name, 
                           "Invalid first name. It should only contain letters and spaces.")
    if first_name is None:
        return

    last_name = get_input("Enter last name or type 'cancel' to return: ", 
                          validate_name, 
                          "Invalid last name. It should only contain letters and spaces.")
    if last_name is None:
        return

    email = get_input("Enter email or type 'cancel' to return: ", 
                      validate_email, 
                      "Invalid email. Please enter a valid email address.")
    if email is None:
        return

    job_title = get_input("Enter job title or type 'cancel' to return: ", 
                          validate_name, 
                          "Invalid job title. It should only contain letters and spaces.")
    if job_title is None:
        return

    security_question = get_input("Enter security question (end with a ?) or type 'cancel' to return: ", 
                                  validate_security_question, 
                                  "Invalid security question. It must end with a question mark.")
    if security_question is None:
        return

    while True:
        security_answer = getpass.getpass("Enter security answer or type 'cancel' to return: ")
        if security_answer.lower() == 'cancel':
            return
        if not validate_security_answer(security_answer):
            print("Invalid security answer. It must contain at least one letter or number.")
            continue

        confirm_security_answer = getpass.getpass("Confirm security answer: ")
        if confirm_security_answer.lower() == 'cancel':
            return
        if security_answer == confirm_security_answer:
            break
        else:
            print("Security answers do not match. Please try again.")

    return admin.create_staff_account(username, password, first_name, last_name, email, job_title, security_question, security_answer)
#------------------------------------------------------------------------------------------------------------------

#Update Staff-------------------------------------------------------------------------------------------------------
def update_staff_account(admin):
    display_staff_list()
    staff_ID = input("Enter Staff ID to update or type 'cancel' to return: ")
    if staff_ID.lower() == 'cancel':
        return

    if not staff_ID.isdigit():
        print("Invalid Staff ID. Please enter a numeric ID.")
        return

    staff_ID = int(staff_ID)
    staff_members = UserManager.list_staff(staff_ID)

    if not staff_members:
        print(f"No staff member found with ID '{staff_ID}'.")
        return

    print("\nStaff Member Information:")
    for staff_member in staff_members:
        print(f"{staff_member['User ID']} | {staff_member['Username']} | {staff_member['First Name']} | {staff_member['Last Name']} | {staff_member['Email']} | {staff_member['Job Title']} | {staff_member['Security Question']}")

    input("\nPress Enter to continue")

    validation_options = {
        '1': ('username', validate_username, "Enter new username or type 'cancel' to return: ", "Invalid username. It may already exist or be empty."),
        '2': ('password', validate_password, "Invalid password."),
        '3': ('security_question', validate_security_question, "Enter new security question or type 'cancel' to return: ", "Invalid security question."),
        '4': ('security_answer', validate_security_answer, "Invalid security answer."),
        '5': ('first_name', validate_name, "Enter new first name or type 'cancel' to return: ", "Invalid first name."),
        '6': ('last_name', validate_name, "Enter new last name or type 'cancel' to return: ", "Invalid last name."),
        '7': ('job_title', validate_name, "Enter new job title or type 'cancel' to return: ", "Invalid job title."),
        '8': ('email', validate_email, "Enter new email or type 'cancel' to return: ", "Invalid email.")
    }

    while True:
        print("\nChoose field to update:")
        print("1. Username")
        print("2. Password")
        print("3. Security Question")
        print("4. Security Answer")
        print("5. First Name")
        print("6. Last Name")
        print("7. Job Title")
        print("8. Email")
        print("9. Return to previous menu")

        update_option = input("Enter option number: ")
        if update_option.lower() == '9':
            return  # Return to the previous menu

        update_field = ""
        updates = {}

        if update_option == '2':  # Password Update
            update_field = 'password'
            while True:
                new_password = getpass.getpass("Enter new password or type 'cancel' to return: ")
                if new_password.lower() == 'cancel':
                    break
                if not validate_password(new_password):
                    print("Invalid password. Must be at least 12 characters long with a mix of upper, lower, numbers, and special characters.")
                    continue

                confirm_password = getpass.getpass("Confirm new password: ")
                if confirm_password.lower() == 'cancel':
                    break
                if new_password == confirm_password:
                    updates = {'password': new_password}
                    break
                else:
                    print("Passwords do not match. Please try again.")
            if new_password.lower() == 'cancel' or confirm_password.lower() == 'cancel':
                continue  # Skip to the next iteration if user cancels

        elif update_option == '4':  # Security Answer Update
            update_field = 'security_answer'
            while True:
                new_security_answer = getpass.getpass("Enter new security answer or type 'cancel' to return: ")
                if new_security_answer.lower() == 'cancel':
                    break
                if not validate_security_answer(new_security_answer):
                    print("Invalid security answer. It must contain at least one letter or number.")
                    continue

                confirm_security_answer = getpass.getpass("Confirm new security answer: ")
                if confirm_security_answer.lower() == 'cancel':
                    break
                if new_security_answer == confirm_security_answer:
                    updates = {'security_answer': new_security_answer}
                    break
                else:
                    print("Security answers do not match. Please try again.")
            if new_security_answer.lower() == 'cancel' or confirm_security_answer.lower() == 'cancel':
                continue  # Skip to the next iteration if user cancels

        else:
            if update_option in validation_options:
                update_field, validation_func, prompt, error_message = validation_options[update_option]
                new_value = get_input(prompt, validation_func, error_message)
                if new_value is None:
                    continue  # Skip to the next iteration if user cancels
                updates = {update_field: new_value}
            else:
                print("Invalid option. Please enter a valid option number.")
                continue

        # Update logic
        success = admin.update_staff_account(staff_ID, **updates)
        if success:
            print(f"{update_field.capitalize()} updated on staff account with ID {staff_ID} successfully.")
        else:
            print(f"Failed to update {update_field} on staff account with ID {staff_ID}.")

    return staff_member  # Return staff member details after updates
#------------------------------------------------------------------------------------------------------------------

# Delete Staff Account---------------------------------------------------------------------------------------------
def delete_staff_account(admin):
    display_staff_list()
    staff_ID = input("Enter Staff ID to delete or type 'cancel' to return: ")
    if staff_ID.lower() == 'cancel':
        return

    if not staff_ID.isdigit():
        print("Invalid Staff ID. Please enter a numeric ID.")
        return

    staff_ID = int(staff_ID)
    staff_username = UserManager.get_username_by_id(staff_ID)
    if staff_username is None:
        print(f"Staff account with ID '{staff_ID}' not found.")
        return

    confirmation = input(f"Are you sure you want to delete the staff account with ID '{staff_ID}'? This action cannot be undone. Type 'yes' to confirm: ")
    if confirmation.lower() == 'yes':
        success = admin.delete_staff_account(staff_ID)
        if success:
            print(f"Staff account with ID '{staff_ID}' has been successfully deleted.")
        else:
            print(f"Failed to delete staff account with ID '{staff_ID}'.")
    else:
        print("Staff account deletion cancelled.")
#------------------------------------------------------------------------------------------------------------------

# Main Menu--------------------------------------------------------------------------------------------------------
def staff_main_menu(admin_user):
    print("\nStaff Management System")
    print("1. Create Staff Account")
    print("2. Manage Staff Accounts")
    print("3. Exit")
    choice = input("Enter your choice: ")
    return choice
#------------------------------------------------------------------------------------------------------------------

# Sub-Menu --------------------------------------------------------------------------------------------------------
def manage_staff_accounts_menu():
    print("\nManage Staff Accounts")
    print("1. View All Staff Accounts")
    print("2. Update Staff Account")
    print("3. Delete Staff Account")
    print("4. Return to Main Menu")
    choice = input("Enter your choice: ")
    return choice
#------------------------------------------------------------------------------------------------------------------

#Manage Staff Accounts---------------------------------------------------------------------------------------------
def manage_staff_accounts(admin_user):
    while True:
        choice = manage_staff_accounts_menu()
        if choice == '1':
            view_all_staff_accounts()
        elif choice == '2':
            update_staff_account(admin_user)
        elif choice == '3':
            delete_staff_account(admin_user)
        elif choice == '4':
            break  # Return to the main menu
        else:
            print("Invalid choice. Please try again.")
#------------------------------------------------------------------------------------------------------------------

#Main function-----------------------------------------------------------------------------------------------------
def main(admin_user):
    print("Welcome to the Staff Management System")

    #Verify the user is Admin
    if not isinstance(admin_user, Admin):
        print("Access denied. This system is only accessible to administrators.")
        return

    while True:
        choice = staff_main_menu(admin_user)
        if choice == '1':
            create_staff(admin_user)
        elif choice == '2':
            manage_staff_accounts(admin_user)
        elif choice == '3':
            print("Exiting Staff Management System.")
            break
        else:
            print("Invalid choice. Please try again.")
#------------------------------------------------------------------------------------------------------------------