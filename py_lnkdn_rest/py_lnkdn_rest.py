from rauth import OAuth2Service, OAuth2Session
from hashlib import sha1
from random import random
import requests
import re
import json
import os


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
                        config_parser.get(credentials_section,'redirect_uri')
  
        elif auth_credential_dict:
            self.api_key = auth_credential_dict['client_id']
            self.sec_key = auth_credential_dict['client_secret']
            self.redirect_url = auth_credential_dict['redirect_url']

        #generate state for cross checking with the linkedin website
        self.state = sha1(str(random())).hexdigest()
            

        return super(Oauth2_Py_Linkedin, self).__init__(
            name = self.service_name,
            client_id = self.api_key,
            client_secret = self.sec_key,
            authorize_url = self.authorize_url,
            access_token_url = self.access_token_url,
            base_url = self.base_url
           )

    def get_authorize_url(self, scope = 'r_network'):
        params = dict(response_type = 'code',
                      state = self.state,
                      redirect_uri = self.redirect_url,
                      scope = scope)
        return super(Oauth2_Py_Linkedin, self).get_authorize_url(**params)

    def generate_access_token(self):
        auth_url = self.get_authorize_url()
        print('Visit this url in your browser: \n' + auth_url  + '\n')

        redirected_url_lnkdn = raw_input('and copy the redirection url')

        self.access_token = self.get_lnkdn_access_token(redirected_url_lnkdn)
        return self.access_token

    def get_lnkdn_access_token(self, redirected_url):
        #import for parsing the url and getting the state and getting
        #the code for authentication
        try:
            from urlparse import parse_qsl
        except ImportError:
            from cgi import parse_qsl
        query = redirected_url.split('?',1)[-1]
        query = dict(parse_qsl(query))

        #make sure the state returned is the same as the one sent
        assert(self.state == query['state'])

        code = query['code']
        data = {'code': code,
            'redirect_uri': self.redirect_url,
                'grant_type': 'authorization_code'}
        creds = (self.client_id, self.client_secret)
        sess = self.get_auth_session(data = data, decoder=json.loads,
                                    auth = creds)
        return sess.access_token
        
                
class Py_LinkedIn(object):
    def __init__(self, oauth2_service_object, req_format = 'json'):
        ''' creates Py_linkedin object which sets the authentication
            parameter used for calling the REST call to linkedin
        '''
        self.token = oauth2_service_object.access_token
        self.req_format = req_format
        self.prefix_url = oauth2_service_object.base_url

    def get_all_contacts_for_user(self):
        requested_url = self.prefix_url + r'v1/people/~/connections?format=' \
                    + self.req_format \
                        + r'&oauth2_access_token='\
                        + self.token
        r = requests.get(requested_url)
        return r
    
