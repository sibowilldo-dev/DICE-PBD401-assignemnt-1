from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+mysqlconnector://admin:password@localhost/mydb')

Session = sessionmaker(bind=engine)

# create base model class
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    given_name = Column(String(50))
    family_name = Column(String(50))
    name = Column(String(100))


# create session
session = Session()

class UpdateUser:
    def __init__(self):
        self.user_id = input("Enter user id: ")
        self.given_name = input("Enter given name: ")
        self.family_name = input("Enter family name: ")
        self.name = input("Enter name: ")

    def update_user(self):
        # retrieve user by id
        user = session.query(User).filter_by(id=self.user_id).first()

        if not user:
            print("User not found.")
            return

        # update user attributes
        user.given_name = self.given_name
        user.family_name = self.family_name
        user.name = self.name
        session.commit()
        print("User updated successfully.")

    def __del__(self):
        # close session
        session.close()


# create instance of UpdateUser and call update_user() method
update_user = UpdateUser()
update_user.update_user()
