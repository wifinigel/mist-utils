#!/usr/bin/env python
"""
aps_org_dump_to_csv.py - Dump all your Org APs to a CSV file

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
import csv
from datetime import datetime
import argparse

from modules.core.logger import ScriptLogger
from modules.core.mist_verbs import MistVerbs
from modules.core.stopwatch import StopWatch
from modules.core.get_vars import GetVars
from modules.core.banner import header, footer

# create parser args
parse_descr = "Script to dump all APs of an org in to a CSV report (date-stamped reports dumped in the 'reports' folder) \n"
parser = argparse.ArgumentParser(description=parse_descr)

args = parser.parse_args()

# set up logging
logger = ScriptLogger('mist_api')

# supply required token
vars_obj = GetVars()
vars_found = vars_obj.find_vars()
api_token = vars_found.get('token')
org_id = vars_found.get('org_id')

# define URLs
base_url = "https://api.mist.com"
sites_url = "{}/api/v1/orgs/{}/sites".format(base_url, org_id)
inventory_url = "{}/api/v1/orgs/{}/inventory".format(base_url, org_id)

# define CSV file name
report_file = 'reports/AP_Inventory_Org_' + str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '.csv'

def main():

    timer = StopWatch()
    timer.start()

    if not api_token:
        print("You must define a valid API token using the MIST_TOKEN environmental variable name to use this script...exiting.")
        sys.exit()
    
    if not org_id:
        print("You must define a valid organization ID using the MIST_ORG environmental variable name to use this script...exiting.")
        sys.exit()
    
    header()

    # Get my org sites
    logger.info("Getting sites info.")
    verb_obj = MistVerbs(api_token)
    sites = verb_obj.mist_read(sites_url)

    # Create sites dict based on response
    sites_lookup = {}

    for site in sites:

        site_id = site['id']
        site_name = site['name']

        sites_lookup[site_id] = site_name
    
    # Get my device inventory
    logger.info("Getting device inventory info.")
    devices = verb_obj.mist_read(inventory_url)

    dict_data = []
    
    for device in devices:
        dict = {
            "device_name": device['name'],
            "device_model": device['model'],
            "device_type": device['type'],
            "device_serial": device['serial'],
            "site_name": sites_lookup[device['site_id']],
        }

        if device['type'] == 'ap':
            dict_data.append(dict)

    logger.info("Dumping CSV device report file: {}.".format(report_file))

    column_headers = ["device_name", "device_model", "device_type", "device_serial", "site_name"]

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


