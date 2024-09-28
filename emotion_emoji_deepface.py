import cv2
from deepface import DeepFace
import streamlit as st

# Stores
happy_mood = cv2.imread(r"C:\Users\vedan\Downloads\archive\train\happy")
sad_mood = cv2.imread(r"C:\Users\vedan\Downloads\archive\train\sad")
surprise_mood = cv2.imread(r"C:\Users\vedan\Downloads\archive\train\surprise")
neutral_mood = cv2.imread(r"C:\Users\vedan\Downloads\archive\train\neutral")
angry_mood = cv2.imread(r"C:\Users\vedan\Downloads\archive\train\angry")
fear_mood = cv2.imread(r"C:\Users\vedan\Downloads\archive\train\fear")
disgust_mood = cv2.imread(r"C:\Users\vedan\Downloads\archive\train\disgust")


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

        # Analyze the mood
        try:
            analysis = DeepFace.analyze(
                photo_path, actions=["emotion"], enforce_detection=False
            )
            dominant_emotion = analysis[0]["dominant_emotion"]
            print(analysis)
            mood_image = emotion_to_image.get(dominant_emotion)

            # Display the corresponding mood image
            if mood_image is not None:
                cv2.imshow("Mood Image", mood_image)
                cv2.waitKey(3000)  # Display for 3 seconds
                cv2.destroyWindow("Mood Image")

            print(f"Dominant Emotion: {dominant_emotion}")
        except Exception as e:
            print(f"Error in emotion detection: {e}")

st.title("Mood Generation")

cap.release()
cv2.destroyAllWindows()
