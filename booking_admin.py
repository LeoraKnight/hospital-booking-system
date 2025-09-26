#__________________________________________________________________________________________________________________
#                                               Import 
#__________________________________________________________________________________________________________________
import os
from datetime import datetime
from entities import UserManager, Booking, RoomType, Room, Patient, Staff, Admin

# View Available Room Types------------------------------------------------------------------------------------------
def view_available_room_types():
    RoomType.load_room_types()
    for i, room_type in enumerate(RoomType.ROOM_TYPES, start=1):
        print(f"{i}. {room_type}")

    choice = int(input("Select a room type by number: "))
    if choice <= len(RoomType.ROOM_TYPES):
        return RoomType.ROOM_TYPES[choice - 1]
    else:
        print("Invalid choice. Please try again.")
        return None
#----------------------------------------------------------------------------------------------------------------------

#validate dates--------------------------------------------------------------------------------------------------------
def validate_and_parse_date(date_input):
    try:
        return datetime.strptime(date_input, "%Y-%m-%d %H:%M")
    except ValueError:
        print("Invalid date format. Please enter the date in 'YYYY-MM-DD HH:MM' format.")
        return None
#----------------------------------------------------------------------------------------------------------------------

#Display rooms by type-------------------------------------------------------------------------------------------------
def display_rooms_of_selected_type(selected_type):
    available_rooms = Room.get_rooms_by_type(selected_type)
    room_ids = []

    if not available_rooms:
        return []

    print("Room ID | Room Type | Available From | Available To")
    for room in available_rooms:
        room_parts = room.split(',')
        room_id = int(room_parts[0])
        print(f"{room_id} | {room_parts[1]} | {room_parts[2]} | {room_parts[3]}")
        room_ids.append(room_id)

    return room_ids
#----------------------------------------------------------------------------------------------------------------------

