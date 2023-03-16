# import the necessary modules
from backend.database.models import Application
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# create an engine to connect to the database
engine = create_engine('sqlite:///application.db')

# create a session factory
Session = sessionmaker(bind=engine)


# H
# create a function to retrieve the applicant details
def get_applicant_details(applicant_id1):
    # create a session object
    session = Session()

    # retrieve the applicant details by applicant ID
    applicant = session.query(Application).filter_by(id=applicant_id1)

    # check if the applicant exists
    if applicant:
        # print the applicant details
        print(f"Applicant ID: {applicant.id}")
        print(f"User ID: {applicant.user_id}")
        print(f"Phone: {applicant.phone}")
        print(f"Vacancy ID: {applicant.vacancy_id}")
        # add more fields as needed
    else:
        print("Applicant not found")


# prompt the user to enter an applicant ID and call the function
applicant_id = input("Enter the applicant ID: ")
get_applicant_details(applicant_id)
