import requests
import os
import time
from requests_oauthlib import OAuth2Session

os.environ['DEBUG'] = '1'
api_key = '16k7wi51gfrm'
sec_key = 'rvGAHWyoOq3hbqi9'
app_name = 'my_website'

site = 'https://www.linkedin.com'
auth_url = '/uas/oauth2/authorization'
token_url = '/uas/oauth2/accessToken'

client_id = api_key
client_secret = sec_key
redirect_uri = 'http://www.kashyapmaduri.com'

url1 = 'https://www.linkedin.com/uas/oauth2/authorization?response_type=code&client_id=16k7wi51gfrm&state=DCEEFWF45453sdffef424&redirect_uri=http://www.kashyapmaduri.com'
linkedIn = OAuth2Session(client_id, redirect_uri=redirect_uri)

auth_url, state = linkedIn.authorization_url(site + auth_url)

print 'pleas go here and authorize, ', auth_url

redirect_response = raw_input('redirect_uri')

linkedIn.fetch_token(site + token_url, client_secret = client_secret,
                    authorization_response = redirect_response)

r = linkedIn.get('https://www.linkedin.com/v1/people/~')


