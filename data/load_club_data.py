import requests
import json

url = 'http://35.237.207.25/api/clubs/'
with open('clubs.json') as json_file:
    data = json.load(json_file)
    for club_json in data:
        print(requests.post(url, json=club_json))

