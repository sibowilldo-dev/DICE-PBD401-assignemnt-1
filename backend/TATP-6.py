from flask import Flask, session, redirect, request, url_for
from auth0.v3.authentication import GetToken
from auth0.v3.authentication import Users

app = Flask(__name__)
app.secret_key = 'your_secret_key'

AUTH0_DOMAIN = 'your_auth0_domain'
AUTH0_CLIENT_ID = 'your_auth0_client_id'
AUTH0_CLIENT_SECRET = 'your_auth0_client_secret'

@app.route('/')
def index():
    if 'profile' in session:
        return 'You are logged in as ' + session['profile']['email']
    else:
        return 'Please log in <a href="/login">here</a>.'

@app.route('/login')
def login():
    return redirect('https://' + AUTH0_DOMAIN + '/authorize?' +
                    'response_type=code&client_id=' + AUTH0_CLIENT_ID +
                    '&redirect_uri=' + url_for('callback', _external=True) +
                    '&scope=openid%20profile&audience=https://' + AUTH0_DOMAIN + '/userinfo')

@app.route('/callback')
def callback():
    code = request.args.get('code')

    # Exchange the code for an access token
    get_token = GetToken(AUTH0_DOMAIN)
    token = get_token.authorization_code(AUTH0_CLIENT_ID,
                                          AUTH0_CLIENT_SECRET,
                                          code,
                                          url_for('callback', _external=True))

    # Use the access token to get the user's profile information
    users = Users(AUTH0_DOMAIN)
    user_info = users.userinfo(token['access_token'])

    # Store the access token and user profile in the session
    session['access_token'] = token['access_token']
    session['profile'] = user_info

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
