import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from werkzeug.exceptions import Forbidden, Unauthorized, BadRequest

from auth.auth import AuthError, requires_auth

load_dotenv('.env')

app = Flask(__name__, instance_relative_config=True)
CORS(app, resources={r"/api/*": {"origins": "*"}})

api_route = os.getenv("API_URL", "/api/v1")

app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)


@app.route(f"{api_route}/vacancy/<int:vacancy_id>/apply", methods=['POST'])
@requires_auth('post:vacancy-apply')
def vacancy_apply(payload, vacancy_id):
    try:
        vacancy = None  # get this using vacancy_id
        applicant = None  # get this using applicant_id/logged-in user_id
        # link vacancy and applicant to applications table
        return jsonify({
            "success": True,
            "message": "Your application was submitted. Good Luck!",
            "vacancy": vacancy,
            "applicant": applicant,
        }), 200
    except Forbidden or Unauthorized or BadRequest:
        raise AuthError


@app.route('/login')
def login():
    return jsonify('You\'re logging in!'), 200


@app.errorhandler(422)
def unprocessable():
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.error['code'],
        "message": error.error['description']
    }), error.status_code
