from flask import Flask, request, jsonify

from backend.database.models import Application
from database import models

app = Flask(__name__)

# Set up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Application.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/applications/<int:vacancy_id>', methods=['GET'])
def get_applicants_by_vacancy(vacancy_id):
    try:
        # Retrieve applicants based on vacancy_id
        applicant_list = []
        query = Application.query.filter_by(vacancy_id=vacancy_id).all()
        for applicant in query:
            applicant_dict = {
                'id': Application.id,
                'user_id': Application.user_id,
                'status_id': Application.status_id,
                'vacancy_id': Application.vacancy_id

            }
            applicant_list.append(applicant_dict)

        # Return JSON response
        return jsonify(applicant_list)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)