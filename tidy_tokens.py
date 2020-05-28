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

def mist_delete(url, session):
    """function to delete object from Mist API using a requests session

    Arguments:
        url {str} -- [Full URL of API call inc ID of object to be deleted]
        session {requests session obj} -- [session object created using requests]

    Raises:
        Exception: [Generic failure message if http delete fails]

    Returns:
        [boolean] -- [True = delete OK, False = bad delete]
    """

    response = session.delete(url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        raise Exception('Query to Mist API failed: {} (check token or req URL format?)'.format(response.status_code))

def main():

    start_time = time.time()

    if not api_token:
        print("You must define a valid API key using the MIST_TOKEN environmental variable name to use this script...exiting.")
        sys.exit()
           
    if not org_id:
        print("You must define a valid organization ID using the MIST_ORG environmental variable name to use this script...exiting.")
        sys.exit()
    
    with requests.Session() as session:    

        # List tokens
        logger.info("Getting tokens.")
        tokens = mist_get(tokens_url, session)
        pprint(tokens)

        # Verify ID of token we are using
        api_token_short = "{}...{}".format(api_token[0:4], api_token[-4:])
        our_token_id = None

        for token in tokens:
            if token['key'] == api_token_short:

                our_token_id = token['id']
        
        # Delete all tokens apart from our current token
        if len(tokens) > 1:
            logger.info("Deleting tokens.")

            for token in tokens:

                if token['id'] != our_token_id:
                    logger.info("Deleting tokens ID: {}".format(token['id']))
                    mist_delete("{}/{}".format(tokens_url, token['id']), session)
        else:
            logger.info("No tokens to tidy up.")
    
    logger.info("Script complete.")
    run_time = time.time() - start_time
    print("")
    print("** Time to run: %s sec" % round(run_time, 2))

if __name__ == "__main__":
    main()


