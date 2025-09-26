#__________________________________________________________________________________________________________________
#                                              Import 
#__________________________________________________________________________________________________________________
import hashlib #hash passwords
import os #dealing with files
import getpass #retrieve hashed passwords
import re #regular expressions
from datetime import datetime #get date/time 
from admin_menu import display_admin_menu
from staff_menu import display_staff_menu

#__________________________________________________________________________________________________________________
#----------------------------------------------classes-------------------------------------------------------------
#__________________________________________________________________________________________________________________

#__________________________________________________________________________________________________________________
#                                           Account Class
#__________________________________________________________________________________________________________________
class Account:
    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password)

# Hash password----------------------------------------------------------------------------------------------------
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
#------------------------------------------------------------------------------------------------------------------

# Check Username Exists-------------------------------------------------------------------------------------------
    @staticmethod
    def username_exists(username):
        return UserManager.username_exists(username)
#------------------------------------------------------------------------------------------------------------------

#__________________________________________________________________________________________________________________
#                                                 User Class
#__________________________________________________________________________________________________________________
class User:
    user_count = 0

    def __init__(self, username, password, first_name, last_name, email, job_title, security_question, security_answer, role, user_id=None):
        self.user_id = user_id if user_id is not None else self.generate_new_user_id()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.job_title = job_title
        self.security_question = security_question
        self.security_answer = Account.hash_password(security_answer)
        self.account = Account(username, password)
        self.role = role  # 'admin' or 'staff'

# create new user ID-----------------------------------------------------------------------------------------------------
    @staticmethod
    def generate_new_user_id():
        highest_id = 0
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'users.txt')

        # Check if file exists and is not empty
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            try:
                with open(file_path, 'r') as file:
                    for line in file:
                        parts = line.split(',', 1)
                        if len(parts) >= 2:
                            user_id = parts[0]
                            try:
                                highest_id = max(highest_id, int(user_id))
                            except ValueError:
                                pass
            except IOError as e:
                print(f"Error reading file: {e}")

        new_id = highest_id + 1
        return str(new_id)

    # Save user-------------------------------------------------------------------------------------------------------
    def save(self):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'users.txt')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if Account.username_exists(self.account.username):
            print(f"Username '{self.account.username}' already exists.")
            return

        user_data = f"{self.user_id},{self.account.username},{self.account.password},{self.first_name},{self.last_name},{self.email},{self.job_title},{self.security_question},{self.security_answer},{self.role}\n"

        with open(file_path, 'a') as file:
            file.write(user_data)
        print(f"User '{self.account.username}' created successfully.")
#------------------------------------------------------------------------------------------------------------------

#Update user-------------------------------------------------------------------------------------------------------
    def update(self):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'users.txt')
        try:
            with open(file_path, 'r') as file:
                users = file.readlines()

            updated = False
            for i in range(len(users)):
                parts = users[i].split(',')
                if parts[0] == str(self.user_id):
                    user_data = f"{self.user_id},{self.account.username},{self.account.password},{self.first_name},{self.last_name},{self.email},{self.job_title},{self.security_question},{self.security_answer},{self.role}\n"
                    users[i] = user_data
                    updated = True
                    break

            if updated:
                with open(file_path, 'w') as file:
                    file.writelines(users)
            else:
                print(f"No user found with ID '{self.user_id}'.")
        except FileNotFoundError:
            print("Error: User data file not found.")
#------------------------------------------------------------------------------------------------------------------

#__________________________________________________________________________________________________________________
#                              User Manager Class (for managing user)
#__________________________________________________________________________________________________________________
class UserManager:
    @staticmethod
    def username_exists(username):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'users.txt')
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    parts = line.split(',')
                    if len(parts) > 1 and parts[1] == username:
                        return True
        except FileNotFoundError:
            pass
        return False

#Reset Password------------------------------------------------------------------------------------------------------
    @staticmethod
    def reset_password():

        # Validate Password
        def validate_password(password):
            if len(password) < 12 or \
                not re.search("[a-z]", password) or \
                not re.search("[A-Z]", password) or \
                not re.search("[0-9]", password) or \
                not re.search("[!@#$%^&*()_+]", password):
                return False
            return True

        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'users.txt')

        while True:
            username = input("Enter your username or type 'cancel' to return to the previous menu: ")
            if username.lower() == 'cancel':
                print("Password reset canceled.")
                return

            if UserManager.username_exists(username):
                break
            else:
                print(f"User '{username}' not found. Please enter a valid username or type 'cancel' to cancel.")

        try:
            with open(file_path, 'r') as file:
                users = file.readlines()

            updated_users = []
            password_reset_completed = False

            for user in users:
                user_data = user.strip().split(',')
                if user_data[1] == username and not password_reset_completed:
                    while True:
                        old_password = getpass.getpass("Enter the old password or type 'cancel' to cancel: ")
                        if old_password.lower() == 'cancel':
                            print("Password reset canceled.")
                            return
                        hashed_old_password = hashlib.sha256(old_password.encode('utf-8')).hexdigest()

                        if hashed_old_password == user_data[2]:
                            while True:
                                new_password = getpass.getpass("Enter the new password or type 'cancel' to return: ")
                                if new_password.lower() == 'cancel':
                                    print("Password reset canceled.")
                                    return

                                if not validate_password(new_password):
                                    print("Invalid password. Password must be at least 12 characters long and include at least one lowercase letter, one uppercase letter, one digit, and one special character (!@#$%^&*()_+).")
                                    continue

                                confirm_new_password = getpass.getpass("Confirm the new password or type 'cancel' to return: ")
                                if confirm_new_password.lower() == 'cancel':
                                    print("Password reset canceled.")
                                    return

                                if confirm_new_password == new_password:
                                    hashed_new_password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
                                    user_data[2] = hashed_new_password  # Update the password field
                                    print(f"Password reset for user '{username}' is successful.")
                                    updated_users.append(','.join(user_data) + '\n')
                                    password_reset_completed = True
                                    break  # Exit the inner loop
                        else:
                            print("Incorrect old password. Please try again or type 'cancel' to cancel.")
                        if password_reset_completed:
                            break  # Exit the outer loop
                else:
                    updated_users.append(user)

            if password_reset_completed:
                with open(file_path, 'w') as file:
                    file.writelines(updated_users)

        except IOError as e:
            print(f"An error occurred: {e}")

#------------------------------------------------------------------------------------------------------------------------------

