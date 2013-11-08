import unittest, os
from py_lnkdn_rest import *

class Authentication_Tests(unittest.TestCase):
    auth_credential_dict = dict(client_id = 'test_client_id',
                                client_secret = 'test_secret',
                                redirect_url = 'www.foo.com')
    path_to_write = os.path.join(os.path.expanduser('~'),
                                     'py_lnkdn_auth_test_file.ini')


    def setUp(self):
        '''creating an ini file with different credentials'''
        dev_credentials = '''[website1_details]
client_id = api_key1
client_secret = api_secret1
redirect_uri = http://www.website1.com

[website2_details]
client_id = api_key2
client_secret = api_secret2
redirect_uri = http://www.website2.com
        '''
        with open(self.path_to_write, 'w') as f:
            f.write(dev_credentials)
    
    def test_initFromCredentialDict(self):
        test_auth_object = Oauth2_Py_Linkedin(**self.auth_credential_dict)
        assert(self.auth_credential_dict['client_id'] ==
                   test_auth_object.client_id)
        assert(test_auth_object.client_secret ==
                   self.auth_credential_dict['client_secret'])
        assert(test_auth_object.redirect_url ==
                   self.auth_credential_dict['redirect_url'])

    def test_initFromIniFile(self):
        test_auth_object1 = Oauth2_Py_Linkedin(self.path_to_write,
                                              'website1_details')
        test_auth_object2 = Oauth2_Py_Linkedin(self.path_to_write,
                                              'website2_details')
        assert(test_auth_object1.client_id == 'api_key1')
        assert(test_auth_object2.client_secret == 'api_secret2')
        assert(test_auth_object1.client_id == 'api_key1')
        assert(test_auth_object2.client_secret == 'api_secret2')
        assert(test_auth_object1.redirect_url ==
                           'http://www.website1.com')
        assert(test_auth_object2.redirect_url ==
                           'http://www.website2.com')

    def test_stateGeneration(self):
        test_auth_object = Oauth2_Py_Linkedin(**self.auth_credential_dict)
        assert(len(test_auth_object.state) == 40)
        import string
        assert(all(c in string.hexdigits for c in test_auth_object.state))

    def test_authorize_url(self):
        test_auth_object = Oauth2_Py_Linkedin(**self.auth_credential_dict)
        test_url = test_auth_object.get_authorize_url()
        assert(test_auth_object.authorize_url in test_url)
        assert(r'state=' + test_auth_object.state in test_url)
        assert(r'redirect_uri=' + test_auth_object.redirect_url in test_url)
        assert(r'client_id=' + test_auth_object.client_id in test_url)

    def test_getAccessToken(self):
        test_auth_object = Oauth2_Py_Linkedin(**self.auth_credential_dict)
        test_redirected_url = 'http://www.foo.com/?' \
            'code=AQSl-uTllUkqaslmahLg0jPb8CYsFnkQ6btgA1VXLw2rI4h3V5zJaoiNxpHASHftu-'\
            'a_SibpH5Dg7VWQ7PZnklNjHv7yXtOjNWlkM1CrAUhRrjgBk_4' \
            '&state=' +  test_auth_object.state

    def tearDown(self):
        os.remove(self.path_to_write)
        
        
    
if __name__ == '__main__':
    unittest.main(exit = False)
