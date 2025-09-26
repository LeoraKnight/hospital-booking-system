#Staff Menu-------------------------------------------------------------------------------------
def display_staff_menu(staff_user):
    import booking_staff
    import patients

    while True:
        print(f"Welcome {staff_user.account.username}, what would you like to do today?")
        print("1. Room Booking")
        print("2. Patients")
        print("3. Logout")

        choice = input("Enter your choice, or '3' to logout: ")

        if choice == '1':
            booking_staff.main(staff_user)
        elif choice == '2':
            patients.main(staff_user)
        elif choice == '3':
            print("Logging out.")
            break
        else:
            print("Invalid choice. Please try again.")
#------------------------------------------------------------------------------------------------------------------