#Forgotton Password------------------------------------------------------------------------------------------------------------
    @staticmethod
    def forgotten_password(username=None):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'users.txt')

        # Validate Password
        def validate_password(password):
            if len(password) < 12 or \
                not re.search("[a-z]", password) or \
                not re.search("[A-Z]", password) or \
                not re.search("[0-9]", password) or \
                not re.search("[!@#$%^&*()_+]", password):
                return False
            return True

        try:
            if username is None:
                while True:
                    username = input("Enter your username or type 'cancel' to return to the previous menu: ")
                    if username.lower() == 'cancel':
                        print("Password reset canceled.")
                        return

                    if UserManager.username_exists(username):
                        break
                    else:
                        print(f"User '{username}' not found. Please enter a valid username or type 'cancel' to cancel.")

            with open(file_path, 'r') as file:
                users = file.readlines()

            updated_users = []
            password_changed = False

            for user_data in users:
                user_data = user_data.strip().split(',')
                if user_data[1] == username and not password_changed:
                    while True:
                        security_question = user_data[7]
                        answer = getpass.getpass(f"{security_question} or type 'cancel' to return: ")
                        if answer.lower() == 'cancel':
                            print("Password reset canceled.")
                            return

                        hashed_answer = hashlib.sha256(answer.encode('utf-8')).hexdigest()

                        if hashed_answer == user_data[8]:
                            while True:
                                new_password = getpass.getpass("Enter the new password or type 'cancel' to return: ")
                                if new_password.lower() == 'cancel':
                                    print("Password reset canceled.")
                                    return

                                if not validate_password(new_password):
                                    print("Invalid password. Password must be at least 12 characters long and include at least one lowercase letter, one uppercase letter, one digit, and one special character (!@#$%^&*()_+).")
                                    continue

                                confirm_password = getpass.getpass("Confirm the new password or type 'cancel' to return: ")
                                if confirm_password.lower() == 'cancel':
                                    print("Password reset canceled.")
                                    return

                                if new_password == confirm_password:
                                    hashed_new_password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
                                    user_data[2] = hashed_new_password  # Update the password field
                                    password_changed = True
                                    print("Password has been successfully reset.")
                                    break
                                else:
                                    print("Passwords do not match. Try again.")
                            break
                        else:
                            print("Incorrect answer. Try again or type 'cancel' to return.")
                
                updated_users.append(','.join(user_data) + '\n')

            if password_changed:
                with open(file_path, 'w') as file:
                    file.writelines(updated_users)

        except IOError as e:
            print(f"An error occurred: {e}")

#------------------------------------------------------------------------------------------------------------------------------   

#List staff--------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def list_staff(staff_ID=None):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'users.txt')
        staff_members = []

        try:
            with open(file_path, 'r') as file:
                users = file.readlines()

            for user in users:
                user_data = user.strip().split(',')
                if user_data[-1] == 'staff':
                    user_info = {
                        'User ID': user_data[0],
                        'Username': user_data[1],
                        'First Name': user_data[3],
                        'Last Name': user_data[4],
                        'Email': user_data[5],
                        'Job Title': user_data[6],
                        'Security Question': user_data[7]
                    }
                    staff_members.append(user_info)

            if staff_ID is not None:
                staff_members = [staff for staff in staff_members if staff['User ID'] == str(staff_ID)]

        except IOError:
            print("Error reading the users file.")

        return staff_members
#------------------------------------------------------------------------------------------------------------------------------

#Get username by ID------------------------------------------------------------------------------------------------------------
    @classmethod
    def get_username_by_id(cls, user_id):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'users.txt')
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    user_data = line.strip().split(',')
                    if len(user_data) >= 1 and user_data[0] == str(user_id):
                        return user_data[1]
        except FileNotFoundError:
            print("Error: User data file not found.")
            return None

        print("User ID not found.")
        return None
#------------------------------------------------------------------------------------------------------------------------------
  
#get staff by ID---------------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_staff_by_id(staff_id):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'users.txt')
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    user_data = line.strip().split(',')
                    if len(user_data) >= 10 and user_data[0] == str(staff_id) and user_data[9] == 'staff':
                        username = user_data[1]
                        password = user_data[2]
                        first_name = user_data[3]
                        last_name = user_data[4]
                        email = user_data[5]
                        job_title = user_data[6]
                        security_question = user_data[7]
                        security_answer = user_data[8]
                        return Staff(username, password, first_name, last_name, email, job_title, security_question, security_answer, staff_id)
        except FileNotFoundError:
            print("Error: User data file not found.")
        return None
#------------------------------------------------------------------------------------------------------------------------------
   
#Get user by username----------------------------------------------------------------------------------------------------------
    @classmethod
    def get_user_by_username(cls, username):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'users.txt')

        try:
            with open(file_path, 'r') as file:
                for line in file:
                    user_data = line.strip().split(',')
                    if len(user_data) >= 2 and user_data[1] == username:
                        # Found a user with the matching username
                        return User(
                            user_data[1],  # username
                            user_data[2],  # password
                            user_data[3],  # first_name
                            user_data[4],  # last_name
                            user_data[5],  # email
                            user_data[6],  # job_title
                            user_data[7],  # security_question
                            user_data[8],  # security_answer
                            user_data[9]   # role
                        )
        except FileNotFoundError:
            pass
        # User with the specified username not found
        return None
#------------------------------------------------------------------------------------------------------------------------------

#Verify Login-----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def verify_login(username, password):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'users.txt')
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    user_data = line.strip().split(',')
                    if user_data[1] == username and user_data[2] == hashlib.sha256(password.encode('utf-8')).hexdigest():
                        return user_data
        except FileNotFoundError:
            print("Error: User data file not found.")
            return None
#-----------------------------------------------------------------------------------------------------------------------------

#Login------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def login():
        print("Login to your Account")
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'users.txt')

        while True:
            username = input("Enter your username or type 'cancel' to return: ")
            if username.lower() == 'cancel':
                print("Login cancelled. Returning to previous menu.")
                return None

            user_found = False
            user_data = None

            try:
                with open(file_path, 'r') as file:
                    for line in file:
                        current_user_data = line.strip().split(',')
                        if current_user_data[1] == username:
                            user_found = True
                            user_data = current_user_data
                            break

            except FileNotFoundError:
                print("Error: User data file not found.")
                return None

            if not user_found:
                print("Username not found. Please try again.")
                continue

            # Inner loop for password verification
            while True:
                password = getpass.getpass("Enter your password or type 'cancel' to return: ")
                if password.lower() == 'cancel':
                    print("Login cancelled. Returning to previous menu.")
                    return None

                if hashlib.sha256(password.encode('utf-8')).hexdigest() == user_data[2]:
                    break  # Correct password
                else:
                    print("Incorrect password. Please try again.")

            # Unpack the login and direct to respective menus
            user_id, _, _, first_name, last_name, email, job_title, security_question, security_answer, role = user_data
            if role == 'staff':
                user = Staff(username, password, first_name, last_name, email, job_title, security_question, security_answer, user_id)
                display_staff_menu(user)
                return user
            elif role == 'admin':
                user = Admin(username, password, first_name, last_name, email, job_title, security_question, security_answer, user_id)
                display_admin_menu(user)
                return user
            else:
                print("Access denied. This system is only accessible to staff and admin members.")
                return None

