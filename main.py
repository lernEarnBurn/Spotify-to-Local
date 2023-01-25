from dotenv import load_dotenv
import os
import requests
import base64
import json


load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

def get_token():
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    token_url = "https://accounts.spotify.com/api/token"
    data = {"grant_type": "client_credentials"}
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    response = requests.post(token_url, data=data, headers=headers)
    json_result = json.loads(response.content)
    token = json_result["access_token"]
    return token



def get_auth_header(token):
    return {"Authorization" : "Bearer " + token}


def spotifyRequest(url, header):
    response = requests.get(url, headers=header)
    return json.loads(response.content)

def structuredData(playlists):
    names = []
    urls = []
    for playlist in playlists:
        names.append(playlist["name"])
        urls.append(playlist["tracks"]["href"])
    return [names, urls]


def playlistExists(num, names):
    if (num) <= len(names):
        return True
    else:
        return False


playlists_url = "https://api.spotify.com/v1/users/gnmk2ryw9oqx4r6uz9wmtjixl/playlists" 
token = get_token()
header = get_auth_header(token)

playlists = spotifyRequest(playlists_url, header)["items"]

names = structuredData(playlists)[0]
urls = structuredData(playlists)[1]


for name in names:
    print(f"{names.index(name) + 1}. {name}")

choice = int(input('\nSelect a number corresponding to the playlist that you want: '))

if playlistExists(choice, names):
    url = urls[choice - 1]
    tracks = spotifyRequest(url, header)["items"]
    for track in tracks:
        song = track["track"]["name"] + ' by ' + track["track"]["artists"][0]["name"]
        print(song)
        #youtubeDownload func to download each song and print u some confirmation
else:
    print("Playlist doesn't exist")



