from dotenv import load_dotenv
import os
import base64
from requests import post
import json
import requests

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

print(client_id, client_secret)


def get_token():
    auth_string = client_id + ":" + client_secret

    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"

    }
    data = {"grant_type": "client_credentials"}
    print("HEADERS", headers)
    result = post(url, headers=headers, data=data)
    print('aaa')
    print(result.content)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

token = get_token()

print(token)



def get_reccomended_songs(limit=5, seed_artists='', seed_tracks='', market="US",
                            seed_genres="hip-hop", target_danceability=0.95, target_energy=0.95, target_liveness=0.9, target_loudness=0.9, target_tempo=0.9):  # reccomendations API
    endpoint_url = "https://api.spotify.com/v1/recommendations?"
    all_recs = []

    # API query plus some additions
    query = f'{endpoint_url}limit={limit}&market={market}&seed_genres={seed_genres}&target_danceability={target_danceability}'
    query += f'&seed_artists={seed_artists}&target_energy={target_energy}'
    query += f'&seed_tracks={seed_tracks}'
    query += f'&target_liveness={target_liveness}&target_loudness={target_loudness}&target_tempo={target_tempo}'
    response = requests.get(query, headers={
                            "Content-type": "application/json", "Authorization": f"Bearer {token}"})
    json_response = response.json()

    # print(json_response)
    if response:
        print("Reccomended songs")
        for i, j in enumerate(json_response['tracks']):
            track_name = j['name']
            artist_name = j['artists'][0]['name']
            link = j['artists'][0]['external_urls']['spotify']

            print(f"{i+1}) \"{j['name']}\" by {j['artists'][0]['name']}")
            reccs = [track_name, artist_name, link]
            all_recs.append(reccs)
        return all_recs


get_reccomended_songs(limit=5, seed_artists='', seed_tracks='', market="US",
                            seed_genres="hip-hop", target_danceability=0.1, target_energy=0.1, target_liveness=0.1, target_loudness=0.1, target_tempo=0.1)
