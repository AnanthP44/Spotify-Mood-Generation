import cv2
import numpy as np
from deepface import DeepFace
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

st.markdown(
    """
    <style>
    .title {
        color: white;
        font-size: 2em;
    }
    .subheading {
        color: white;
        font-size: 1.5em;
    }
    .stTextInput input {
        background-color: #1ED760; /* Background color of the input field */
        color: black; /* Text color inside the input field */
        font-weight: bold; /*Make the text bold*/
    }
    </style>
    <h1 class="title">Describe your emotion in one sentence?</h1>
    <p class="subheading">Enter your mood here:</p>
""",
    unsafe_allow_html=True,
)

mood = st.text_input("", key="moodInput1")

# Spotify API setup
sp_client_id = "b7b076b85c7d4cc19664df7cef6481ad"
sp_client_secret = "87963b1a078843e8872072adc5719ea2"
client_credentials_manager = SpotifyClientCredentials(
    client_id=sp_client_id, client_secret=sp_client_secret
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Stores
happy_mood = cv2.imread(r"C:\Users\vedan\Downloads\archive\train\happy.jpg")
sad_mood = cv2.imread(r"C:\Users\vedan\Downloads\archive\train\sad.jpg")
surprise_mood = cv2.imread(r"C:\Users\vedan\Downloads\archive\train\surprise.jpg")
neutral_mood = cv2.imread(r"C:\Users\vedan\Downloads\archive\train\neutral.jpg")
angry_mood = cv2.imread(r"C:\Users\vedan\Downloads\archive\train\angry.jpg")
fear_mood = cv2.imread(r"C:\Users\vedan\Downloads\archive\train\fear.jpg")
disgust_mood = cv2.imread(r"C:\Users\vedan\Downloads\archive\train\disgust.jpg")

# Emoji mapping
emotion_to_image = {
    "happy": happy_mood,
    "sad": sad_mood,
    "surprise": surprise_mood,
    "neutral": neutral_mood,
    "angry": angry_mood,
    "fear": fear_mood,
    "disgust": disgust_mood,
}

# Streamlit app title
st.title("Mood Detection with DeepFace")

# Streamlit's camera input to capture image
img_file_buffer = st.camera_input("Capture a photo to detect your mood")


dominant_emotion = ""
# Check if an image is captured
if img_file_buffer is not None:
    # Convert the image to an OpenCV format
    image_bytes = img_file_buffer.getvalue()
    np_img = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    # Display the captured image
    st.image(img, channels="BGR")

    # Save the image temporarily for DeepFace to analyze
    photo_path = "captured_photo.jpg"
    cv2.imwrite(photo_path, img)

    # Analyze the image with DeepFace to detect emotion

    analysis = DeepFace.analyze(
        photo_path, actions=["emotion"], enforce_detection=False
    )
    dominant_emotion = dominant_emotion + analysis[0]["dominant_emotion"]
    st.write(f"Detected Emotion: **{dominant_emotion}**")

    # Get the corresponding mood image
    mood_image = emotion_to_image.get(dominant_emotion)

    if dominant_emotion in emotion_to_image:
        query = emotion_to_image[dominant_emotion]
        # Search for tracks with modern criteria
        results = sp.search(
            q=f"{query} year:2020-2023", type="track", limit=10
        )  # Adjust the year range as needed
        songs = results["tracks"]["items"]
        st.text("Suggested Modern Songs:")

    for track in songs:
        track_name = track["name"]
        artists = ", ".join(artist["name"] for artist in track["artists"])
        st.text(f"- {track_name} by {artists}")


else:
    if mood in emotion_to_image:
        query = emotion_to_image[dominant_emotion]
        # Search for tracks with modern criteria
        results = sp.search(
            q=f"{query} year:2020-2023", type="track", limit=10
        )  # Adjust the year range as needed
        songs = results["tracks"]["items"]
        st.text("Suggested Modern Songs:")
