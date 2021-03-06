import streamlit as st

import cv2
import mediapipe as mp
from io import BytesIO
import numpy as np

st.title("Utils")



option = st.sidebar.selectbox('Please select mode!',
                       ['hands', 'face', 'pose'])

st.sidebar.write("Please select source")
left_column, right_column = st.sidebar.columns(2)
image = left_column.button('image')
cam = right_column.button('webcam')


detection_conf = st.sidebar.slider("confidence",min_value = 0.0,max_value = 1.0,step=0.1)
mp_drawing = mp.solutions.drawing_utils


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=detection_conf)

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=detection_conf, min_tracking_confidence=0.5)
drawing_spec = mp_drawing.DrawingSpec(color=(0,128,128), thickness=1, circle_radius=1)



mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    min_detection_confidence=detection_conf, min_tracking_confidence=0.5)
# For static images:
if image:
    uploaded_file = st.file_uploader("Choose a Image")
    try:
        bytes_data = uploaded_file.getvalue()
        encoded_img = np.frombuffer(bytes_data, dtype = np.uint8)
        image = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if option=='hands':
            results = hands.process(image)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        drawing_spec,
                        drawing_spec)
                    
        elif option=='face':
            results = face_mesh.process(image)
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=drawing_spec)
        elif option=='pose':
            st.error("please use webcam")
        
        st.image(image,use_column_width=True)
        
    except:
        st.write("Not Found")
# For Webcam:
elif cam:
    FRAME_WINDOW = st.image([])
    cam = cv2.VideoCapture(0)
    stop=st.button('stop')
    while True:
        ret, frame = cam.read()
        if frame is None:
            st.error("Please Check Webcam")
        else:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if option=='hands':
                results = hands.process(image)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            image,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            drawing_spec,
                            drawing_spec)

            elif option=='face':
                results = face_mesh.process(image)
                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=drawing_spec)

            elif option == 'pose':
                results = pose.process(image)
                image.flags.writeable = True
                mp_drawing.draw_landmarks(
                    image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            FRAME_WINDOW.image(image)
            if stop:
                cam=False
else:
    st.subheader("please Select Mode")