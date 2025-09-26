#__________________________________________________________________________________________________________________
#                                               Import 
#__________________________________________________________________________________________________________________
from entities import UserManager

#Main Menu----------------------------------------------------------------------------------------------------------
def main():
    while True:
        print("\n1. Login")
        print("2. Reset Password")
        print("3. Forgotten Password")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            UserManager.login()
        elif choice == '2':
            UserManager.reset_password()
        elif choice == '3':
            UserManager.forgotten_password()
        elif choice == '4':
            print("Exiting the system.")
            break

if __name__ == "__main__":
    main()
#----------------------------------------------------------------------------------------------------------------------------------------
