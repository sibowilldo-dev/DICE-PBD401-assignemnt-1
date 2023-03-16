from auth0.v3.authentication import GetToken
from auth0.v3.authentication import PasswordGrant

DOMAIN = 'AUTH0_DOMAIN'
CLIENT_ID = 'your_auth0_client_id'
CLIENT_SECRET = 'your_auth0_client_secret'
USERNAME = 'user@example.com'
PASSWORD = 'password'

get_token = GetToken(DOMAIN)
client_creds = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'audience': f'https://{DOMAIN}/api/v2/'
}
token = get_token.client_credentials(client_creds)['access_token']

pg = PasswordGrant(DOMAIN)
response = pg.login(
    username=USERNAME,
    password=PASSWORD,
    scope='openid profile email',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET)

if 'access_token' in response:
    print('User authenticated successfully')
    # Save the access token in a secure place for future use
    access_token = response['access_token']
else:
    print('Authentication failed')
