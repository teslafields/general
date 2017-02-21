import requests
from requests.auth import HTTPBasicAuth


class Api(object):

    def __init__(self):
        self.URL = "http://179.223.178.122:5000/"
        self.AUTH = HTTPBasicAuth('maickelc@gmail.com', 'rhkg38yw4w')

    def post(self, url, data):
        post_data = data # json.dumps(data)
        url = self.URL+url
        return requests.post(url, json=post_data, auth=self.AUTH)

    def get(self, url):
        return requests.get('{0}{1}'.format(self.URL, url), auth=self.AUTH)
