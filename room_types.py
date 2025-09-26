#__________________________________________________________________________________________________________________
#                                               Import 
#__________________________________________________________________________________________________________________
import os
from entities import Admin, UserManager, RoomType

#Menu 1-------------------------------------------------------------------------------------------------------------
def room_types_main():
    print("\nRoom Type Management System")
    print("1. Add Room Types")
    print("2. Manage Room Types")
    print("3. Exit")
    choice = input("Enter your choice: ")
    return choice
#------------------------------------------------------------------------------------------------------------------

#Sub Menu-------------------------------------------------------------------------------------------------------------
def room_types_sub():
    print("\nManage Room Types")
    print("1. View Room Types")
    print("2. Delete Room Types")
    print("3. Update Room Types")
    print("4. Return to Main Menu")
    choice = input("Enter your choice: ")
    return choice
#------------------------------------------------------------------------------------------------------------------

#Add Room Type------------------------------------------------------------------------------------------------------
def add_room_type(admin):
    # Load and print existing room types
    RoomType.load_room_types()
    list_room_types()

    while True:
        new_room_type = input("Enter new room type or type 'cancel' to return: ")
        if new_room_type.lower() == 'cancel':
            print("Operation cancelled. Returning to the previous menu.")
            return

        if new_room_type.strip():
            if admin.add_room_type(new_room_type):
                break
            else:
                print(f"Failed to create room type '{new_room_type}'. It may already exist.")
        else:
            print("Invalid room type. Please enter a valid name (spaces are allowed).")
#------------------------------------------------------------------------------------------------------------------

# Update Room type-------------------------------------------------------------------------------------------------
def update_room_type(admin):
    # Print the list of existing room types with numbers
    RoomType.load_room_types()
    for index, room_type in enumerate(RoomType.ROOM_TYPES, start=1):
        print(f"{index}. {room_type}")

    while True:
        old_room_type_choice = input("Enter the number corresponding to the old room type to update or type 'cancel' to return: ")
        if old_room_type_choice.lower() == 'cancel':
            print("Operation cancelled. Returning to the previous menu.")
            return

        try:
            old_room_type_choice = int(old_room_type_choice)
            if 1 <= old_room_type_choice <= len(RoomType.ROOM_TYPES):
                old_room_type = RoomType.ROOM_TYPES[old_room_type_choice - 1]
                break
            else:
                print("Invalid number. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a numeric choice.")

    while True:
        new_room_type = input("Enter new room type or type 'cancel' to return: ")
        if new_room_type.lower() == 'cancel':
            print("Operation cancelled. Returning to the previous menu.")
            return

        if new_room_type.strip():
            # Check if new_room_type already exists in RoomType.ROOM_TYPES
            if new_room_type in RoomType.ROOM_TYPES:
                print(f"Room type '{new_room_type}' already exists. Please enter a different name.")
            elif admin.update_room_type(old_room_type, new_room_type):
                print(f"Room type '{old_room_type}' updated to '{new_room_type}'.")
                break
            else:
                print(f"Failed to update room type '{old_room_type}'. It may not exist.")
        else:
            print("Invalid new room type. Please enter a valid name (spaces are allowed).")
#------------------------------------------------------------------------------------------------------------------

#Delete Room Types-------------------------------------------------------------------------------------------------
def delete_room_type(admin):
    # Load and print existing room types with numbers
    RoomType.load_room_types()
    for index, room_type in enumerate(RoomType.ROOM_TYPES, start=1):
        print(f"{index}. {room_type}")

    while True:
        room_type_choice = input("Enter the number corresponding to the room type to delete or type 'cancel' to return: ")
        if room_type_choice.lower() == 'cancel':
            print("Operation cancelled. Returning to previous menu.")
            return

        try:
            room_type_choice = int(room_type_choice)
            if 1 <= room_type_choice <= len(RoomType.ROOM_TYPES):
                room_type = RoomType.ROOM_TYPES[room_type_choice - 1]
                break
            else:
                print("Invalid number. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a numeric choice.")

    confirmation = input(f"Are you sure you want to delete the room type '{room_type}'? This action cannot be undone. Type 'yes' to confirm: ")
    if confirmation.lower() == 'yes':
        if admin.delete_room_type(room_type):
            pass
        else:
            print(f"Failed to delete room type '{room_type}'.")
    else:
        print("Room type deletion cancelled.")
#------------------------------------------------------------------------------------------------------------------

#List Room Type----------------------------------------------------------------------------------------------------
def list_room_types():
    print("Current Room Types:")
    for rt in RoomType.ROOM_TYPES:
        print(rt)
#------------------------------------------------------------------------------------------------------------------

#Main function-----------------------------------------------------------------------------------------------------
def main(admin_user):
    print("Welcome to the Room Type Management System")

#Verify User is Admin
    if not isinstance(admin_user, Admin):
        print("Access denied. This system is only accessible to administrators.")
        return

    while True:
        choice = room_types_main()

        if choice == '1':
            add_room_type(admin_user)
        elif choice == '2':
            while True:
                manage_choice = room_types_sub()
                if manage_choice == '1':
                    RoomType.load_room_types()
                    list_room_types()
                    input("Press Enter to return")
                elif manage_choice == '2':
                    delete_room_type(admin_user)
                elif manage_choice == '3':
                    update_room_type(admin_user)
                elif manage_choice == '4':
                    break  # Return to main menu
                else:
                    print("Invalid choice. Please try again.")
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")
#------------------------------------------------------------------------------------------------------------------


