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

# set up logging
logger = ScriptLogger('mist_api')

# get requried vars (token & org IDs)
vars_obj = GetVars()
vars_found = vars_obj.find_vars()
api_token = vars_found.get('token')

# create parser args
parse_descr = "Script to list summary of an organisation. (Requires MIST_TOKEN env var, org_id may be passed on CLI or via MIST_ORG_ID env var) \n"
parser = argparse.ArgumentParser(description=parse_descr)
parser.add_argument('org_id', nargs='?', default=vars_found.get('org_id'))

args = parser.parse_args()

# get the site_id passed on the command line
org_id = args.org_id

# define URLs
base_url = "https://api.mist.com"
org_stats_url = "{}/api/v1/orgs/{}/stats".format(base_url, org_id)

def main():

    timer = StopWatch()
    timer.start()

    if not api_token:
        print("You must define a valid API token using the MIST_TOKEN environment variable name to use this script...exiting.")
        sys.exit()
    
    if not org_id:
        print("You must define a valid organization ID using the MIST_ORG environment variable name to use this script...exiting.")
        sys.exit()
    
    header()

    # Get my org sites
    logger.info("Getting org info.")
    verb_obj = MistVerbs(api_token)
    org_info = verb_obj.mist_read(org_stats_url)

    """
    Data structure returned:

            {
            "num_inventory": 12,
            "num_devices": 10,
            "name": "Sam MSP Customer 5",
            "orggroup_ids": [],
            "allow_mist": false,
            "num_devices_connected": 8,
            "num_devices_disconnected": 2,
            "num_sites": 1,
            "num_clients": 80,
            "id": "448a3934-df89-11e5-8898-1258369c38a9",
            "sle": [
                {"path": "coverage", "user_minutes": {"total": 20, "ok": 19}},
                {"path": "capacity", "user_minutes": {"total": 20, "ok": 18}},
                {"path": "time-to-connect", "user_minutes": {"total": 20, "ok": 19}}
            ]
        }
    """

    print(f"""
        Org name = {org_info['name']}
        Claimed Devices: {org_info['num_inventory']}
        Devices in use: {org_info['num_devices']}
        Connected Devices: {org_info['num_devices_connected']}
        Disconnected Devices: {org_info['num_devices_disconnected']}
        Number Sites: {org_info['num_sites']}
    """)
    
    logger.info("Script complete.")

    timer.stop()

    footer()

if __name__ == "__main__":
    main()


