from __future__ import print_function
import requests
import json
#from requests_oauthlib import OAuth1

url = "https://api.kairos.com/recognize"
#auth = OAuth1('6c53b4533d32d3773539951326ea7118')

r = requests.post(url, json="request.json")

print(r.status_code, r.reason)
print(r.text[:500])
