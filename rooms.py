#__________________________________________________________________________________________________________________
#                                               Import 
#__________________________________________________________________________________________________________________
import os
from datetime import datetime, timedelta
from entities import Admin, UserManager, RoomType, Room

# Validate date-------------------------------------------------------------------------------------------------
def validate_and_parse_date(date_input, allow_today=False):
    while True:
        try:
            # Attempt to parse the date input
            date_obj = datetime.strptime(date_input, "%Y-%m-%d")
            
            # Get the current date
            current_date = datetime.now()
            
            # Check if the parsed date is before today
            if not allow_today and date_obj <= current_date:
                print("Date cannot be before today. Please enter a valid date.")
                date_input = input("Enter the date (YYYY-MM-DD): ")
                continue
            
            return date_obj
        except ValueError:
            # If parsing fails, inform the user and ask for input again
            print("Invalid date format. Please enter the date in 'YYYY-MM-DD' format.")
            date_input = input("Enter the date (YYYY-MM-DD): ")
#------------------------------------------------------------------------------------------------------------------

# Main Menu for Room Management-------------------------------------------------------------------------------------
def room_management_menu():
    print("\nRoom Management System")
    print("1. Add Room")
    print("2. Manage Rooms")
    print("3. Exit")
    choice = input("Enter your choice: ")
    return choice
#------------------------------------------------------------------------------------------------------------------

# Submenu for Managing Rooms----------------------------------------------------------------------------------------
def manage_rooms_menu():
    print("\nManage Rooms")
    print("1. View All Rooms")
    print("2. Update Room")
    print("3. Delete Room")
    print("4. Return to Main Menu")
    choice = input("Enter your choice: ")
    return choice
#------------------------------------------------------------------------------------------------------------------

# Add Room---------------------------------------------------------------------------------------------------------
def add_room(admin):
    while True:
        # Load and print the list of existing room types with numbering
        RoomType.load_room_types()
        print("Current Room Types:")
        for index, rt in enumerate(RoomType.ROOM_TYPES, start=1):
            print(f"{index}. {rt}")

        choice = input("Enter the number corresponding to the room type or type 'cancel' to return: ")
        if choice.lower() == 'cancel':
            print("Operation cancelled. Returning to the previous menu.")
            return

        try:
            choice = int(choice)
            room_type = RoomType.ROOM_TYPES[choice - 1]
            break
        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid number.")

    while True:
        current_date = datetime.now().date()

        while True:
            available_from = input("Enter available from date (YYYY-MM-DD) or type 'cancel' to return: ")
            if available_from.lower() == 'cancel':
                print("Operation cancelled. Returning to the previous menu.")
                return
            
            try:
                date_obj = datetime.strptime(available_from, '%Y-%m-%d').date()  # Convert to datetime.date
                if date_obj < current_date:
                    print("Date cannot be before today. Please enter a valid date.")
                else:
                    break
            except ValueError:
                print("Invalid date format. Please enter the date in 'YYYY-MM-DD' format.")

        while True:
            available_to = input("Enter available to date (YYYY-MM-DD) or type 'cancel' to return: ")
            if available_to.lower() == 'cancel':
                print("Operation cancelled. Returning to the previous menu.")
                return

            try:
                date_obj = datetime.strptime(available_to, '%Y-%m-%d').date()  # Convert to datetime.date
                if date_obj < current_date:
                    print("Date cannot be before today. Please enter a valid date.")
                elif date_obj < datetime.strptime(available_from, '%Y-%m-%d').date() - timedelta(days=1):
                    print("Invalid date range. 'Available to' must be the same as or after 'available from'. Please enter valid dates.")
                else:
                    break
            except ValueError:
                print("Invalid date format. Please enter the date in 'YYYY-MM-DD' format.")

        admin.add_room(room_type, available_from, available_to)
        break
#------------------------------------------------------------------------------------------------------------------