# Create Booking-------------------------------------------------------------------------------------------------------
def create_booking(Admin):
    RoomType.load_room_types()

    while True:
        for i, room_type in enumerate(RoomType.ROOM_TYPES, start=1):
            print(f"{i}. {room_type}")

        choice = input("Select a room type by number or type 'cancel' to return: ")

        if choice.lower() == 'cancel':
            return

        try:
            choice = int(choice)
            if 1 <= choice <= len(RoomType.ROOM_TYPES):
                selected_type = RoomType.ROOM_TYPES[choice - 1]
            else:
                print("Invalid choice. Please select a valid room type.")
                continue  # Go back to the start of the loop if the choice is invalid
        except ValueError:
            print("Invalid choice. Please enter a number.")
            continue  # Go back to the start of the loop if the input is not a number

        print(f"Available rooms of type '{selected_type}':")
        available_room_ids = display_rooms_of_selected_type(selected_type)

        if not available_room_ids:
            print("No rooms available for this type. Please choose another type.")
            continue  # Go back to the start of the loop to reselect room type

        while True:
            room_id_input = input("Enter the ID of the room you want to book or type 'cancel' to return: ")
            if room_id_input.lower() == 'cancel':
                return
            try:
                room_id = int(room_id_input)
                if room_id in available_room_ids:
                    break
                else:
                    print("Invalid Room ID. Please enter a valid room ID from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        print("\nList of Registered Patients:")
        Patient.view_all_patients()

        while True:
            patient_id_input = input("Enter the ID of the patient (or 0 for no patient) or type 'cancel' to return: ")
            if patient_id_input.lower() == 'cancel':
                return
            try:
                patient_id = int(patient_id_input)
                if patient_id == 0 or Patient.patient_exists(patient_id):
                    break
                else:
                    print("Invalid patient ID. Patient does not exist.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        while True:
            start_date_input = input("Enter the start date and time (YYYY-MM-DD HH:MM) or type 'cancel' to return: ")
            if start_date_input.lower() == 'cancel':
                return
            start_datetime = validate_and_parse_date(start_date_input)
            if start_datetime is None:
                continue

            end_date_input = input("Enter the end date and time (YYYY-MM-DD HH:MM) or type 'cancel' to return: ")
            if end_date_input.lower() == 'cancel':
                return
            end_datetime = validate_and_parse_date(end_date_input)
            if end_datetime is None:
                continue

            current_datetime = datetime.now()
            if start_datetime < current_datetime:
                print("Start date/time cannot be in the past.")
            elif end_datetime <= start_datetime:
                print("End date/time must be after the start date/time.")
            else:
                break

        if Booking.check_room_availability(room_id, start_datetime, end_datetime):
            booking = Booking.make_booking(room_id, patient_id, start_datetime, end_datetime, Admin.user_id)
            if booking:
                print(f"Booking created successfully. Booking ID: {booking.booking_id}")
                return  # Return to the main menu
            else:
                print("Failed to create booking. The room might be unavailable for the specified time.")
        else:
            print("Room is not available for the specified time period.")
#----------------------------------------------------------------------------------------------------------------------

# View all Bookings---------------------------------------------------------------------------------------------------
def view_all_bookings(Admin):
    print("\nYour Existing Bookings:")
    Booking.view_bookings(None)
#----------------------------------------------------------------------------------------------------------------------

#View all bookings with enter prompt------------------------------------------------------------------------------------
def view_all_with_enter(Admin):
    Booking.view_bookings(None)
    input("Press Enter to return")
#----------------------------------------------------------------------------------------------------------------------

# Update Any Booking---------------------------------------------------------------------------------------------------
def update_any_booking(admin):
    view_all_bookings(admin)

    booking_id_input = input("Enter the ID of the booking you want to update or type 'cancel' to return: ").strip()
    if booking_id_input.lower() == 'cancel':
        print("Operation cancelled. Returning to previous menu.")
        return

    try:
        booking_id = int(booking_id_input)
    except ValueError:
        print("Invalid input. Please enter a valid booking ID.")
        return

    booking = Booking.find_booking_by_id(booking_id)
    if booking is None:
        print(f"No booking found with ID {booking_id}.")
        return

    while True:
        print("\nChoose an option to update:")
        print("1. Update Patient")
        print("2. Update Booking Dates/Times")
        option = input("Enter your choice (1 or 2) or type 'cancel' to return: ").strip()

        if option.lower() == 'cancel':
            print("Operation cancelled. Returning to previous menu.")
            break

        if option == '1':
            # Update Patient
            print("\nList of Registered Patients:")
            Patient.view_all_patients()
            while True:
                patient_id_input = input("Enter the ID of the patient (or type 'cancel' to return): ").strip()
                if patient_id_input.lower() == 'cancel':
                    break
                try:
                    patient_id = int(patient_id_input)
                    if patient_id == 0 or Patient.patient_exists(patient_id):
                        booking.patient_id = patient_id
                        booking.update()
                        print("Patient updated successfully")
                        break
                    else:
                        print("Invalid patient ID. Patient does not exist.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

        elif option == '2':
            #update dates
            new_start_datetime, new_end_datetime = Booking.validate_booking_dates()
            if new_start_datetime and new_end_datetime:
                # Ensure the new dates are different from the current ones before checking availability
                if new_start_datetime != booking.start_date or new_end_datetime != booking.end_date:
                    if Booking.check_room_availability(booking.room_id, new_start_datetime, new_end_datetime):
                        booking.start_date = new_start_datetime
                        booking.end_date = new_end_datetime
                        booking.update()
                        print("Date/Time updated successfully")
                    else:
                        print("The room is not available for the new specified time period.")
                else:
                    # Don't update if dates are unchanged
                    print("No changes made to booking dates/times.")

        else:
            print("Invalid option selected.")

    print("Returning to the main menu.")
#----------------------------------------------------------------------------------------------------------------------

# Cancel Any Booking------------------------------------------------------------------------------------------------------
def cancel_any_booking(Admin):
    view_all_bookings(Admin)

    booking_id_input = input("Enter the ID of the booking you want to cancel or type 'cancel' to return: ").strip()
    if booking_id_input.lower() == 'cancel':
        print("Operation cancelled. Returning to previous menu.")
        return

    try:
        booking_id = int(booking_id_input)
    except ValueError:
        print("Invalid input. Please enter a valid booking ID.")
        return

    booking = Booking.find_booking_by_id(booking_id)
    if booking is None:
        print(f"No booking found with ID {booking_id}.")
        return

    confirmation = input(f"Are you sure you want to cancel booking with ID '{booking_id}'? This action cannot be undone. Type 'yes' to confirm: ").strip().lower()
    if confirmation == "yes":
        Admin.cancel_booking(booking_id) 
    else:
        print("Booking cancellation aborted.")
#----------------------------------------------------------------------------------------------------------------------

# Manage Bookings Submenu----------------------------------------------------------------------------------------------
def manage_bookings(Admin):
    while True:
        print("\nManage Bookings")
        print("1. View Bookings")
        print("2. Update Booking")
        print("3. Cancel Booking")
        print("4. Return to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            view_all_with_enter(Admin)
        elif choice == '2':
            update_any_booking(Admin)
        elif choice == '3':
            cancel_any_booking(Admin)
        elif choice == '4':
            print("Returning to Main Menu.")
            break
        else:
            print("Invalid choice. Please try again.")
#----------------------------------------------------------------------------------------------------------------------

# Admin Booking Menu--------------------------------------------------------------------------------------------------
def main(admin_user):
    print("Welcome to the Admin Booking Menu")

    # Verify that the user is Admin
    if not isinstance(admin_user, Admin):
        print("Access denied. This system is only accessible to administrators.")
        return

    while True:
        print("\nStaff Booking Menu")
        print("1. Create Booking")
        print("2. Manage Bookings")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            create_booking(admin_user)
        elif choice == '2':
            manage_bookings(admin_user)
        elif choice == '3':
            print("Logging out.")
            break
        else:
            print("Invalid choice. Please try again.")
#----------------------------------------------------------------------------------------------------------------------
