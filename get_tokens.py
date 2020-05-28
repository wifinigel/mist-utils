"""
get_tokens.py - List my API tokens

This script will list all API tokens currently created for your
Mist login.

To use this script, you must set the following environmental variables that
are used by the script:

    MIST_TOKEN - A valid API token created for access to your organization

This is required to prevent the requirement for hard coding them in to
script of an accompanying config file. It should be created as an env_var
that is private to your environment, not a global var on the machine that
you are working on.
"""

import os
import json
import requests
import logging
import sys
import time
from pprint import pprint
from getpass import getpass

# set up logging to console
logger = logging.getLogger('mist_api')
logger.setLevel(logging.INFO)

# create console handler & set level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to console handler
console_handler.setFormatter(formatter)

# add console handler to logger
logger.addHandler(console_handler)

logger.info("Starting script...")

# define required credential & org id
api_token = os.environ.get('MIST_TOKEN')

# define URLs
base_url = "https://api.mist.com"
tokens_url = "{}/api/v1/self/apitokens".format(base_url)

# define common headers
headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Token {}'.format(api_token)
}

def mist_get(url, session):
    """function to return data structure from Mist API using a requests session

    Arguments:
        url {str} -- [Full URL of API call]
        session {requests session obj} -- [session object created using requests]

    Raises:
        Exception: [Generic failure message if http request fails]

    Returns:
        [data structure] -- [Data structure returned - varies with API call]
    """

    response = session.get(url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        raise Exception('Query to Mist API failed: {} (check token or req URL format?)'.format(response.status_code))

def mist_post(url, session, data):
    """function to post data structure to Mist API using a requests session

    Arguments:
        url {str} -- [Full URL of API call]
        session {requests session obj} -- [session object created using requests]
        data {dict} -- [data dict structure]

    Raises:
        Exception: [Generic failure message if http post fails]

    Returns:
        [boolean] -- [True = post OK, False = bad post]
    """

    response = session.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        raise Exception('Query to Mist API failed: {} (check token or req URL format?)'.format(response.status_code))

def main():

    start_time = time.time()

    if not api_token:
        print("You must define a valid API key using the MIST_TOKEN environmental variable name to use this script...exiting.")
        sys.exit()
             
    with requests.Session() as session:    

        # List tokens
        logger.info("Getting tokens.")
        tokens = mist_get(tokens_url, session)
        pprint(tokens)
    
    logger.info("Script complete.")
    run_time = time.time() - start_time
    print("")
    print("** Time to run: %s sec" % round(run_time, 2))

if __name__ == "__main__":
    main()