#Update Room-------------------------------------------------------------------------------------------------------
def update_room(admin):
    # Print the list of existing rooms
    admin.view_all_rooms()

    while True:
        room_id_input = input("Enter the ID of the room you want to update or type 'cancel' to return to the main menu: ")
        if room_id_input.lower() == 'cancel':
            print("Returning to main menu.")
            return

        try:
            room_id = room_id_input
            room_to_update = Room.find_room_by_id(room_id)
            if room_to_update is None:
                print(f"Room with ID '{room_id}' not found. Please enter a valid ID.")
                continue
            break
        except ValueError:
            print("Invalid room ID. Please enter a numeric ID.")

    while True:
        print("\nUpdate Options:")
        print("1. Room Type")
        print("2. Dates")
        print("3. Return to Main Menu")
        update_option = input("Enter your update choice: ")

        if update_option == '1':
            RoomType.load_room_types()
            print("Select New Room Type:")
            for index, rt in enumerate(RoomType.ROOM_TYPES, start=1):
                print(f"{index}. {rt}")

            type_choice = input("Enter the number corresponding to the new room type or type 'cancel' to cancel: ")
            if type_choice.lower() == 'cancel':
                continue

            try:
                new_room_type = RoomType.ROOM_TYPES[int(type_choice) - 1]
                admin.update_room(room_id, room_type=new_room_type)
                print("Room type updated successfully.")
            except (ValueError, IndexError):
                print("Invalid choice. Please enter a valid number.")

        elif update_option == '2':
            while True:
                new_available_from = input("Enter the new available from date (YYYY-MM-DD) or type 'cancel' to cancel: ")
                if new_available_from.lower() == 'cancel':
                    break  # Exit the loop if the user cancels
                new_available_to = input("Enter the new available to date (YYYY-MM-DD) or type 'cancel' to cancel: ")
                if new_available_to.lower() == 'cancel':
                    break  # Exit the loop if the user cancels

                try:
                    if datetime.strptime(new_available_from, '%Y-%m-%d') > datetime.strptime(new_available_to, '%Y-%m-%d'):
                        raise ValueError("Invalid dates. 'Available from' must be before or the same as 'available to'.")
                    
                    admin.update_room(room_id, available_from=new_available_from, available_to=new_available_to)
                    print("Dates updated successfully.")
                    break  # Exit the loop if the update is successful
                except ValueError as ve:
                    print(ve)
                    continue  # Prompt the user to re-enter the dates

        elif update_option == '3':
            print("Returning to previous menu.")
            return
        else:
            print("Invalid choice. Please try again.")
#------------------------------------------------------------------------------------------------------------------

# Delete Room-------------------------------------------------------------------------------------------------------
def delete_room(admin):
    admin.view_all_rooms()
    
    while True:
        room_id_input = input("Enter the ID of the room you want to delete or type 'cancel' to return to the main menu: ")
        if room_id_input.lower() == 'cancel':
            print("Returning to main menu.")
            return

        try:
            room_id = room_id_input
            room_to_delete = Room.find_room_by_id(room_id)
            if room_to_delete is None:
                print(f"Room with ID '{room_id}' not found. Please enter a valid ID.")
                continue
            break
        except ValueError:
            print("Invalid room ID. Please enter a numeric ID.")

    confirmation = input(f"Are you sure you want to delete the room with ID '{room_id}'? This action cannot be undone. Type 'yes' to confirm: ")
    if confirmation.lower() == 'yes':
        admin.delete_room(room_id)
        print(f"Room with ID '{room_id}' has been successfully deleted.")
    else:
        print("Room deletion cancelled.")
#------------------------------------------------------------------------------------------------------------------

# View All Rooms Function------------------------------------------------------------------------------------------
def view_all_rooms(admin):
    admin.view_all_rooms()
    input("Press Enter to return")
#------------------------------------------------------------------------------------------------------------------

# Manage Rooms Function-------------------------------------------------------------------------------------------
def manage_rooms(admin):
    while True:
        choice = manage_rooms_menu()
        if choice == '1':
            view_all_rooms(admin)
        elif choice == '2':
            update_room(admin)
        elif choice == '3':
            delete_room(admin)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")
#------------------------------------------------------------------------------------------------------------------

# Main Function----------------------------------------------------------------------------------------------------
def main(admin_user):
    print("Welcome to the Room Management System")

#Verify User is Admin
    if not isinstance(admin_user, Admin):
        print("Access denied. This system is only accessible to administrators.")
        return

    while True:
        choice = room_management_menu()
        if choice == '1':
            add_room(admin_user)
        elif choice == '2':
            manage_rooms(admin_user)
        elif choice == '3':
            print("Exiting Room Management System.")
            break
        else:
            print("Invalid choice. Please try again.")
#------------------------------------------------------------------------------------------------------------------