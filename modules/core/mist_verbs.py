import requests
import json
import sys
from http.client import responses

from modules.core.logger import ScriptLogger

class MistVerbs(object):

    """
    A class to peform read, create, update & delete operations via the
    Mist API.

    Arguments:
        token {mandatory str} -- [API token string]
        read_only {optional boolean} -- [True (default) allows only read operations]
    """

    def __init__(self, token, read_only=True):

        self.token = token
        self.read_only = read_only
        self.session = requests.Session()
        self.logger = ScriptLogger('MistVerbs')
        self.response_headers = ''

        # define common headers
        self.headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Token {}'.format(token)
        }
    
    def mist_read(self, url):
        """function to get data structure from Mist API using a requests session. This
        provides a read operation via the Mist API to retrieve data.

        Arguments:
            url {str} -- [Full URL of API call]
            session {requests session obj} -- [session object created using requests]

        Raises:
            Exception: [Generic failure message if http request fails]

        Returns:
            [data structure] -- [Data structure returned - varies with API call]
        """

        response = self.session.get(url, headers=self.headers)
        self.response_headers = response.headers

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            print('** Query to Mist API failed: {} (check token or req URL format?) - Bad URL: {}'.format(responses[response.status_code], url))
            sys.exit()

    def mist_create(self, url, data=''):
        """function to post data structure to Mist API using a requests session. This
        has the effect of creating new objects via the Mist API

        Arguments:
            url {str} -- [Full URL of API call]
            session {requests session obj} -- [session object created using requests]
            data {dict} -- [data dict structure]

        Raises:
            Exception: [Generic failure message if http post fails]

        Returns:
            [boolean] -- [True = post OK, False = bad post]
        """

        # check if object is read only
        if self.read_only:
            self.logger.error('Object is read only...exiting')
            print('** Object is read-only. If you intend to perform write/update/delete operations, set read_only=False when creating object')
            sys.exit()

        response = None

        if data:
            response = self.session.post(url, headers=self.headers, data=json.dumps(data))
            self.response_headers = response.headers
        else:
            response = self.session.post(url, headers=self.headers)
            self.response_headers = response.headers

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            print('** Query to Mist API failed: {} (check token or req URL format?) - bad URL: {}'.format(responses[response.status_code], url))
            sys.exit()

    def mist_update(self, url, data):
        """function to put data structure to Mist API using a requests session. This
        hs the effect of doing an update of data sent to the Mist API

        Arguments:
            url {str} -- [Full URL of API call]
            session {requests session obj} -- [session object created using requests]
            data {dict} -- [data dict structure]

        Raises:
            Exception: [Generic failure message if http post fails]

        Returns:
            [boolean] -- [True = post OK, False = bad post]
        """

        # check if object is read only
        if self.read_only:
            self.logger.error('Object is read only...exiting')
            print('Object is read-only. If you intend to perform write/update/delete operations, set read_only=False when creating object')
            sys.exit()

        response = self.session.put(url, headers=self.headers, data=json.dumps(data))
        self.response_headers = response.headers

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            print('** Query to Mist API failed: {} (check token or req URL format?)'.format(responses[response.status_code]))
            sys.exit()

    def mist_delete(self, url):
        """function to delete object from Mist API using a requests session

        Arguments:
            url {str} -- [Full URL of API call inc ID of object to be deleted]
            session {requests session obj} -- [session object created using requests]

        Raises:
            Exception: [Generic failure message if http delete fails]

        Returns:
            [boolean] -- [True = delete OK, False = bad delete]
        """

        # check if object is read only
        if self.read_only:
            self.logger.error('Object is read only...exiting')
            raise Exception('Object is read-only. If you intend to perform write/update/delete operations, set read_only=False when creating object')
        
        response = self.session.delete(url, headers=self.headers)
        self.response_headers = response.headers

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            print('** Query to Mist API failed: {} (check token or req URL format?) - Bad URL: {}'.format(responses[response.status_code], url))
            sys.exit()