#------------------------------------------------------------------------------------------------------------------------------

#__________________________________________________________________________________________________________________
#                                                    Admin Class
#__________________________________________________________________________________________________________________
class Admin(User):  
    def __init__(self, username, password, first_name, last_name, email, job_title, security_question, security_answer, user_id=None):
        super().__init__(username=username, password=password, first_name=first_name, last_name=last_name, email=email, job_title=job_title, security_question=security_question, security_answer=security_answer, role='admin', user_id=user_id)
        self.is_superuser = True
        
#---------------------------------------------------------------------------------------------------------------------
#                                                  Staff Management
#---------------------------------------------------------------------------------------------------------------------

#create staff---------------------------------------------------------------------------------------------------------------
    def create_staff_account(self, username, password, first_name, last_name, email, job_title, security_question, security_answer):
        if self.role != 'admin':
            raise PermissionError("Only admins can create staff accounts.")
        staff = User(username, password, first_name, last_name, email, job_title, security_question, security_answer, role='staff')
        staff.save()
        return staff
#---------------------------------------------------------------------------------------------------------------------
   
#update staff account-------------------------------------------------------------------------------------------------
    def update_staff_account(self, staff_id, **kwargs):
        staff = UserManager.get_staff_by_id(staff_id)
        if staff and staff.role == 'staff':
            for field, value in kwargs.items():
                if field == 'username':
                    if UserManager.username_exists(value) and value != staff.account.username:
                        raise ValueError(f"Username '{value}' already exists.")
                    staff.account.username = value
                elif field == 'password':
                    staff.account.password = Account.hash_password(value)
                elif field == 'security_answer':
                    staff.security_answer = Account.hash_password(value)
                elif hasattr(staff, field):
                    setattr(staff, field, value)
                else:
                    raise ValueError(f"Invalid field '{field}' for staff account update.")
            staff.update()
            return True
        else:
            print(f"Staff account with ID '{staff_id}' not found.")
            return False
#---------------------------------------------------------------------------------------------------------------------

# Delete Staff--------------------------------------------------------------------------------------------------------
    def delete_staff_account(self, staff_id):
        file_path_users = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'users.txt')
        file_path_bookings = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'bookings.txt')

        try:
            # Deleting staff from users.txt
            with open(file_path_users, 'r') as file:
                users = file.readlines()

            updated_users = []
            found = False

            for user in users:
                user_data = user.strip().split(',')
                if user_data[0] == str(staff_id) and user_data[-1] == 'staff':
                    found = True
                    continue 
                updated_users.append(user)

            if found:
                with open(file_path_users, 'w') as file:
                    file.writelines(updated_users)
                print(f"Staff account with ID '{staff_id}' deleted successfully.")
            else:
                print(f"No staff account found with ID '{staff_id}'.")
                return  # Exit if no staff found

            # Updating bookings in bookings.txt
            updated_bookings = []
            with open(file_path_bookings, 'r') as file:
                bookings = file.readlines()

            for booking in bookings:
                booking_data = booking.strip().split(',')
                if booking_data[5] == str(staff_id):  # Check if the booking is by the deleted staff
                    booking_data[5] = '0'  # Set user_id to 0
                    booking_data[6] = 'Cancelled'  # Set status to Cancelled
                updated_booking = ','.join(booking_data)
                updated_bookings.append(updated_booking + '\n')

            with open(file_path_bookings, 'w') as file:
                file.writelines(updated_bookings)

        except FileNotFoundError as e:
            print(f"Error: {e}")
#---------------------------------------------------------------------------------------------------------------------

#View Staff-----------------------------------------------------------------------------------------------------------
    def view_staff_accounts(self):
        if self.role != 'admin':
            raise PermissionError("Only admins can view staff accounts.")

        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'users.txt')

        try:
            with open(file_path, 'r') as file:
                users = file.readlines()

            staff_accounts = []
            for user in users:
                user_data = user.strip().split(',')
                if user_data[-1] == 'staff':
                    staff_info = {
                        'Username': user_data[1],
                        'First Name': user_data[3],
                        'Last Name': user_data[4],
                        'Email': user_data[5],
                        'Job Title': user_data[6],
                    }
                    staff_accounts.append(staff_info)

            return staff_accounts

        except IOError as e:
            print(f"An error occurred while viewing staff accounts: {e}")
#---------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------
#                                           Room Type Management
# ---------------------------------------------------------------------------------------------------------------------   
            
#Add Room Type -------------------------------------------------------------------------------------------------------            
    def add_room_type(self, new_room_type):
        if self.role != 'admin':
            raise PermissionError("Only admins can add new room types.")

        # Load current room types check if the new type already exists
        RoomType.load_room_types()

        if new_room_type in RoomType.ROOM_TYPES:
            return False
        else:
            RoomType.ROOM_TYPES.append(new_room_type)
            RoomType.save_room_types()
            print(f"Room type '{new_room_type}' added successfully.")
            return True
# ---------------------------------------------------------------------------------------------------------------------  

#update room type------------------------------------------------------------------------------------------------------
    def update_room_type(self, old_room_type, new_room_type):
        if self.role != 'admin':
            raise PermissionError("Only admins can update room types.")

        if old_room_type not in RoomType.ROOM_TYPES:
            print(f"Room type '{old_room_type}' does not exist.")
            return False

        # Replace old room type with new room type
        index = RoomType.ROOM_TYPES.index(old_room_type)
        RoomType.ROOM_TYPES[index] = new_room_type

        # Save the updated list to file
        RoomType.save_room_types()
        print(f"Room type '{old_room_type}' updated to '{new_room_type}'.")

        # Update room types in rooms.txt
        file_path_rooms = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'rooms.txt')
        updated_rooms = False
        new_lines_rooms = []

        try:
            with open(file_path_rooms, 'r') as file:
                for line in file:
                    room_id, room_type, available_from, available_to = line.strip().split(',')
                    if room_type == old_room_type:
                        room_type = new_room_type
                        updated_rooms = True
                    new_line = f"{room_id},{room_type},{available_from},{available_to}\n"
                    new_lines_rooms.append(new_line)

            if updated_rooms:
                with open(file_path_rooms, 'w') as file:
                    file.writelines(new_lines_rooms)
                print(f"All rooms with old room type '{old_room_type}' updated to '{new_room_type}'.")

        except FileNotFoundError:
            print("Room data file not found.")
        
        return True
# ---------------------------------------------------------------------------------------------------------------------  
 
