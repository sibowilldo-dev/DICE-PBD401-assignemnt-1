from flask import Flask, request
from authlib.integrations.flask_client import OAuth
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'your-database-uri'
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['AUTH0_DOMAIN'] = 'your-auth0-domain'
app.config['AUTH0_CLIENT_ID'] = 'your-auth0-client-id'
app.config['AUTH0_CLIENT_SECRET'] = 'your-auth0-client-secret'
app.config['AUTH0_CALLBACK_URL'] = 'http://localhost:5000/callback'

db.init_app(app)

oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=app.config['AUTH0_CLIENT_ID'],
    client_secret=app.config['AUTH0_CLIENT_SECRET'],
    api_base_url=f'https://{app.config["AUTH0_DOMAIN"]}',
    access_token_url=f'https://{app.config["AUTH0_DOMAIN"]}/oauth/token',
    authorize_url=f'https://{app.config["AUTH0_DOMAIN"]}/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)



@app.route('/reset_password', methods=['POST'])
def get_password_reset_link():
    access_token = auth0.authorize_access_token()
    user = User.get_by_auth0_id(access_token['sub'])
    if not user:
        return 'User not found'
    redirect_uri = request.host_url + 'callback'
    return auth0.authorize_redirect(redirect_uri=redirect_uri, audience=f'https://{app.config["AUTH0_DOMAIN"]}/api/v2/')


@app.route('/callback')
def callback_handling():
    # handle the auth0 callback here
    pass

