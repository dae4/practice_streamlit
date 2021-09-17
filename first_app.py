import streamlit as st
import json
import os
from io import BytesIO
import numpy as np
from PIL import Image
import torch
from torchvision import transforms
from models.experimental import attempt_load
from utils.general import non_max_suppression,scale_coords,check_img_size
from utils.plots import colors, plot_one_box

st.title("han""'""s first app")

with open("class.json", "r") as f:
    class_idx = json.load(f)
    idx2label = [class_idx[str(k)][1] for k in range(len(class_idx))]

weights=os.listdir("weights/")

option = st.selectbox(
    'Select weights',
    weights)

def load_model(weights):
    device ='cpu'
    imgsz=640
    model = attempt_load(weights, map_location=device)
    stride = int(model.stride.max())
    imgsz = check_img_size(imgsz, s=stride) 
    return model


model = load_model(option)
model.eval()

uploaded_file = st.file_uploader("Choose a Image")

conf_thres = st.slider("conf")
iou_thres = st.slider("iou")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    image = Image.open(BytesIO(bytes_data)).convert("RGB")
    
    
    img = transforms.ToTensor()(image)
    img = img.unsqueeze(dim=0)
    det = model(img)[0]
    lb=class_idx
    det = non_max_suppression(det, conf_thres, iou_thres, classes=None, agnostic_nms=False, max_det=1000)
    gn = torch.tensor(img.shape)[[1, 0, 1, 0]]
    imc = img.copy()
    s=''
    if len(det):
        det[:4] = scale_coords(img.shape[2:], det[:, :4], img.shape).round()
        for c in det[:, -1].unique():
                n = (det[:, -1] == c).sum()  # detections per class
                s += f"{n} {lb[int(c)]}{'s' * (n > 1)}, "  # add to string
        for *xyxy, conf, cls in reversed(det):
            c = int(cls)  # integer class
            label =  f'{lb[c]} {conf:.2f}'
            plot_one_box(xyxy, img, label=label, color=colors(c, True), line_thickness=3)

    img_for_plot = np.array(img)
    st.image(img_for_plot, use_column_width=True)
