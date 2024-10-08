import cv2
import numpy as np
from deepface import DeepFace
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import base64
from requests import post
import json
import requests
import random

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&display=swap');

    body {
        font-family: 'Poppins', sans-serif;
    }

    /* Target the Streamlit main content container */
    .main {
        background: linear-gradient(270deg, #ff6f61, #d3e0ea, #00c9ff, #ff6f61);
        background-size: 800% 800%;
        animation: gradientAnimation 12s ease infinite;
        height: 100vh;
        width: 100vw;
        position: absolute;
        top: 0;
        left: 0;
    }

    @keyframes gradientAnimation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    h1 {
        font-family: 'Poppins', sans-serif;
        color: white;
        font-size: 3em;
        text-align: center;
        margin-bottom: 0;
    }

    h2 {
        font-family: 'Poppins', sans-serif;
        color: white;
        font-size: 2em;
        text-align: center;
        margin-top: 0;
    }

    </style>

    <div>
        <h1>Howdy!</h1>
        <h2>Welcome To Moodify</h2>
        <h2>Let Your Mood Drive Spotify</h2>
    </div>
    """,
    unsafe_allow_html=True,
)


# Spotify API setup
sp_client_id = "441dc6182d234d05993cd770118ca859"
sp_client_secret = "f9979f2b5e9648609b7fccf0c99314f8"
client_credentials_manager = SpotifyClientCredentials(
    client_id=sp_client_id, client_secret=sp_client_secret
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Stores the file chosen into the appropriate instance variables
happy_mood = cv2.imread(r"C:\Users\vedan\Downloads\archive\train\happy.jpg")
sad_mood = cv2.imread(r"C:\Users\vedan\Downloads\archive\train\sad.jpg")
surprise_mood = cv2.imread(r"C:\Users\vedan\Downloads\archive\train\surprise.jpg")
neutral_mood = cv2.imread(r"C:\Users\vedan\Downloads\archive\train\neutral.jpg")
angry_mood = cv2.imread(r"C:\Users\vedan\Downloads\archive\train\angry.jpg")
fear_mood = cv2.imread(r"C:\Users\vedan\Downloads\archive\train\fear.jpg")
disgust_mood = cv2.imread(r"C:\Users\vedan\Downloads\archive\train\disgust.jpg")

# Maps all the different emojis
emotion_to_image = {
    "happy": happy_mood,
    "sad": sad_mood,
    "surprise": surprise_mood,
    "neutral": neutral_mood,
    "angry": angry_mood,
    "fear": fear_mood,
    "disgust": disgust_mood,
}

img_file_buffer = st.camera_input("")


def get_token():
    auth_string = sp_client_id + ":" + sp_client_secret

    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    print("HEADERS", headers)
    result = post(url, headers=headers, data=data)
    print("aaa")
    print(result.content)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_reccomended_songs(
    limit=5,
    seed_artists="",
    seed_tracks="",
    market="US",
    seed_genres="hip-hop",
    target_danceability=0.95,
    target_energy=0.95,
    target_liveness=0.9,
    target_loudness=0.9,
    target_tempo=0.9,
):
    endpoint_url = "https://api.spotify.com/v1/recommendations?"
    all_recs = []

    query = f"{endpoint_url}limit={limit}&market={market}&seed_genres={seed_genres}&target_danceability={target_danceability}"
    query += f"&seed_artists={seed_artists}&target_energy={target_energy}"
    query += f"&seed_tracks={seed_tracks}"
    query += f"&target_liveness={target_liveness}&target_loudness={target_loudness}&target_tempo={target_tempo}"
    response = requests.get(
        query,
        headers={
            "Content-type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    json_response = response.json()

    if response:
        print("Recommended songs:")
        for i, j in enumerate(json_response["tracks"]):
            track_name = j["name"]
            artist_name = j["artists"][0]["name"]
            track_link = j["external_urls"]["spotify"]

            reccs = [track_name, artist_name, track_link]
            all_recs.append(reccs)

    return all_recs


def spotify_embed(embed_urls):
    spotify_html = '<div style="display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 20px;">'

    for url in embed_urls:
        spotify_html += f"""
        <div style="flex: 1 1 300px; max-width: 300px;">
        <iframe src="https://open.spotify.com/embed/track/{url.split('/')[-1]}" width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
        </div>
        """

    spotify_html += "</div>"

    st.components.v1.html(spotify_html, height=800)


if img_file_buffer is not None:
    image_bytes = img_file_buffer.getvalue()
    np_img = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    st.image(img, channels="BGR")

    photo_path = "captured_photo.jpg"
    cv2.imwrite(photo_path, img)

    analysis = DeepFace.analyze(
        photo_path, actions=["emotion"], enforce_detection=False
    )
    dominant_emotion = analysis[0]["dominant_emotion"]
    st.markdown(
        f"<p style='font-size: 20px; text-align: center;'>Detected Emotion: <b>{dominant_emotion}</b></p>",
        unsafe_allow_html=True,
    )

    if dominant_emotion in emotion_to_image:
        query = emotion_to_image[dominant_emotion]
        token = get_token()

        if dominant_emotion == "happy":
            rec = get_reccomended_songs(
                limit=8,
                seed_artists="",
                seed_tracks="",
                market="US",
                seed_genres="hip-hop",
                target_danceability=random.uniform(0.7, 1.0),
                target_energy=random.uniform(0.7, 1.0),
                target_liveness=random.uniform(0.7, 1.0),
                target_loudness=random.uniform(0.7, 1.0),
                target_tempo=random.uniform(0.7, 1.0),
            )

        elif dominant_emotion == "sad":
            rec = get_reccomended_songs(
                limit=8,
                seed_artists="",
                seed_tracks="",
                market="US",
                seed_genres="hip-hop",
                target_danceability=random.uniform(0.0, 0.3),
                target_energy=random.uniform(0.0, 0.3),
                target_liveness=random.uniform(0.0, 0.3),
                target_loudness=random.uniform(0.0, 0.3),
                target_tempo=random.uniform(0.0, 0.3),
            )

        else:
            rec = get_reccomended_songs(
                limit=8,
                seed_artists="",
                seed_tracks="",
                market="US",
                seed_genres="hip-hop",
                target_danceability=random.uniform(0.3, 0.6),
                target_energy=random.uniform(0.3, 0.6),
                target_liveness=random.uniform(0.3, 0.6),
                target_loudness=random.uniform(0.3, 0.6),
                target_tempo=random.uniform(0.3, 0.6),
            )

        spotify_links = [rec[2] for rec in rec]
        spotify_embed(spotify_links)
