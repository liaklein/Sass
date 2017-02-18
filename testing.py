from __future__ import print_function
import requests
import json
#from requests_oauthlib import OAuth1
url = "https://api.kairos.com/enroll"
headers = {
    'Content-Type': 'application/json',
    'app_id': 'f62afb61',
    'app_key': '6c53b4533d32d3773539951326ea7118'
}
json = {
    "image": " http://media.kairos.com/kairos-elizabeth.jpg ",
    "subject_id": "Elizabeth",
    "gallery_name": "MyGallery"
}
def enroll_player():
    pass

def get_players_from_image():
    pass

r = requests.post(url, json=json, headers=headers)
print(r.status_code, r.reason)
print(r.text[:500])