#Delete room types-----------------------------------------------------------------------------------------------------
    def delete_room_type(self, room_type):
        if self.role != 'admin':
            raise PermissionError("Only admins can delete room types.")

        # Load current room types
        RoomType.load_room_types()

        # Check if the room type exists
        if room_type not in RoomType.ROOM_TYPES:
            print(f"Room type '{room_type}' not found.")
            return False

        # Load rooms data
        file_path_rooms = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'rooms.txt')
        try:
            with open(file_path_rooms, 'r') as file:
                rooms = file.readlines()
        except FileNotFoundError:
            print("Room data file not found.")
            return False

        # Update rooms with deleted room type to NULL
        updated_rooms = False
        new_lines_rooms = []
        for line in rooms:
            r_id, r_type, available_from, available_to = line.strip().split(',')
            if r_type == room_type:
                r_type = 'NULL'  # Set room type to NULL
                updated_rooms = True
            new_line = f"{r_id},{r_type},{available_from},{available_to}\n"
            new_lines_rooms.append(new_line)

        # Save updated room data
        if updated_rooms:
            try:
                with open(file_path_rooms, 'w') as file:
                    file.writelines(new_lines_rooms)
            except IOError as e:
                print(f"An error occurred while updating rooms: {e}")
                return False

        # Remove the room type from ROOM_TYPES and save
        RoomType.ROOM_TYPES.remove(room_type)
        RoomType.save_room_types()  # save updated list to file
        print(f"Room type '{room_type}' has been deleted and all associated rooms have been updated.")
        return True
# ---------------------------------------------------------------------------------------------------------------------  

# ---------------------------------------------------------------------------------------------------------------------  
#                                        Room Management
# ---------------------------------------------------------------------------------------------------------------------  

#add room-------------------------------------------------------------------------------------------------------------
    def add_room(self, room_type, available_from, available_to):
        RoomType.load_room_types()
        if self.role != 'admin':
            raise PermissionError("Only admins can add new rooms.")

        # Check if the room type is valid
        if room_type not in RoomType.ROOM_TYPES:
            raise ValueError(f"Invalid room type: {room_type}. Must be one of {RoomType.ROOM_TYPES}.")

        # Check if the dates are valid (available_from is before available_to)
        if datetime.strptime(available_from, '%Y-%m-%d') > datetime.strptime(available_to, '%Y-%m-%d'):
            raise ValueError("Invalid dates: 'available_from' must be before or the same as 'available_to'.")

        # Create a new Room instance
        new_room = Room(room_type, available_from, available_to)
        new_room.save()  # Save room details to the file
        return new_room

# ---------------------------------------------------------------------------------------------------------------------     
  
#view rooms------------------------------------------------------------------------------------------------------------
    def view_all_rooms(self):
        RoomType.load_room_types()
        if self.role != 'admin':
            raise PermissionError("Only admins can view all rooms.")

        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'rooms.txt')
        try:
            with open(file_path, 'r') as file:
                rooms = file.readlines()
                
            if not rooms:
                print("No rooms are currently registered in the system.")
                return []

            print("Room ID | Room Type | Available From | Available To")
            for room in rooms:
                room_id, room_type, available_from, available_to = room.strip().split(',')
                print(f"{room_id} | {room_type} | {available_from} | {available_to}")
                
            return rooms 

        except FileNotFoundError:
            print("Room data file not found.")
            return []
# ---------------------------------------------------------------------------------------------------------------------  
       
#update room-----------------------------------------------------------------------------------------------------------
    def update_room(self, room_id, **kwargs):
        # Find the room by ID
        room = Room.find_room_by_id(room_id)

        if room:
            room.room_id = room_id
            updated_room_type = False
            updated_availability = False

            for field, value in kwargs.items():
                if field == 'room_type':
                    old_room_type = room.room_type
                    room.room_type = value
                    updated_room_type = True
                elif field == 'available_from':
                    room.available_from = value
                    updated_availability = True
                elif field == 'available_to':
                    room.available_to = value
                    updated_availability = True

            room.update()

            if updated_room_type or updated_availability:
                # Update room in rooms.txt
                file_path_rooms = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'rooms.txt')
                new_lines_rooms = []

                try:
                    with open(file_path_rooms, 'r') as file:
                        for line in file:
                            r_id, r_type, available_from, available_to = line.strip().split(',')
                            if r_id == room_id:
                                r_type = room.room_type if updated_room_type else r_type
                                available_from = room.available_from if updated_availability else available_from
                                available_to = room.available_to if updated_availability else available_to
                            new_line = f"{r_id},{r_type},{available_from},{available_to}\n"
                            new_lines_rooms.append(new_line)

                    with open(file_path_rooms, 'w') as file:
                        file.writelines(new_lines_rooms)

                except FileNotFoundError:
                    print("Room data file not found.")

        else:
            print(f"No room found with ID {room_id}.")

# ---------------------------------------------------------------------------------------------------------------------  

#Delete Room-----------------------------------------------------------------------------------------------------------
    def delete_room(self, room_id):
        if self.role != 'admin':
            raise PermissionError("Only admins can delete rooms.")

        # Delete the room
        file_path_rooms = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'rooms.txt')
        updated_rooms = False
        new_lines_rooms = []

        try:
            with open(file_path_rooms, 'r') as file:
                for line in file:
                    current_id, _, _, _ = line.strip().split(',')
                    if current_id != room_id:
                        new_lines_rooms.append(line)
                    else:
                        updated_rooms = True

            if updated_rooms:
                with open(file_path_rooms, 'w') as file:
                    file.writelines(new_lines_rooms)
            else:
                print(f"No room found with ID {room_id}.")

        except FileNotFoundError:
            print("Room data file not found.")

        # Process to cancel bookings associated with the deleted room
        file_path_bookings = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'bookings.txt')
        try:
            with open(file_path_bookings, 'r') as file:
                bookings = file.readlines()

            updated_bookings = False
            for i in range(len(bookings)):
                booking_data = bookings[i].strip().split(',')
                if len(booking_data) >= 7 and booking_data[1] == room_id:  # Removed integer conversion
                    # Update the status to 'Cancelled'
                    booking_data[6] = "Cancelled"
                    bookings[i] = ','.join(booking_data) + '\n'
                    updated_bookings = True

            if updated_bookings:
                with open(file_path_bookings, 'w') as file:
                    file.writelines(bookings)
                print(f"All bookings for room ID {room_id} have been marked as cancelled.")
        except FileNotFoundError:
            print("Booking data file not found.")

# ---------------------------------------------------------------------------------------------------------------------  

# ---------------------------------------------------------------------------------------------------------------------  
#                                                 Booking Management
# ---------------------------------------------------------------------------------------------------------------------  

# Cancel any Booking----------------------------------------------------------------------------------------------------
    def cancel_booking(self, booking_id):
        booking = Booking.find_booking_by_id(booking_id)
        if booking is None:
            print(f"No booking found with ID {booking_id}.")
            return
        booking.change_status(Cancelled())
        booking.update()
        print(f"Booking with ID {booking_id} has been cancelled.")

# --------------------------------------------------------------------------------------------------------------------- 

