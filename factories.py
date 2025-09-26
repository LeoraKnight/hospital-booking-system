#__________________________________________________________________________________________________________________
#                                               Import 
#__________________________________________________________________________________________________________________
from entities import Admin, Staff

#__________________________________________________________________________________________________________________
#----------------------------------------------classes-------------------------------------------------------------
#__________________________________________________________________________________________________________________

#__________________________________________________________________________________________________________________
#                                           UserFactory Class
#__________________________________________________________________________________________________________________
#Factory method for creating user types (currently limited to admin and staff)
class UserFactory:
    @staticmethod
    def create_user(role, username, password, first_name, last_name, email, job_title, security_question, security_answer, user_id=None):
        if role == 'admin':
            return Admin(username=username, password=password, first_name=first_name, last_name=last_name, email=email, job_title=job_title, security_question=security_question, security_answer=security_answer, user_id=user_id)
        elif role == 'staff':
            return Staff(username=username, password=password, first_name=first_name, last_name=last_name, email=email, job_title=job_title, security_question=security_question, security_answer=security_answer, user_id=user_id)
        else:
            raise ValueError("Invalid role specified when creating a user.")



        


