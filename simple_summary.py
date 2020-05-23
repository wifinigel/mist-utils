"""
simple_summary.py - Create a simple summary of Mist organisaiton information

To use this script, you must set the following environmental variables that
are used by the script:

    MIST_TOKEN - A valid API token created for access to your organization
    MIST_ORG - The organization ID of your org

These are required to prevent the requirement for hard coding them in to
script of an accompanying config file. These variables should be created
as env vars that are private to your environment, not global vars on the 
machine that you are working on.
"""

import os
import json
import requests
import logging
import sys
import time

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
sites_url = "{}/api/v1/orgs/{}/sites".format(base_url, org_id)
org_wlans_url = "{}/api/v1/orgs/{}/wlans".format(base_url, org_id)
inventory_url = "{}/api/v1/orgs/{}/inventory".format(base_url, org_id)

# define common headers
headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Token {}'.format(api_token)
}

def mist_request(url, session):
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

def main():

    start_time = time.time()

    if not api_token:
        print("You must define a valid API token using the MIST_TOKEN environmental variable name to use this script...exiting.")
        sys.exit()
    
    if not org_id:
        print("You must define a valid organization ID using the MIST_ORG environmental variable name to use this script...exiting.")
        sys.exit()
    
    with requests.Session() as session:    

        # Get my org sites
        logger.info("Getting sites info.")
        sites = mist_request(sites_url, session)

        print("\nOrganization sites: \n")

        for site in sites:
            print("\t" + site['name'])

        print("\n")

        # Get my org wlans
        logger.info("Getting WLANs info.")
        wlans = mist_request(org_wlans_url, session)
        
        print("\nOrganization WLANs: \n")

        for wlan in wlans:
            print("\t" + wlan['ssid'])
        
        print("\n")
        
        # Get device inventory
        logger.info("Getting device inventory info.")
        devices = mist_request(inventory_url, session)
        
        print("\nOrganization Inventory: \n")

        for device in devices:
            print("\t{}\t{}\t{}".format(device['name'], device['model'], device['type']))

        print("\n")
    
    logger.info("Script complete.")
    run_time = time.time() - start_time
    print("")
    print("** Time to run: %s sec" % round(run_time, 2))

if __name__ == "__main__":
    main()


