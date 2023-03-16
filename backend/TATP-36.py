from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+mysql connector://admin:password@localhost/mydb')

Session = sessionmaker(bind=engine)

# create base model class
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(50))


# create session
session = Session()


class UpdateUserEmail:
    def __init__(self):
        self.user_id = input("Enter user id: ")
        self.email = input("Enter new email: ")

    def update_email(self):
        # retrieve user by id
        user = session.query(User).filter_by(id=self.user_id)

        if not user:
            print("User not found.")
            return

        # update user email
        user.email = self.email
        session.commit()
        print("User email updated successfully.")

    def __del__(self):
        # close session
        session.close()


# create instance of UpdateUserEmail and call update_email() method
update_user_email = UpdateUserEmail()
update_user_email.update_email()