# Update any booking---------------------------------------------------------------------------------------------------
    @classmethod
    def update_booking(cls, booking_id, patient_id=None, new_start_datetime=None, new_end_datetime=None, room_id=None):
        booking = Booking.find_booking_by_id(booking_id)
        if booking is None:
            print(f"No booking found with ID {booking_id}.")
            return

        # Update patient ID
        if patient_id is not None:
            booking.patient_id = patient_id

        # Check if dates are changed
        dates_or_room_changed = (new_start_datetime != booking.start_date) or (new_end_datetime != booking.end_date) or (room_id is not None and room_id != booking.room_id)

        if dates_or_room_changed:
            # Check room availability for the new times
            if Booking.check_room_availability(room_id or booking.room_id, new_start_datetime or booking.start_date, new_end_datetime or booking.end_date):
                if new_start_datetime:
                    booking.start_date = new_start_datetime
                if new_end_datetime:
                    booking.end_date = new_end_datetime
                if room_id:
                    booking.room_id = room_id
            else:
                print("The room is not available for the new specified time period.")
                return

        booking.update()
# --------------------------------------------------------------------------------------------------------------------- 

#__________________________________________________________________________________________________________________
#                                               Staff Class
#__________________________________________________________________________________________________________________

class Staff(User):
    def __init__(self, username, password, first_name, last_name, email, job_title, security_question, security_answer, user_id=None):
        super().__init__(username=username, password=password, first_name=first_name, last_name=last_name, email=email, job_title=job_title, security_question=security_question, security_answer=security_answer, role='staff', user_id=user_id)
        self.is_superuser = False

# --------------------------------------------------------------------------------------------------------------------- 
#                                           Booking Management
# ---------------------------------------------------------------------------------------------------------------------   
    
# Update own booking---------------------------------------------------------------------------------------------------
    def update_own_booking(self, booking_id, patient_id=None, new_start_datetime=None, new_end_datetime=None):
        booking = Booking.find_booking_by_id(booking_id)
        if booking is None:
            return

        # Check if the current user is allowed to update this booking
        if int(booking.user_id) != int(self.user_id):
            print("You can only update your own bookings.")
            return

        # Update patient ID if provided
        if patient_id is not None:
            booking.patient_id = patient_id

        # Check if dates are changed
        dates_changed = (new_start_datetime != booking.start_date) or (new_end_datetime != booking.end_date)

        if dates_changed:
            # Check room availability for the new times
            if Booking.check_room_availability(booking.room_id, new_start_datetime, new_end_datetime):
                booking.start_date = new_start_datetime
                booking.end_date = new_end_datetime
                print(f"Booking start date updated to {new_start_datetime}, end date updated to {new_end_datetime}.")
            else:
                print("The room is not available for the new specified time period.")
                return

        booking.update()
# ---------------------------------------------------------------------------------------------------------------------     

# Cancel own booking--------------------------------------------------------------------------------------------------
    def cancel_own_booking(self, booking_id):
        # Find the booking with the provided ID
        booking = Booking.find_booking_by_id(booking_id)
        if booking is None:
            return

        # Check if the current user is allowed to cancel this booking
        if int(booking.user_id) != int(self.user_id):
            print("You can only cancel your own bookings.")
            return

        # Confirm the cancellation
        confirmation = input("Are you sure you want to cancel this booking? (yes/no): ").strip().lower()
        if confirmation == "yes":
            # Update the booking status to "Cancelled"
            booking.status = "Cancelled"
            booking.update()
            print(f"Booking with ID {booking_id} has been cancelled.")
        else:
            print("Booking cancellation aborted.")
# --------------------------------------------------------------------------------------------------------------------- 

#__________________________________________________________________________________________________________________
#                                              Room Type Class
#__________________________________________________________________________________________________________________
class RoomType:
    _instance = None
    ROOM_TYPES = [] # singleton design pattern

    FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'roomTypes.txt')
# --------------------------------------------------------------------------------------------------------------------- 

#Singleton room type manager--------------------------------------------------------------------------------------------
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RoomType, cls).__new__(cls)
            # load room types
            cls._initialize()
        return cls._instance
# --------------------------------------------------------------------------------------------------------------------- 

#Initilize Room Types----------------------------------------------------------------------------------------------------
    @classmethod
    def _initialize(cls):
        # Load room types from file or use defaults in load_room_types if file not found
        cls.load_room_types()
# --------------------------------------------------------------------------------------------------------------------- 

#load room types----------------------------------------------------------------------------------------------------------
    @classmethod
    def load_room_types(cls):
        try:
            with open(cls.FILE_PATH, 'r') as file:
                cls.ROOM_TYPES = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            cls.ROOM_TYPES = [
                "Ward", "ICU", "NICU", "Isolation Room", 
                "Labor & Delivery Room", "Operating Room", 
                "Recovery Room", "Emergency Room", "Pediatric Room"
            ]
            cls.save_room_types()
            print("Default room types initialized and saved to roomTypes.txt.")
# --------------------------------------------------------------------------------------------------------------------- 

#save room types-------------------------------------------------------------------------------------------------------
    @classmethod
    def save_room_types(cls):
        with open(cls.FILE_PATH, 'w') as file:
            for room_type in cls.ROOM_TYPES:
                file.write(room_type + '\n')
# --------------------------------------------------------------------------------------------------------------------- 
            
#__________________________________________________________________________________________________________________
#                                                 Room Class
#__________________________________________________________________________________________________________________
class Room:
    def __init__(self, room_type, available_from, available_to):
        self.room_id = self.generate_new_room_id()
        self.room_type = room_type
        self.available_from = available_from
        self.available_to = available_to

#Generate ID---------------------------------------------------------------------------------------------------------------
    @staticmethod
    def generate_new_room_id():
        highest_id = 0
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'rooms.txt')

        # Check if file exists and is not empty
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            try:
                with open(file_path, 'r') as file:
                    for line in file:
                        parts = line.strip().split(',', 1)
                        if len(parts) >= 2:
                            room_id = parts[0]
                            try:
                                highest_id = max(highest_id, int(room_id))
                            except ValueError:
                                pass
            except IOError as e:
                print(f"Error reading file: {e}")

        new_id = highest_id + 1
        return str(new_id)
# --------------------------------------------------------------------------------------------------------------------- 
 
#Save-------------------------------------------------------------------------------------------------------------------
    def save(self):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'rooms.txt')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        room_data = f"{self.room_id},{self.room_type},{self.available_from},{self.available_to}\n"

        with open(file_path, 'a') as file:
            file.write(room_data)

# --------------------------------------------------------------------------------------------------------------------- 

#Update----------------------------------------------------------------------------------------------------------------
    def update(self):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'rooms.txt')

        try:
            with open(file_path, 'r') as file:
                rooms = file.readlines()

            updated = False
            for i in range(len(rooms)):
                room_id, _, _, _ = rooms[i].strip().split(',')
                if room_id == self.room_id:
                    room_data = f"{self.room_id},{self.room_type},{self.available_from},{self.available_to}\n"
                    rooms[i] = room_data
                    updated = True
                    break

            if updated:
                with open(file_path, 'w') as file:
                    file.writelines(rooms)
            else:
                print(f"No room found with ID {self.room_id}.")

        except IOError as e:
            print(f"An error occurred while updating the room: {e}")
