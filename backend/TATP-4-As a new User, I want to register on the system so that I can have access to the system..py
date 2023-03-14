from flask import Flask, render_template, request, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy
from models import db, User
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")
db = SQLAlchemy(app)

oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=os.environ.get("CLIENT_ID"),
    client_secret=os.environ.get("CLIENT_SECRET"),
    api_base_url=os.environ.get("API_BASE_URL"),
    access_token_url=os.environ.get("ACCESS_TOKEN_URL"),
    authorize_url=os.environ.get("AUTHORIZE_URL"),
    client_kwargs={
        'scope': 'openid profile email',
    },
)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=url_for('callback', _external=True))

@app.route('/callback')
def callback():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    session['jwt_payload'] = userinfo
    session['profile'] = {
        'id': userinfo['sub'],
        'name': userinfo['name'],
        'email': userinfo['email']
    }

    # Check if user already exists in the database
    user = User.query.filter_by(id=userinfo['sub']).first()
    if user is None:
        # Create a new user record in the database
        user = User(id=userinfo['sub'], name=userinfo['name'], email=userinfo['email'])
        db.session.add(user)
        db.session.commit()

    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'profile' in session:
        profile = session['profile']
        return render_template('dashboard.html', profile=profile)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
