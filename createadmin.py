#__________________________________________________________________________________________________________________
#                                               Import 
#__________________________________________________________________________________________________________________
from factories import UserFactory

#Create admin--------------------------------------------------------------------------------------------------------
def create_admin_user():
    print("Create New Admin Account")
    username = input("Enter username: ")  
    password = input("Enter password: ")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = input("Enter email: ")
    job_title = input("Enter job title: ")
    security_question = input("Enter security question: ")
    security_answer = input("Enter security answer: ")
   
    admin_user = UserFactory.create_user('admin', username, password, first_name, last_name, email, job_title, security_question, security_answer)
    
    admin_user.save()

    print(f"Admin account created for {username} with ID {admin_user.user_id}.")
#-----------------------------------------------------------------------------------------------------------------------------

#Main---------------------------------------------------------------------------------------------------------------------------
def main():
    create_admin_user()

if __name__ == "__main__":
    main()
#-----------------------------------------------------------------------------------------------------------------------------