# --------------------------------------------------------------------------------------------------------------------- 

#find room by ID-------------------------------------------------------------------------------------------------------
    @classmethod
    def find_room_by_id(cls, room_id):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'rooms.txt')
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    room_data = line.strip().split(',')
                    if len(room_data) >= 1 and room_data[0] == str(room_id):
                        room_type = room_data[1]
                        available_from = room_data[2]
                        available_to = room_data[3]
                        return cls(room_type, available_from, available_to)
        except FileNotFoundError:
            pass
        return None
# --------------------------------------------------------------------------------------------------------------------- 

#check room with ID exists---------------------------------------------------------------------------------------------
    @classmethod
    def room_exists(cls, rooms, room_id):
        # Check if a room with the given ID exists in the list of rooms
        for room in rooms:
            if room.room_id == str(room_id):
                return True
        return False
# --------------------------------------------------------------------------------------------------------------------- 
   
#get rooms by room type-----------------------------------------------------------------------------------------------
    @classmethod
    def get_rooms_by_type(cls, room_type):
        available_rooms = []
        # file path
        file_path_rooms = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'rooms.txt')
        # Load room data
        try:
            with open(file_path_rooms, 'r') as file:
                rooms = file.readlines()
        except FileNotFoundError:
            print("Room data file not found.")
            return []
        # Filter rooms by type
        for room in rooms:
            room_parts = room.strip().split(',')
            if len(room_parts) >= 4:
                room_id, r_type, _, _ = room_parts
                if r_type == room_type:
                    available_rooms.append(room.strip())
        if not available_rooms:
            print(f"No available rooms found for room type '{room_type}'")
        return available_rooms
# --------------------------------------------------------------------------------------------------------------------- 

#__________________________________________________________________________________________________________________
#                                               Patient Class
#__________________________________________________________________________________________________________________

class Patient:
    def __init__(self, first_name, last_name, age, gender, contact_number, patient_id=None):
        if patient_id is None:
            self.patient_id = self.generate_new_patient_id()
        else:
            self.patient_id = patient_id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.contact_number = contact_number

#generare ID-----------------------------------------------------------------------------------------------------------
    @staticmethod
    def generate_new_patient_id():
        highest_id = 0
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'patients.txt')

        # Check if file exists and is not empty
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            try:
                with open(file_path, 'r') as file:
                    for line in file:
                        parts = line.strip().split(',', 1)
                        if len(parts) >= 2:
                            patient_id = int(parts[0])
                            highest_id = max(highest_id, patient_id)
            except IOError as e:
                print(f"Error reading file: {e}")

        return highest_id + 1
# --------------------------------------------------------------------------------------------------------------------- 
    
# Save-----------------------------------------------------------------------------------------------------------------
    def save(self):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'patients.txt')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        patient_data = f"{self.patient_id},{self.first_name},{self.last_name},{self.age},{self.gender},{self.contact_number}\n"
        
        with open(file_path, 'a') as file:
            file.write(patient_data)
        print(f"Patient '{self.first_name} {self.last_name}' with ID {self.patient_id} added successfully.")
# --------------------------------------------------------------------------------------------------------------------- 

#update---------------------------------------------------------------------------------------------------------------
    def update(self):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'patients.txt')

        try:
            with open(file_path, 'r') as file:
                patients = file.readlines()

            updated = False
            for i, patient in enumerate(patients):
                patient_id, _, _, _, _, _ = patient.strip().split(',')
                if int(patient_id) == self.patient_id:
                    # Replace the existing record with the updated data
                    updated_patient_data = f"{self.patient_id},{self.first_name},{self.last_name},{self.age},{self.gender},{self.contact_number}\n"
                    patients[i] = updated_patient_data
                    updated = True
                    break

            if updated:
                with open(file_path, 'w') as file:
                    file.writelines(patients)
            else:
                print(f"No patient found with ID {self.patient_id}.")

        except IOError as e:
            print(f"An error occurred while updating the patient: {e}")
# --------------------------------------------------------------------------------------------------------------------- 

#find patient by ID---------------------------------------------------------------------------------------------------- 
    @classmethod
    def find_patient_by_id(cls, patient_id):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'patients.txt')
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    patient_data = line.strip().split(',')
                    if len(patient_data) >= 1 and patient_data[0] == str(patient_id):
                        first_name = patient_data[1]
                        last_name = patient_data[2]
                        age = int(patient_data[3])
                        gender = patient_data[4]
                        contact_number = patient_data[5]
                        return cls(first_name, last_name, age, gender, contact_number)
        except FileNotFoundError:
            pass
        # Patient with the specified ID not found
        return None
# --------------------------------------------------------------------------------------------------------------------- 

#check if patient exists-----------------------------------------------------------------------------------------------
    def patient_exists(patient_id):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'patients.txt')
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    # Split the line by comma and compare the first element (ID)
                    current_patient_id = line.split(',')[0].strip()
                    if current_patient_id == str(patient_id):
                        return True
        except FileNotFoundError:
            print(f"Error: Unable to open {file_path}.")
        return False
# --------------------------------------------------------------------------------------------------------------------- 

# Add patient----------------------------------------------------------------------------------------------------------
    @staticmethod
    def add_patient(first_name, last_name, age, gender, contact_number):
        new_patient = Patient(first_name, last_name, age, gender, contact_number)
        new_patient.save()
        return new_patient
# --------------------------------------------------------------------------------------------------------------------- 

# View all patients----------------------------------------------------------------------------------------------------
    @staticmethod
    def view_all_patients():
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'patients.txt')
        try:
            with open(file_path, 'r') as file:
                patients = file.readlines()
            if not patients:
                print("No patients are currently registered in the system.")
                return []
            print("Patient ID | First Name | Last Name | Age | Gender | Contact Number")
            for patient in patients:
                patient_id, first_name, last_name, age, gender, contact_number = patient.strip().split(',')
                print(f"{patient_id} | {first_name} | {last_name} | {age} | {gender} | {contact_number}")
            return patients
        except FileNotFoundError:
            print("Patient data file not found.")
            return []
# --------------------------------------------------------------------------------------------------------------------- 

# Update patient--------------------------------------------------------------------------------------------------------
    def update_patient(self, **kwargs):
        for field, value in kwargs.items():
            if hasattr(self, field):
                setattr(self, field, value)
            else:
                raise ValueError(f"Invalid field '{field}' for patient update.")
        self.save() 
# --------------------------------------------------------------------------------------------------------------------- 
    
