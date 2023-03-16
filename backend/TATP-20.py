from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0 as ManagementAuth0
from auth0.v3.exceptions import Auth0Error
from flask import Flask, request

app = Flask(__name__)

# Configuration for the Auth0 Management API
AUTH0_DOMAIN = 'your-auth0-domain.auth0.com'
AUTH0_CLIENT_ID = 'your-auth0-client-id'
AUTH0_CLIENT_SECRET = 'your-auth0-client-secret'
AUTH0_AUDIENCE = f'https://{AUTH0_DOMAIN}/api/v2/'

# Create an instance of the Auth0 Management API
auth0_token = GetToken(AUTH0_DOMAIN).client_credentials(AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_AUDIENCE)
auth0 = ManagementAuth0(AUTH0_DOMAIN, auth0_token['access_token'])

@app.route('/change-password', methods=['POST'])
def change_password():
    # Get the user's access token from the Authorization header
    access_token = request.headers.get('Authorization').split()[1]

    # Get the user's current password and new password from the request body
    current_password = request.json.get('current_password')
    new_password = request.json.get('new_password')

    try:
        # Call the Auth0 Management API to update the user's password
        auth0.users.update_user_password(user_id='me', connection_id='Username-Password-Authentication',
                                          password=current_password, new_password=new_password,
                                          include_email_in_welcome_email=False, email_verified=True,
                                          client_id=AUTH0_CLIENT_ID, access_token=access_token)

        # Return a success message to the user
        return {'message': 'Password updated successfully'}, 200

    except Auth0Error as e:
        # Return an error message to the user if the password change fails
        return {'message': 'Failed to update password', 'error': str(e)}, 400
