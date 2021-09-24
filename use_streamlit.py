import streamlit as st

import cv2
import mediapipe as mp
from io import BytesIO
import numpy as np

st.title("Utils")

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5, min_tracking_confidence=0.5)
drawing_spec = mp_drawing.DrawingSpec(color=(0,128,128), thickness=1, circle_radius=1)


# For static images:
hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5)
# # For webcam input:
# hands = mp_hands.Hands(
#     min_detection_confidence=0.5, min_tracking_confidence=0.5)



option = st.sidebar.selectbox('Please select mode!',
                       ['hands', 'face', 'pose'])

st.sidebar.write("Please select source")
left_column, right_column = st.sidebar.columns(2)
image = left_column.button('image')
cam = right_column.button('webcam')

st.write('You selected:', option)
uploaded_file = st.file_uploader("Choose a Image")
if image:
    try:
        bytes_data = uploaded_file.getvalue()
        encoded_img = np.frombuffer(bytes_data, dtype = np.uint8)
        image = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if option=='hands':
            results = hands.process(image)
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    drawing_spec,
                    drawing_spec)
                    
        elif option=='face':
            results = face_mesh.process(image)
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=drawing_spec)
        st.image(image,use_column_width=True)
    except:
        st.write("Not Found")

else:
    st.subheader("please push button")