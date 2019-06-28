#!/usr/bin/python

# This procedure enables the module to be a client of twitcher (from https://github.com/bird-house/twitcher/tree/dev-oauth) running on port 8000

from twitcher.client import TwitcherService
base_url = 'http://localhost:8000'
twitcher = TwitcherService(base_url, verify=False)

client = twitcher.add_client_app(username='demo', password='demo')
print(client)

token = twitcher.fetch_token(client_id=client['client_id'], client_secret=client['client_secret'])
print(token)

service = twitcher.register_service(access_token=token['access_token'], name="esgf_cwt_wps", url="http://localhost/wps")
print(service)

import requests
resp = requests.get("{}/ows/proxy/esgf_cwt_wps?service=WPS&request=GetCapabilities".format(base_url), verify=False)
print(resp.ok)
print(resp.text)

from twitcher.client import get_headers
headers = get_headers(token['access_token'])
print(headers)

resp = requests.get("{}/ows/proxy/esgf_cwt_wps?service=WPS&version=1.0.0&request=Execute&identifier=OPHIDIA.subset&datainputs=variable%3D%5B%7B%22uri%22%3A%22file.nc%22%2C%22id%22%3A%22tos%7Cv1%22%2C%22domain%22%3A%22d0%22%7D%5D%3Bdomain%3D%5B%7B%22lat%22%3A%7B%22start%22%3A-60%2C%22end%22%3A-15%2C%22crs%22%3A%22values%22%7D%2C%22lon%22%3A%7B%22start%22%3A42%2C%22end%22%3A113%2C%22crs%22%3A%22values%22%7D%2C%22id%22%3A%22d0%22%7D%5D%3Boperation%3D%5B%7B%22name%22%3A%22OPHIDIA.subset%22%2C%22input%22%3A%5B%22v1%22%5D%2C%22domain%22%3A%22d0%22%2C%22axes%22%3A%22time%22%7D%5D".format(base_url), headers=headers, verify=False)
print(resp.ok)
print(resp.text)

