import streamlit as st

import cv2
import mediapipe as mp
from io import BytesIO
import numpy as np

st.title("hands")

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles

# For static images:
hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5)
# # For webcam input:
# hands = mp_hands.Hands(
#     min_detection_confidence=0.5, min_tracking_confidence=0.5)


uploaded_file = st.file_uploader("Choose a Image")
try:
    bytes_data = uploaded_file.getvalue()
    encoded_img = np.frombuffer(bytes_data, dtype = np.uint8)
    image = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
    image.flags.writeable = False
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
    st.image(image,use_column_width=True)
except:
    None