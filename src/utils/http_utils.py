import json

import requests


class HttpUtils(object):
    @staticmethod
    def post_to_rest_endpoint(url, dictionary):
        """
        Method to POST a dict object (transformed in a JSON payload) to a REST endpoint
        :param url: str
        :param dictionary: the dictionary to send (dict)
        """

        headers = {'user-agent': 'virtual-app-consumer/dummy1', 'Content-Type': 'application/json'}
        r = requests.post(url=url, headers=headers, json=dictionary, timeout=2)

        print(r.status_code)
        print(r.json())

        return r.status_code, r.json()

    @staticmethod
    def get_from_rest_endpoint(url):
        headers = {'user-agent': 'virtual-app-consumer/dummy1', 'Content-Type': 'application/json'}
        r = requests.get(url=url, headers=headers, timeout=2)

        print(r.status_code)
        print(r.json()[0])

        return r.status_code, r.json()[0]
