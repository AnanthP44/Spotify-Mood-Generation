import cv2
from deepface import DeepFace
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st
import numpy as np

# Title and subheading with specific colors
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

# User input
mood = st.text_input("", key="moodInput1")

# Spotify API setup
sp_client_id = "b7b076b85c7d4cc19664df7cef6481ad"
sp_client_secret = "87963b1a078843e8872072adc5719ea2"
client_credentials_manager = SpotifyClientCredentials(
    client_id=sp_client_id, client_secret=sp_client_secret
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Emotion to song search query mapping
emotion_to_query = {
    "happy": "happy",
    "sad": "sad",
    "angry": "angry",
    "surprise": "surprise",
    "disgust": "disgust",
    "fear": "fear",
    "neutral": "neutral",
}

# Initialize webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Press SPACE to capture a photo, or 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Display the webcam feed
    cv2.imshow("Webcam", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break
    elif key == 32:  # Spacebar key
        # Capture the image
        photo_path = "captured_photo.jpg"
        cv2.imwrite(photo_path, frame)
        print(f"Photo captured and saved as {photo_path}")

img_file_buffer = st.camera_input("Capture a photo to detect your mood")

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
    # Analyze the mood

try:
    analysis = DeepFace.analyze(
        photo_path, actions=["emotion"], enforce_detection=False
    )
    dominant_emotion = analysis[0]["dominant_emotion"]
    st.text(f"Dominant Emotion: {dominant_emotion}")

    # Fetch modern songs from Spotify based on the dominant emotion
    if dominant_emotion in emotion_to_query:
        query = emotion_to_query[dominant_emotion]
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


except Exception as e:
    print(f"Error in emotion detection: {e}")

cap.release()
cv2.destroyAllWindows()
