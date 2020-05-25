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
org_id = os.environ.get('MIST_ORG')

# define URLs
base_url = "https://api.mist.com"
login_url = "{}/api/v1/login".format(base_url)
tokens_url = "{}/api/v1/self/apitokens".format(base_url)

sites_url = "{}/api/v1/orgs/{}/sites".format(base_url, org_id)
org_wlans_url = "{}/api/v1/orgs/{}/wlans".format(base_url, org_id)
inventory_url = "{}/api/v1/orgs/{}/inventory".format(base_url, org_id)

email = ''
password = ''

# define common headers
headers = {
        'Content-Type': 'application/json',
        #'Authorization': 'Token {}'.format(api_token)
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

    email = ''
    password = ''

    start_time = time.time()

    if not api_token:
        email = input("Enter Mist email address: ")
        password = getpass()
           
    if not org_id:
        print("You must define a valid organization ID using the MIST_ORG environmental variable name to use this script...exiting.")
        sys.exit()
    
    with requests.Session() as session:    

        if not api_token:
            # Login with email/pwd
            logger.info("Logging in.")
            data = { "email": email, "password": password}
            login = mist_post(login_url, session, data)

            pprint(login)

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


