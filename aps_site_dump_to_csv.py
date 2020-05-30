#!/usr/bin/env python
"""
aps_org_dump_to_csv.py <site_id> - Dump all APs on a specific site to a CSV file

To use this script, you must set the following environmental variables that
are used by the script:

    MIST_TOKEN - A valid API token created for access to your organization

These are required to prevent the requirement for hard coding them in to
script of an accompanying config file. These variables should be created
as env vars that are private to your environment, not global vars on the 
machine that you are working on.
"""

import os
import sys
import csv
from datetime import datetime
import argparse

from modules.core.logger import ScriptLogger
from modules.core.mist_verbs import MistVerbs
from modules.core.stopwatch import StopWatch
from modules.core.banner import header, footer

# create parser args
parse_descr = "Script to dump all APs for a specific site in to a CSV report (date-stamped reports dumped in the 'reports' folder) \n"
parser = argparse.ArgumentParser(description=parse_descr)
parser.add_argument('site_id')


args = parser.parse_args()

# set up logging
logger = ScriptLogger('mist_api')

# define required credential & org id
api_token = os.environ.get('MIST_TOKEN')

# get the site_id passed on the command line
site_id = args.site_id

# define URLs
base_url = "https://api.mist.com"
site_inventory_url = "{}/api/v1/sites/{}/devices".format(base_url, site_id)

# define CSV file name
report_file = 'reports/AP_Inventory_Site_' + str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '.csv'

def main():

    timer = StopWatch()
    timer.start()

    if not api_token:
        print("You must define a valid API token using the MIST_TOKEN environmental variable name to use this script...exiting.")
        sys.exit()
       
    header()

    # Get my org sites
    logger.info("Getting sites info.")
    verb_obj = MistVerbs(api_token)
    devices_on_site = verb_obj.mist_read(site_inventory_url)

    dict_data = []
    
    for device in devices_on_site:
        dict = {
            "device_name": device['name'],
            "device_model": device['model'],
            "device_type": device['type'],
            "device_serial": device['serial'],
        }

        if device['type'] == 'ap':
            dict_data.append(dict)

    logger.info("Dumping CSV device report file: {}.".format(report_file))

    column_headers = ["device_name", "device_model", "device_type", "device_serial"]

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


