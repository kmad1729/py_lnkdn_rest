import ConfigParser

def read_config_details(config_file_path):
     config = ConfigParser.RawConfigParser()
     config.read(config_file_path)
     return config
     

def get_access_token (client_id, client_key):
    pass
