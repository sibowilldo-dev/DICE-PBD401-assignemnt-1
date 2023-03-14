from flask import Flask, request, redirect, session, render_template
import json
import requests

app = Flask(__name__)

# Set up the Auth0 credentials
AUTH0_DOMAIN = 'your-auth0-domain.auth0.com'
AUTH0_API_IDENTIFIER = 'your-auth0-api-identifier'
AUTH0_CLIENT_ID = 'your-auth0-client-id'
AUTH0_CLIENT_SECRET = 'your-auth0-client-secret'

# Set up the routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return redirect(f'https://{AUTH0_DOMAIN}/authorize?response_type=code&client_id={AUTH0_CLIENT_ID}&redirect_uri=http://localhost:5000/callback&scope=openid%20profile%20email')

@app.route('/callback')
def callback():
    auth0_url = f'https://{AUTH0_DOMAIN}/oauth/token'
    auth0_data = {
        'grant_type': 'authorization_code',
        'client_id': AUTH0_CLIENT_ID,
        'client_secret': AUTH0_CLIENT_SECRET,
        'code': request.args.get('code'),
        'redirect_uri': 'http://localhost:5000/callback'
    }
    auth0_headers = {'content-type': 'application/json'}
    response = requests.post(auth0_url, data=json.dumps(auth0_data), headers=auth0_headers)
    session['access_token'] = response.json()['access_token']
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'access_token' not in session:
        return redirect('/login')
    else:
        user_info = get_user_info(session['access_token'])
        return render_template('dashboard.html', user_info=user_info)

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'access_token' not in session:
        return redirect('/login')
    else:
        if request.method == 'POST':
            user_id = request.form['user_id']
            new_password = request.form['new_password']
            update_password(user_id, new_password, session['access_token'])
            return redirect('/dashboard')
        else:
            user_info = get_user_info(session['access_token'])
            return render_template('change_password.html', user_info=user_info)

# Helper functions
def get_user_info(access_token):
    user_info_url = f'https://{AUTH0_DOMAIN}/userinfo'
    user_info_headers = {
        'content-type': 'application/json',
        'authorization': f'Bearer {access_token}'
    }
    response = requests.get(user_info_url, headers=user_info_headers)
    return response.json()

def update_password(user_id, new_password, access_token):
    update_url = f'https://{AUTH0_DOMAIN}/api/v2/users/{user_id}'
    update_data = {
        'password': new_password,
        'connection': 'Username-Password-Authentication'
    }
    update_headers = {
        'content-type': 'application/json',
        'authorization': f'Bearer {access_token}',
        'auth0-api': AUTH0_API_IDENTIFIER
    }
    response = requests.patch(update_url, data=json.dumps(update_data), headers=update_headers)
    if response.status_code == 200:
        print('Password updated successfully!')
    else:
        print(f'Error updating password: {response.text}')

# Start the app
if __name__ == '__main__':
    app.secret_key = 'your-secret-key'
    app.run(debug=True)