#Delete Patient------------------------------------------------------------------------------------------------------- 
    @staticmethod
    def delete_patient(patient_id):
        patients_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'patients.txt')
        bookings_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'bookings.txt')

        try:
            # Remove patient from patients.txt
            with open(patients_file_path, 'r') as file:
                patients = file.readlines()
            patients = [patient for patient in patients if patient.split(',')[0] != str(patient_id)]
            with open(patients_file_path, 'w') as file:
                file.writelines(patients)
        except FileNotFoundError:
            print("Patient data file not found.")
            return

        try:
            # Update bookings in bookings.txt
            with open(bookings_file_path, 'r') as file:
                bookings = file.readlines()
            updated_bookings = []
            for booking in bookings:
                parts = booking.split(',')
                if parts[2] == str(patient_id):  # Check if the patient_id matches
                    parts[2] = '0'  # Set patient_id to 0
                updated_bookings.append(','.join(parts))
            with open(bookings_file_path, 'w') as file:
                file.writelines(updated_bookings)
        except FileNotFoundError:
            print("Booking data file not found.")
# --------------------------------------------------------------------------------------------------------------------- 
  
#Validate patient ID---------------------------------------------------------------------------------------------------
    @staticmethod
    def validate_patient_id():
        print("\nList of Registered Patients:")
        Patient.view_all_patients()
        try:
            patient_id = int(input("Enter the new patient ID (or 0 for no patient): "))
            if patient_id == 0 or Patient.patient_exists(patient_id):
                patient = Patient.find_patient_by_id(patient_id)
                if patient:
                    patient.patient_id = patient_id
                    return patient_id
                else:
                    print("Patient not found.")
                    return None
            else:
                print("Invalid patient ID. Patient does not exist.")
                return None
        except ValueError:
            print("Please enter a valid number.")
            return None
# --------------------------------------------------------------------------------------------------------------------- 

#__________________________________________________________________________________________________________________
#                                               Booking Class
#__________________________________________________________________________________________________________________

class Booking:
    def __init__(self, room_id, patient_id, start_date, end_date, user_id, booking_id=None, status=None):
        if booking_id is None:
            self.booking_id = self.generate_new_booking_id()
        else:
            self.booking_id = booking_id
        self.room_id = room_id
        self.patient_id = patient_id
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M") if isinstance(start_date, str) else start_date
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M") if isinstance(end_date, str) else end_date
        self.user_id = user_id
        self.status = status if status is not None else Confirmed()  # Initialize with an instance of Confirmed

# Change booking status---------------------------------------------------------------------------------------------------
    def change_status(self, new_status):
        self.status = new_status
# --------------------------------------------------------------------------------------------------------------------- 

#generate booking id--------------------------------------------------------------------------------------------------------
    @staticmethod
    def generate_new_booking_id():
        highest_id = 0
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'bookings.txt')
        # Check if file exists and is not empty
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            try:
                with open(file_path, 'r') as file:
                    for line in file:
                        parts = line.strip().split(',', 1)
                        if len(parts) >= 2:
                            booking_id = int(parts[0])
                            highest_id = max(highest_id, booking_id)
            except IOError as e:
                print(f"Error reading file: {e}")

        return highest_id + 1
# --------------------------------------------------------------------------------------------------------------------- 

#save-------------------------------------------------------------------------------------------------------------------
    def save(self):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'bookings.txt')
        start_date_str = self.start_date.strftime("%Y-%m-%d %H:%M")
        end_date_str = self.end_date.strftime("%Y-%m-%d %H:%M")
        booking_data = f"{self.booking_id},{self.room_id},{self.patient_id},{start_date_str},{end_date_str},{self.user_id},{self.status}\n"
        with open(file_path, 'a') as file: 
            file.write(booking_data)
# --------------------------------------------------------------------------------------------------------------------- 

# Update-----------------------------------------------------------------------------------------------------------------
    def update(self):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'bookings.txt')

        try:
            with open(file_path, 'r') as file:
                bookings = file.readlines()

            updated = False
            for i in range(len(bookings)):
                booking_data = bookings[i].strip().split(',')
                if len(booking_data) >= 7 and int(booking_data[0]) == self.booking_id:
                    start_date_str = self.start_date.strftime("%Y-%m-%d %H:%M")
                    end_date_str = self.end_date.strftime("%Y-%m-%d %H:%M")
                    status_str = self.status.__class__.__name__  # Get the name of the status class
                    # Preserve original user_id (stops admin updates changing staff bookings)
                    original_user_id = booking_data[5]
                    updated_booking_data = f"{self.booking_id},{self.room_id},{self.patient_id},{start_date_str},{end_date_str},{original_user_id},{status_str}\n"
                    bookings[i] = updated_booking_data
                    updated = True
                    break

            if updated:
                with open(file_path, 'w') as file:
                    file.writelines(bookings)
            else:
                raise ValueError(f"No booking found with ID {self.booking_id}")

        except IOError as e:
            print(f"An error occurred while updating the booking: {e}")
# --------------------------------------------------------------------------------------------------------------------- 
   
#map names to classes---------------------------------------------------------------------------------------------------
    @staticmethod
    def map_status(status_name):
        status_mapping = {
            "Confirmed": Confirmed(),
            "Cancelled": Cancelled()
        }
        return status_mapping.get(status_name, None)
# --------------------------------------------------------------------------------------------------------------------- 

#find booking by id---------------------------------------------------------------------------------------------------
    @classmethod
    def find_booking_by_id(cls, booking_id):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'bookings.txt')
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    booking_data = line.strip().split(',')
                    if len(booking_data) >= 7 and int(booking_data[0]) == booking_id:
                        room_id = int(booking_data[1])

                        # Handle case where patient_id is missing or 'None'
                        patient_id_str = booking_data[2].strip()
                        patient_id = int(patient_id_str) if patient_id_str and patient_id_str != 'None' else None

                        start_date = datetime.strptime(booking_data[3], "%Y-%m-%d %H:%M")
                        end_date = datetime.strptime(booking_data[4], "%Y-%m-%d %H:%M")
                        user_id = int(booking_data[5])
                        # Get the status class name and find the corresponding status instance
                        status_class_name = booking_data[6]
                        if status_class_name:
                            status_instance = globals().get(status_class_name)()
                        else:
                            status_instance = None

                        # Return a Booking instance with the correct booking_id and status
                        return cls(room_id, patient_id, start_date, end_date, user_id, booking_id=booking_id, status=status_instance)
        except FileNotFoundError:
            print("Error: bookings.txt file not found.")
            return None
        except ValueError as e:
            print(f"Error: {e}")
            return None
# --------------------------------------------------------------------------------------------------------------------- 

#check booking exists----------------------------------------------------------------------------------------------------
    @classmethod
    def booking_exists(cls, booking_id):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'bookings.txt')
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    current_booking_id, _, _, _, _ = line.strip().split(',')
                    if current_booking_id == str(booking_id):
                        return True
        except FileNotFoundError:
            pass
        return False
