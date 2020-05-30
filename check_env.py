#!/usr/bin/env python
"""
Script to check env for running Mist API calls. Useful to run
before trying to execute any scripts

Checks:

 1. DNS lookup
 2. Network connectivity: can we get to api.mist.com?
 3. Have we got an API key configured?
 4. Can we do a basic API call?

"""

import requests
import os
import socket
import json
from pprint import pprint
from http.client import responses

def check_env():

    banner_width = 70

    print("=" * banner_width)
    print("\nExecuting tests to check if our environment is \nsuitable to use Mist API:\n")

    print("1. Checking our DNS is good (looking up api.mist.com)...")

    try:
        socket.gethostbyname("api.mist.com")
        print("   Result: OK.\n")
    except:
        print("   Result: ** Fail ** (Check your DNS settings or network connectivity) .\n")


    base_url = "https://api.mist.com"
    print("2. Checking we can get to Mist API URL ({})...".format(base_url))

    session = requests.Session()

    try:
        session.get(base_url, timeout=1)
        print("   Result: OK.\n")
    except:
        print("   Result: ** Fail ** (Check network path available to {})\n".format(base_url))
  
    print("3. Checking we have an API key defined (via env var MIST_TOKEN)...")
    api_token = os.environ.get('MIST_TOKEN')

    if api_token:
        print("   Result: OK.\n")
    else:
        print("   Result: ** Fail **. (Please define the env var MIST_TOKEN)\n")
    
    print("4. Try a 'who am I' via the API...")
    
    headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Token {}'.format(api_token)
    }

    url = "https://api.mist.com//api/v1/self"

    try:
        response = session.get(url, headers=headers,  timeout=2)
        if response.status_code == 200:
            print("   Result: OK. (result below)\n")

            data = json.loads(response.content.decode('utf-8'))
            print("      Name: {} {}".format(data['first_name'], data['last_name']))
            print("      Email: {}".format(data['email']))
            #pprint(json.loads(response.content.decode('utf-8')))
        else:
            status_code = response.status_code
            print("   Result: ** Fail. ** (reponse received, but expected data was not received (code: {}, text: {}))".format(status_code, responses[status_code]))
            print("   (Maybe check that API token is available (via env var MIST_TOKEN and is valid)")
    except:
        print("   Result: ** Fail **. (Please check network connectivity)\n")

    
    print("\n  -- Tests complete --")
    print("=" * banner_width)

    



def main():
    check_env()


if __name__ == "__main__":
    main()