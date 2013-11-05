from rauth import OAuth2Service, OAuth2Session
from hashlib import sha1
import requests

#import for parsing the url and getting the state and getting the code
#for authentication
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
config.read(os.path.join(os.path.abspath('..'),
                                         'my_site_key_details.ini'))


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

'''
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

r = requests.get(pref + r'v1/people/~/connections?format=json&oauth2_access_token=' +
                     str(s.access_token) )
'''

def get_dict_from_json(raw_string):
    dict_frm_json = json.loads(raw_string)
    return dict_frm_json

class Oauth2_Py_Linkedin(OAuth2Service):

    
    '''
    These are static variable which are common to all Oatuh2_Py_Linkedin objects
    They contain information about the urls
    '''
    service_name = 'py_lnkdn_service'
    authorize_url =  r'https://www.linkedin.com/uas/oauth2/authorization'
    access_token_url = r'https://www.linkedin.com/uas/oauth2/accessToken'
    base_url = r'https://api.linkedin.com/'

    def __init__(self, *credential_file_path, **auth_credential_dict):
        ''' create a oauth2_service_object for handling the initial authentication
            process with the linkedin server
            example authentication using the auth_credential_dict
            lnkdn = Oauth2_Py_Linkedin(
                      client_id = 'api_key',
                      client_secret = 'sec_key',
                      redirect_uri = 'http://www.website.com'
                      )
            Otherwise, the user can just pass a config file (.ini format) and mention
            the section to look for. An example ini file:

             > cat my_site_key_details.ini 
            [website1_details]
            client_id = api_key1
            client_secret = api_key2
            redirect_uri = http://www.website1.com
            
            [website2_details]
            client_id = api_key1
            client_secret = api_key2
            redirect_uri = http://www.website2.com

            To call just use lnkdn = Oauth2_Py_Linkedin(
                        '/path/to/my_site_key_details.ini', 'website2_details')
            
        '''

        if credential_file_path:
            file_path = credential_file_path[0]
            credentials_section = credential_file_path[1]

            from ConfigParser import RawConfigParser
            config_parser = RawConfigParser()
            config_parser.read(os.path.join(file_path))
            self.api_key = config_parser.get(credentials_section,'client_id')
            self.sec_key = config_parser.get(credentials_section,
                                                             'client_secret')
            self.redirect_url =\
                        config_parser.get(credentials_section,'redirect_url')
  
        elif auth_credential_dict:
            self.api_key = auth_credential_dict['client_id']
            self.sec_key = auth_credential_dict['client_secret']
            self.redirect_url = auth_credential_dict['redirect_url']
            

        return super(Oauth2_Py_Linkedin, self).__init__(
            name = self.service_name,
            client_id = self.api_key,
            client_secret = self.sec_key,
            authorize_url = self.authorize_url,
            access_token_url = self.access_token_url,
            base_url = self.base_url
           )
                    
                
class Py_LinkedIn(object):
    def __init__(self, oauth2_service_object, req_format = 'json'):
        ''' creates Py_linkedin object which sets the authentication
            parameter used for calling the REST call to linkedin
        '''
        self.service = oauth2_service_object
    
