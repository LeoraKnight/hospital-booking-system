#Display Admin Menu------------------------------------------------------------------------------------------------------------
def display_admin_menu(admin_user):
    import staff
    import room_types
    import rooms
    import patients
    import booking_admin
    while True:
        print(f"Welcome {admin_user.account.username}, what would you like to do today?")
        print("1. Staff")
        print("2. Room Types")
        print("3. Rooms")
        print("4. Patients")
        print("5. Bookings")
        print("6. Logout")
        
        choice = input("Enter your choice, or '6' to logout: ")

        if choice == '1':
            staff.main(admin_user)
        elif choice == '2':
            room_types.main(admin_user)
        elif choice == '3':
            rooms.main(admin_user)
        elif choice == '4':
            patients.main(admin_user)
        elif choice == '5':
            booking_admin.main(admin_user)
        elif choice == '6':
            break 
        else:
            print("Invalid choice. Please try again.")
