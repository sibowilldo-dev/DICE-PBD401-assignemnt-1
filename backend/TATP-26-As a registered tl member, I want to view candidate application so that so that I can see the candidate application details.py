# import the necessary modules
from models import application
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# create an engine to connect to the database
engine = create_engine('sqlite:///user.db')

# create a session factory
Session = sessionmaker(bind=engine)


# create a function to retrieve the applicant details
def get_applicant_details(applicant_id):
    # create a session object
    session = Session()

    # retrieve the applicant details by applicant ID
    applicant = session.query(application).filter_by(id=applicant_id).first()
    # check if the applicant exists
    if applicant:
        # print the applicant details
        print(f"Applicant ID: {applicant.id}")
        print(f"Email: {applicant.email}")
        print(f"status Id: {applicant.phone}")
        # add more fields as needed
    else:
        print("Applicant not found")


# prompt the user to enter an applicant ID and call the function
applicant_id = input("Enter the applicant ID: ")
get_applicant_details(applicant_id)