# --------------------------------------------------------------------------------------------------------------------- 
    
# Check Room Availability----------------------------------------------------------------------------------------------
    @classmethod
    def check_room_availability(cls, room, start_time, end_time):
        file_path_rooms = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'rooms.txt')
        file_path_bookings = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'bookings.txt')

        try:
            # Check room availability based on rooms.txt
            with open(file_path_rooms, 'r') as rooms_file:
                rooms = rooms_file.readlines()
            room_found = False
            for room_data in rooms:
                room_info = room_data.strip().split(',')
                if len(room_info) >= 4:
                    room_id = int(room_info[0])
                    available_from = datetime.strptime(room_info[2], "%Y-%m-%d").date()  # Date only
                    available_to = datetime.strptime(room_info[3], "%Y-%m-%d").date()  # Date only

                    if room_id == room:
                        room_found = True
                        if available_from <= start_time.date() <= available_to:
                            break  # Room is available based on rooms.txt
                        else:
                            return False  # Room is not available based on rooms.txt

            if not room_found:
                return False  # Room is not found in rooms.txt

            # Check if the room is already booked based on bookings.txt
            if os.path.exists(file_path_bookings):
                with open(file_path_bookings, 'r') as bookings_file:
                    bookings = bookings_file.readlines()
                for booking_data in bookings:
                    booking_info = booking_data.strip().split(',')
                    if len(booking_info) >= 5:
                        booking_room_id = int(booking_info[1])
                        booking_start_time = datetime.strptime(booking_info[3], "%Y-%m-%d %H:%M")
                        booking_end_time = datetime.strptime(booking_info[4], "%Y-%m-%d %H:%M")

                        if booking_room_id == room and cls.is_time_overlap(start_time, end_time, booking_start_time, booking_end_time):
                            # Check if the booking is not cancelled
                            booking_status = booking_info[6]
                            if booking_status.lower() != "cancelled":
                                return False  # Room is not available due to an existing non-cancelled booking

            return True  # Room is available
        except FileNotFoundError:
            return True  # If file not found, assume room is available
# --------------------------------------------------------------------------------------------------------------------- 


#check for timeoverlap-------------------------------------------------------------------------------------------------
    @staticmethod
    def is_time_overlap(start_time1, end_time1, start_time2, end_time2):
        # Ensure that all arguments are datetime objects
        if not all(isinstance(dt, datetime) for dt in [start_time1, end_time1, start_time2, end_time2]):
            raise ValueError("All arguments must be datetime objects")

        # Check if there's a time overlap between two time intervals
        return start_time1 < end_time2 and start_time2 < end_time1
# --------------------------------------------------------------------------------------------------------------------- 

#make booking----------------------------------------------------------------------------------------------------------
    @classmethod
    def make_booking(cls, room_id, patient_id, start_time, end_time, user_id):
        if cls.check_room_availability(room_id, start_time, end_time):
            # Create a new booking with confirmed status
            new_booking = cls(room_id, patient_id, start_time, end_time, user_id)
            new_booking.status = "Confirmed"  # Set status to "Confirmed"
            new_booking.save()  # Save the booking details
            return new_booking
        else:
            return None
# --------------------------------------------------------------------------------------------------------------------- 
   
#validate booking dates-------------------------------------------------------------------------------------------------
    @staticmethod
    def validate_booking_dates():
        current_datetime = datetime.now()
        try:
            new_start_date_input = input("Enter the new start date and time (YYYY-MM-DD HH:MM): ")
            new_start_datetime = datetime.strptime(new_start_date_input, "%Y-%m-%d %H:%M")
            if new_start_datetime < current_datetime:
                print("Start date/time cannot be in the past.")
                return None, None

            new_end_date_input = input("Enter the new end date and time (YYYY-MM-DD HH:MM): ")
            new_end_datetime = datetime.strptime(new_end_date_input, "%Y-%m-%d %H:%M")
            if new_end_datetime <= new_start_datetime:
                print("End date/time must be after the start date/time.")
                return None, None

            return new_start_datetime, new_end_datetime
        except ValueError:
            print("Invalid date format. Please enter date and time in the format YYYY-MM-DD HH:MM.")
            return None, None
 # --------------------------------------------------------------------------------------------------------------------- 
   
# View bookings---------------------------------------------------------------------------------------------------------
    @staticmethod
    def view_bookings(user_id=None):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'bookings.txt')
        try:
            with open(file_path, 'r') as file:
                bookings = file.readlines()
            if not bookings:
                print("No bookings are currently in the system.")
                return []

            room_data = {}
            rooms_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'rooms.txt')
            with open(rooms_file_path, 'r') as rooms_file:
                room_lines = rooms_file.readlines()
                for room_line in room_lines:
                    room_id, room_type, _, _ = room_line.strip().split(',')
                    room_data[room_id] = room_type

            print("Booking ID | Room ID | Room Type | Patient Name | Date Time")
            patients = {}
            patients_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'patients.txt')
            with open(patients_file_path, 'r') as patient_file:
                patient_data = patient_file.readlines()
                for line in patient_data:
                    patient_id, first_name, last_name, *_ = line.strip().split(',')
                    patients[patient_id] = f"{first_name} {last_name}"

            for booking in bookings:
                booking_parts = booking.strip().split(',')
                if len(booking_parts) == 7:
                    booking_id, room_id, patient_id, start_time, end_time, booked_user_id, status = booking_parts
                    if status == "Confirmed" and (user_id is None or booked_user_id == str(user_id)):
                        patient_name = patients.get(patient_id, "Unknown Patient")
                        room_type = room_data.get(room_id, "Unknown Room Type")
                        print(f"{booking_id} | {room_id} | {room_type} | {patient_name} | {start_time} - {end_time}")

            return bookings
        except FileNotFoundError:
            print("Booking data file not found.")
            return []

#State Pattern#
#__________________________________________________________________________________________________________________
#                                      Booking Status Base Class
#__________________________________________________________________________________________________________________
class BookingStatus:
    def cancel(self, booking):
        # Default behavior: Do nothing
        pass

#__________________________________________________________________________________________________________________
#                                      Confirmed Status Class
#__________________________________________________________________________________________________________________
class Confirmed:
    def cancel(self, booking):
        booking.change_status(Cancelled())

#__str__----------------------------------------------------------------------------------------------------------
    def __str__(self):
        return "Confirmed"
# --------------------------------------------------------------------------------------------------------------------- 

#__________________________________________________________________________________________________________________
#                                        Cancelled Status Class
#__________________________________________________________________________________________________________________
class Cancelled:
    def cancel(self, booking):
        pass  # Booking is already cancelled
    
#__str__----------------------------------------------------------------------------------------------------------
    def __str__(self):
        return "Cancelled"
# --------------------------------------------------------------------------------------------------------------------- 