from __future__ import print_function
import requests
import json
#from requests_oauthlib import OAuth1
enroll_url = "https://api.kairos.com/enroll"
recognize_url = "https://api.kairos.com/recognize"
headers = {
    'Content-Type': 'application/json',
    'app_id': 'f62afb61',
    'app_key': '6c53b4533d32d3773539951326ea7118'
}


def enroll_player(image, player):
    #make your json
    json_info = {"gallery_name": "MyGallery"}
    json_info["image"] = image
    json_info["subject_id"] = player

    #send the request
    r = requests.post(enroll_url, json=json_info, headers=headers).json()
    #do something with r.status_code?
    if r.get('Errors'):
        response = {'result': {'error': r['Errors'][0]['Message']}}
    else:
        response = {'result': {'success': player}}
    return response


def get_players_from_image(image):
    #right now just assume that there is one face per image
    #we will hook up to mathematica later if we have time
    #make your json
    json_info = {"threshold": "0.63", "gallery_name": "MyGallery"}
    json_info["image"] = image

    #send the request
    r = requests.post(recognize_url, json=json_info, headers=headers)
    #error code 5051 if image not in gallery -- we think. will confirm later
    response = r.json()
    if "Errors" in response:
        print("there was an error")
        return ("ERROR",[])
    players = []
    for image in response.get('images', []):
        for candidate in image.get('candidates', []):
            players.append(candidate['subject_id'])
    return ("OK", players)


#print(r.status_code, r.reason)
#print(r.text[:500])
