"""
This script will attempt to grab a number of globally useful variables from
various sourcesto be used in a script.

Many API calls may use one or more of the following variables to perform their
actions. This modules looks in various places to ensure these variables are
available to your script if required.

The following variables are searched for:

 1. token (an API token)
 2. org_id
 3. site_id
 4. device_id
 5. client_id

The folowing sources will be checked in the following order (last match wins):

 1. Environmental variables
 2. config.json file

Env-vars:

 MIST_TOKEN
 MIST_ORG_ID
 MIST_SITE_ID
 MIST_DEVICE_ID
 MIST_CLIENT_ID

config.json file format: (all fields are optional and others may be added as required)

{
    "token":     "xxxxxxxxxxxxxxxxxxxxxxxxxxx", 
    "org_id":    "xxxxxxxxxxxxxxxxxxxxxxxxx",
    "site_id":   "xxxxxxxxxxxxxxxxxxxxxxxxx",
    "device_id": "xxxxxxxxxxxxxxxxxxxxxxxxx",
    "client_id": "xxxxxxxxxxxxxxxxxxxxxxxxx",
}
"""

import os
import json
from modules.core.logger import ScriptLogger

class GetVars(object):

    """
    A class to find various variable values to be used with the Mist API

    Arguments:
        config_file {optional str} -- [filename thay contains json config (default = config.json)]
    """

    def __init__(self, config_file="config.json"):

        self.config_file = config_file

        self.token = ""
        self.org_id = ""
        self.site_id = ""
        self.device_id = ""
        self.client_id = ""

        self.env_vars = {
            'MIST_TOKEN': 'token', 
            'MIST_ORG_ID': 'org_id', 
            'MIST_SITE_ID': 'site_id', 
            'MIST_DEVICE_ID': 'device_id', 
            'MIST_CLIENT_ID': 'client_id'
        }

        self.found_vars = {}
   
    def find_vars(self):
        """
        Method search id a number of locations to find common varaibles needed
        to make a variety of API calls

        Arguments:
            None

        Returns:
            [Dict data structure] -- [Dictionary returned with all found variables]
        """

        # step through all env_vars and store any values that are set
        for env_var_name, key_name in self.env_vars.items():

            env_var_value = os.environ.get(env_var_name)

            if env_var_value:
                self.found_vars[key_name] = env_var_value

        # step through any values found in the json config file
        if os.path.isfile(self.config_file):

            # open file and read in to json format
            with open(self.config_file, 'r') as f:
                vars_data = json.load(f)
        
            for key_name, key_value in self.env_vars.items():

                if vars_data.get(key_value):

                    self.found_vars[key_value] = vars_data.get(key_value)

        # assign values to class values
        self.token = self.found_vars.get('token')
        self.org_id = self.found_vars.get('org_id')
        self.site_id = self.found_vars.get('site_id')
        self.device_id = self.found_vars.get('device_id')
        self.client_id = self.found_vars.get('client_id')
    
        return self.found_vars