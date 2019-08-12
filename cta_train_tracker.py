#!/usr/bin/python

from cta_tracker import CtaTracker
import requests
import json

class CtaTrainTracker(CtaTracker):
    """Class to interact with cta train tracker api"""

    base_url = "http://lapi.transitchicago.com/api/1.0/"
    __key = ''

    def __init__(self, key):
        self.__key = key

    def get_arrivals(self, mapid=None, stpid=None, max=None, rt=None):
        app = "ttarrivals.aspx"

        # Check required parameters
        if not mapid and not stpid:
            raise ValueError("Either mapid or stpid has to be provided")
        if mapid and stpid:
            raise ValueError("Both mapid and stpid cannot be provided")

        # Initialize the object
        payload = {
                'outputType': 'JSON',
                'key': self.__key
                }
        if stpid:
            payload['stpid'] = stpid
        else:
            payload['mapid'] = mapid

        # Add extra options
        if max:
            payload['max'] = max
        if rt:
            payload['rt'] = rt

        return self.call_api(app, payload)

    def follow(self, runnumber):
        app = "ttfollow.aspx"

        # Initialized the object
        payload = {
                'outputType': 'JSON',
                'key': self.__key
                }
        payload['runnumber'] = runnumber

        # Make the request and error check
        return self.call_api(app, payload)

    def call_api(self, app, payload):
        response = requests.get(self.base_url + app, params=payload)
        if not response.ok:
            raise Exception("Error while accessing the api")
        json_response = json.loads(response.content)
        if 'errCd' in json_response['ctatt'] and int(json_response['ctatt']['errCd']) != 0:
            raise Exception("Error while accessing the api: {}".format(json_response['ctatt']['errNm']))
        return json_response
