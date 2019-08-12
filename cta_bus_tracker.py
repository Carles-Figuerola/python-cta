#!/usr/bin/python

from cta_tracker import CtaTracker
import requests
import json

class CtaBusTracker(CtaTracker):
    """Class to interact with cta bus tracker api"""

    base_url = "http://www.ctabustracker.com/bustime/api/v2/"
    __key = ''

    def __init__(self, key):
        self.__key = key

    def get_arrivals(self, stpid=None, max=None, rt=None):
        app = "getpredictions"

        # Check required parameters
        if not stpid:
            raise ValueError("stpid has to be specified to get arrivals")

        # Initialize the object
        payload = {
                'format': 'json',
                'key': self.__key
                }
        if stpid:
            payload['stpid'] = stpid

        # Add extra options
        if max:
            payload['max'] = max
        if rt:
            payload['rt'] = rt

        return self.call_api(app, payload)

    def follow(self, runnumber):
        app = "ttfollow.espx"

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
        if 'error' in json_response['bustime-response']:
            print json_response['bustime-response']
            raise Exception("Error while accessing the api: {}".format(str(json_response['bustime-response']['error'])))
        return json_response
