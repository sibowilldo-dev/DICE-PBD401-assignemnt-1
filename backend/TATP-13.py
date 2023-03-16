from flask import Flask, render_template
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from backend.database.models import Vacancy
from database import models

app = Flask(__name__)

# replace the database_url with your database URL
engine = create_engine('sqlite:///database.db', echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def index():
    # query for active vacancies ordered by created_at descending
    active_vacancies = session.query(Vacancy).filter_by(status='active').order_by(Vacancy.created_at.desc()).all()
    return render_template('index.html', vacancies=active_vacancies)

if __name__ == '__main__':
    app.run(debug=True)
