from rauth import OAuth2Service, OAuth2Session
from hashlib import sha1
import requests
try:
    from urlparse import parse_qsl
except ImportError:
    from cgi import parse_qsl 
from random import random

import re
import json
import os, ConfigParser


### READING the website details
config = ConfigParser.RawConfigParser()
config.read(os.path.join(os.path.abspath('..'),'my_site_key_details.ini'))


api_key = config.get('my_website_details','api_key')
sec_key = config.get('my_website_details','sec_key')
redirect_uri = config.get('my_website_details','redirect_uri')

######

site = r'https://www.linkedin.com'
auth_url = r'/uas/oauth2/authorization'
token_url = r'/uas/oauth2/accessToken/'

bs = r'https://api.linkedin.com/'
lnkdn = OAuth2Service(name = 'example',
                      client_id = api_key,
                      client_secret = sec_key,
                      authorize_url =  r'https://www.linkedin.com/uas/oauth2/authorization',
                      access_token_url = r'https://www.linkedin.com/uas/oauth2/accessToken',
                      base_url = bs)



state = sha1(str(random())).hexdigest()

params = { 'response_type': 'code',
          'state': state,
           'redirect_uri':redirect_uri,
           'scope':'r_network'}

#16K7wi!1f


authorize_url = lnkdn.get_authorize_url(**params)

print 'Visit this URL in your browser: ' + authorize_url

#url_with_code = raw_input("Copy URL from your browser's address bar: ")


# Retrieve code parameter
#code = re.search('\code=([^&]*)', url_with_code).group(1)

# Retrieve state parameter
#returned_state = re.search('\?state=([^&]*)', url_with_code).group(1)

new_url = raw_input('print the new redirected url here:\n')
query = new_url.split('?', 1)[-1]
query = dict(parse_qsl(query))
code = query['code']

#returned_state = raw_input('state:   ')

#assert returned_state == state, 'St5ate parameters do no match! Bailing out.'

data = {'code': code,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'}

creds = (lnkdn.client_id, lnkdn.client_secret)
#b = lnkdn.get_access_token(decoder=json.loads,data = data)


s = lnkdn.get_auth_session(data=data, decoder=json.loads,auth = creds)


##sess = OAuth2Session(*creds, access_token=b)
##tkn = sess.request(site + token_url,"POST")
##r = s.get(r'/~')
##print r.content



pref = 'https://api.linkedin.com/'
#r = s.get(pref + r'v1/people/~/connections?format=json&oauth2_access_token=' +str(s.access_token) , data={'x-li-format': 'json'}, bearer_auth=False)

r = requests.get(pref + r'v1/people/~/connections?format=json&oauth2_access_token=' +str(s.access_token) )


def get_dict_from_json(raw_string):
    dict_frm_json = json.loads(raw_string)
    return dict_frm_json
    
