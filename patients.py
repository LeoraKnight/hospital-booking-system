#__________________________________________________________________________________________________________________
#                                               Import 
#__________________________________________________________________________________________________________________
import os
from entities import Admin, Staff, UserManager, Patient, Admin
from datetime import datetime

# Main Menu for Patient Management---------------------------------------------------------------------------------
def patient_management_menu():
    print("\nPatient Management System")
    print("1. Add Patient")
    print("2. Manage Patients")
    print("3. Exit")
    choice = input("Enter your choice: ")
    return choice
#------------------------------------------------------------------------------------------------------------------

# Submenu for Managing Patients-----------------------------------------------------------------------------------
def manage_patients_menu():
    print("\nManage Patients")
    print("1. View All Patients")
    print("2. Update Patient")
    print("3. Delete Patient")
    print("4. Return to Main Menu")
    choice = input("Enter your choice: ")
    return choice
#------------------------------------------------------------------------------------------------------------------

# Add patient-------------------------------------------------------------------------------------------------------
def add_patient(user):
    if not (isinstance(user, Admin) or isinstance(user, Staff)):
        print("Only Admin or Staff can add patients.")
        return

    while True:
        first_name = input("Enter patient's first name or type 'cancel' to return: ")
        if first_name.lower() == 'cancel':
            print("Operation cancelled. Returning to previous menu.")
            return
        if first_name.isalpha():
            break
        print("Invalid input for first name. Please enter only alphabetic characters.")

    while True:
        last_name = input("Enter patient's last name or type 'cancel' to return: ")
        if last_name.lower() == 'cancel':
            print("Operation cancelled. Returning to previous menu.")
            return
        if last_name.isalpha():
            break
        print("Invalid input for last name. Please enter only alphabetic characters.")

    while True:
        age_input = input("Enter patient's age or type 'cancel' to return: ")
        if age_input.lower() == 'cancel':
            print("Operation cancelled. Returning to previous menu.")
            return
        try:
            age = int(age_input)
            if age < 0:
                print("Invalid age. Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid age. Please enter a numeric value.")

    while True:
        gender = input("Enter patient's gender or type 'cancel' to return: ")
        if gender.lower() == 'cancel':
            print("Operation cancelled. Returning to previous menu.")
            return
        if gender.lower() in ['male', 'female', 'other']:
            break
        print("Invalid gender. Please enter 'male', 'female', or 'other'.")

    while True:
        contact_number = input("Enter patient's contact number or type 'cancel' to return: ")
        if contact_number.lower() == 'cancel':
            print("Operation cancelled. Returning to previous menu.")
            return
        if contact_number.isdigit() and len(contact_number) >= 5: 
            break
        print("Invalid contact number. Please enter a valid number.")

    Patient.add_patient(first_name, last_name, age, gender, contact_number)
#------------------------------------------------------------------------------------------------------------------

# List all patients------------------------------------------------------------------------------------------------
def list_patients():
    print("\nCurrent Patients List:")
    Patient.view_all_patients()
#------------------------------------------------------------------------------------------------------------------

# Update Patient--------------------------------------------------------------------------------------------------
def update_patient(user):
    list_patients()
    
    patient_id_input = input("\nEnter the ID of the patient you want to update or type 'cancel' to return: ")
    if patient_id_input.lower() == 'cancel':
        print("Returning to main menu.")
        return

    try:
        patient_id = int(patient_id_input)
    except ValueError:
        print("Invalid patient ID. Please enter a numeric ID.")
        return

    patient = Patient.find_patient_by_id(patient_id)
    if patient is None:
        print(f"Patient with ID '{patient_id}' not found.")
        return

    patient.patient_id = patient_id  # Explicitly set ID to fix ID error

    while True:
        print("\nWhich field would you like to update?")
        print("1. First Name")
        print("2. Last Name")
        print("3. Age")
        print("4. Gender")
        print("5. Contact Number")
        print("6. Return to main Menu")

        choice = input("Enter your choice: ")
        field_updated = False

        if choice == '1':
            new_first_name = input("Enter the new first name for the patient: ")
            patient.first_name = new_first_name
            field_updated = "First Name"
        elif choice == '2':
            new_last_name = input("Enter the new last name for the patient: ")
            patient.last_name = new_last_name
            field_updated = "Last Name"
        elif choice == '3':
            new_age = input("Enter the new age for the patient: ")
            patient.age = int(new_age)
            field_updated = "Age"
        elif choice == '4':
            new_gender = input("Enter the new gender for the patient: ")
            patient.gender = new_gender
            field_updated = "Gender"
        elif choice == '5':
            new_contact_number = input("Enter the new contact number for the patient: ")
            patient.contact_number = new_contact_number
            field_updated = "Contact Number"
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

        if field_updated:
            patient.update()
            print(f"{field_updated} for patient ID {patient_id} updated successfully.")
#------------------------------------------------------------------------------------------------------------------

# Delete Patient---------------------------------------------------------------------------------------------------
def delete_patient(user):
    list_patients()
    
    patient_id_input = input("\nEnter the ID of the patient you want to delete or type 'cancel' to return: ")
    if patient_id_input.lower() == 'cancel':
        print("Returning to main menu.")
        return

    try:
        patient_id = int(patient_id_input)
        patient = Patient.find_patient_by_id(patient_id)
        if patient is None:
            print(f"Patient with ID '{patient_id}' not found. Please enter a valid ID.")
            return
    except ValueError:
        print("Invalid patient ID. Please enter a numeric ID.")
        return

    confirmation = input(f"Are you sure you want to delete the patient with ID '{patient_id}'? This action cannot be undone. Type 'yes' to confirm: ")
    if confirmation.lower() == 'yes':
        Patient.delete_patient(patient_id)
        print(f"Patient with ID '{patient_id}' has been successfully deleted.")
    else:
        print("Patient deletion cancelled.")
#------------------------------------------------------------------------------------------------------------------

# View all patients-------------------------------------------------------------------------------------------------
def view_all_patients(user):
    list_patients()
    input("Press Enter to return")
#------------------------------------------------------------------------------------------------------------------

# Manage Patients-------------------------------------------------------------------------------------------------
def manage_patients(user):
    while True:
        choice = manage_patients_menu()
        if choice == '1':
            view_all_patients(user)
        elif choice == '2':
            update_patient(user)
        elif choice == '3':
            delete_patient(user)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")
#------------------------------------------------------------------------------------------------------------------

# Main Function----------------------------------------------------------------------------------------------------
def main(user): #accepts any user 
    print("Welcome to the Patient Management System")

    # Verify that the user is either an Admin or Staff
    if not (isinstance(user, Admin) or isinstance(user, Staff)):
        print("Access denied. This system is only accessible to staff and administrators.")
        return

    while True:
        choice = patient_management_menu()
        if choice == '1':
            add_patient(user)
        elif choice == '2':
            manage_patients(user)
        elif choice == '3':
            print("Exiting Patient Management System.")
            break
        else:
            print("Invalid choice. Please try again.")
#------------------------------------------------------------------------------------------------------------------

