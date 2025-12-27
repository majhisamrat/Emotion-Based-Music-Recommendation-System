import cv2
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

face_model = load_model("models/image_emotion_cnn_final.h5")

EMOTIONS = ['angry', 'happy', 'sad', 'neutral', 'fear']

def predict_face_emotion(uploaded_file):
    """
    uploaded_file: Streamlit UploadedFile (camera_input)
    """

   
    image = Image.open(uploaded_file).convert("L")  # grayscale

    # Convert to numpy
    img = np.array(image)

    # Resize & normalize
    img = cv2.resize(img, (48, 48))
    img = img / 255.0
    img = img.reshape(1, 48, 48, 1)

    # Predict
    preds = face_model.predict(img)
    emotion = EMOTIONS[np.argmax(preds)]

    return emotion
