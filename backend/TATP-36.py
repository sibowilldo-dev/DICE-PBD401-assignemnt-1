from flask import Flask, render_template, request
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0 as Auth0Management
import os


# Configure the application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure the login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Configure the database
db = SQLAlchemy(app)

# Configure Auth0
auth0_domain = os.environ.get('AUTH0_DOMAIN')
auth0_client_id = os.environ.get('AUTH0_CLIENT_ID')
auth0_client_secret = os.environ.get('AUTH0_CLIENT_SECRET')
auth0_api_identifier = os.environ.get('AUTH0_API_IDENTIFIER')
auth0_get_token = GetToken(auth0_domain)
auth0_token = auth0_get_token.client_credentials(auth0_client_id, auth0_client_secret, auth0_api_identifier)
auth0_mgmt = Auth0Management(auth0_domain, auth0_token['access_token'])


# Define the user model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80))
    role = db.Column(db.String(20))


# Define the login manager callbacks
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    return 'Unauthorized'


# Define the routes
@app.route('/')
def index():
    return 'Hello, world!'


@app.route('/login')
def login():
    return 'Login'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out'


@app.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        new_user = User(username=username, email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        return 'User created'
    else:
        return render_template('create_user.html')


# Run the application
if __name__ == '__main__':
    app.run()


