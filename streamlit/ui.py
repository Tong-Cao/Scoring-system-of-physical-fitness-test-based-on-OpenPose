import io

import requests
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder

import streamlit as st
import numpy as np


# interact with FastAPI endpoint
backend = "http://fastapi:8000/"


# 传递图片至指定url
def process(input_data, server_url: str):
    m = MultipartEncoder(fields={"file": ("filename", input_data, "image/jpeg")})  # 上传文件

    r = requests.post(
        server_url, data=m, headers={"Content-Type": m.content_type}, timeout=8000
    )  # 传递image至后端 返回r为处理后的图片

    return r


# construct UI layout
st.title("Human-estimation based on OpenPose")

# 单张图片估计及展示     sidebar为展示在侧边栏
input_image = st.sidebar.file_uploader("insert image and get the result picture")  # image upload widget

if st.sidebar.button("Get estimation map"):

    col1, col2 = st.columns(2)

    if input_image:
        estimate = process(input_image, backend+'estimation')
        original_image = Image.open(input_image).convert("RGB")  # 原图片
        estimated_image = Image.open(io.BytesIO(estimate.content)).convert("RGB")
        col1.header("Original")  # 标题
        col1.image(original_image, use_column_width=True)

        col2.header("Estimated")  # 标题
        col2.image(estimated_image, use_column_width=True)

    else:
        # handle case with no image
        st.write("Insert an image!")

# 视频处理
f = st.sidebar.file_uploader("Upload your video and get the result")  # 上传本地视频   数据为二进制存在内存中 可通过f.getvalue读取

project = st.sidebar.selectbox(
     'chose the project',
     ('PushUp', 'PullUp', 'SitUp'))

if st.sidebar.button("Start"):
    estimate = process(f, backend + project)  # 返回response需要用response.content读取其中内容
    estimate = io.BytesIO(estimate.content)  # 往内存中写入estimate.content数据
    st.video(estimate, format="video/mp4", start_time=0)  # 展示视频
