#!/usr/bin/env python
"""
token_create.py - Tidy up unused API tokens

This script will remove all API tokens for your account, except
the token being used to run this script. This mitigates potential
security issues with old tokens being left lying around in your
Mist account.

To use this script, you must set the following environmental variables that
are used by the script:

    MIST_TOKEN - A valid API token created for access to your organization

This is required to prevent the requirement for hard coding them in to
script of an accompanying config file. It should be created as an env_var
that is private to your environment, not a global var on the machine that
you are working on.
"""

import os
import sys
from pprint import pprint

from modules.core.logger import ScriptLogger
from modules.core.mist_verbs import MistVerbs
from modules.core.stopwatch import StopWatch

# set up logging
logger = ScriptLogger('mist_api')

# define required credential & org id
api_token = os.environ.get('MIST_TOKEN')

# define URLs
base_url = "https://api.mist.com"
tokens_url = "{}/api/v1/self/apitokens".format(base_url)

def main():

    timer = StopWatch()
    timer.start()

    if not api_token:
        print("You must define a valid API key using the MIST_TOKEN environmental variable name to use this script...exiting.")
        sys.exit()
           
    # Create tokens  
    verb_obj = MistVerbs(api_token, False)
    token = verb_obj.mist_create(tokens_url)
    print("Token created:")
    pprint(token)
  
    logger.info("Script complete.")

    timer.stop()

if __name__ == "__main__":
    main()


