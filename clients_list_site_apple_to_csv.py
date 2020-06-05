#!/usr/bin/env python
"""
clients_list_site_apple.py - List Apple clients on a site

This script will list all Apple clients on a specific site and dunp them
to a CSV file.

To use this script, you must set the following environmental variables that
are used by the script:

    MIST_TOKEN - A valid API token created for access to your organization
    MIST_SITE_ID - A valid side ID

This is required to prevent the requirement for hard coding them in to
script of an accompanying config file. It should be created as an env_var
that is private to your environment, not a global var on the machine that
you are working on.
"""

import os
import sys
import csv
from datetime import datetime
import argparse

from modules.core.logger import ScriptLogger
from modules.core.mist_verbs import MistVerbs
from modules.core.stopwatch import StopWatch
from modules.core.get_vars import GetVars
from modules.core.banner import header, footer

# create parser args
parse_descr = "Script to dump all Apple device details for a specific site (env var MIST_SITE_ID) in to a CSV report (date-stamped reports dumped in the 'reports' folder) \n"
parser = argparse.ArgumentParser(description=parse_descr)
#parser.add_argument('site_id')

args = parser.parse_args()

# set up logging
logger = ScriptLogger('mist-api')
logger.info("Starting script...")

# supply required token
vars_obj = GetVars()
vars_found = vars_obj.find_vars()
api_token = vars_found.get('token')
site_id = vars_found.get('site_id')

# define URLs
base_url = "https://api.mist.com"
apple_clients_url = "{}/api/v1/sites/{}/clients/sessions/search?client_manufacture=Apple".format(base_url, site_id)

# define CSV file name
report_file = 'reports/Apple_Devices_Site_' + str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '.csv'

def main():

    timer = StopWatch()
    timer.start()

    if not api_token:
        print("You must define a valid API key using the MIST_TOKEN environmental variable name to use this script...exiting.")
        sys.exit()
    
    if not site_id:
        print("You must define a valid site ID using the MIST_SITE_ID environmental variable name to use this script...exiting.")
        sys.exit()
    
    header()

    logger.info("Getting tokens.")
    
    verb_obj = MistVerbs(api_token)
    apple_devices = verb_obj.mist_read(apple_clients_url)

    dict_data = []
    mac_list = []
    
    for device in apple_devices['results']:
        dict = {
            "client_manufacture": device['client_manufacture'],
            "client_family": device['client_family'],
            "client_model": device['client_model'],
            "client_os": device['client_os'],
            "band": device['band'],
            "mac": device['mac'],
        }


        # add to device dict, but do not add duplicates
        if not device['mac'] in mac_list:
            dict_data.append(dict)
            mac_list.append(device['mac'])

    logger.info("Dumping CSV device report file: {}.".format(report_file))

    column_headers = ["client_manufacture", "client_family", "client_model", "client_os", "mac", "band"]

    try:
        with open(report_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=column_headers)
            writer.writeheader()

            for dict in dict_data:
                writer.writerow(dict)

    except IOError as err:
        logger.error("CSV I/O error: {}".format(err))

    logger.info("Script complete.")
    timer.stop()

    footer()
    
if __name__ == "__main__":
    main()


