import io

from starlette.responses import Response

from fastapi import FastAPI, File, Form
from fastapi.responses import FileResponse
import uvicorn
from openpose import estimation_process, video_process

app = FastAPI(
    title="Human-estimation based on OpenPose",
    description="""Obtain human—estimation maps of the image in input via OpenPose implemented in tensorflow.
                           Visit this URL at port 8501 for the streamlit interface.""",
    version="0.1.0",
)

# 单张图片展示
@app.post("/estimation")
def get_estimation_map(file: bytes = File(...)):
    """Get estimation maps from image file"""
    estimated_image = estimation_process(file)  # 输入openpose网络处理的到处理后的图片
    bytes_io = io.BytesIO()
    estimated_image.save(bytes_io, format="PNG")
    return Response(bytes_io.getvalue(), media_type="image/png")


# 俯卧撑
@app.post("/PushUp", response_class=FileResponse)
def main(file: bytes = File(...)):
    out_video = video_process(1, file)  # 使用response文件方式 video_process返回值为文件名
    return out_video


# 引体向上
@app.post("/PullUp", response_class=FileResponse)
def main(file: bytes = File(...)):
    out_video = video_process(2, file)  # 使用response文件方式 video_process返回值为文件名
    return out_video


# 仰卧起坐
@app.post("/SitUp", response_class=FileResponse)
def main(file: bytes = File(...)):
    out_video = video_process(3, file)  # 使用response文件方式 video_process返回值为文件名
    return out_video

# 自动运行uvicorn
if __name__ == '__main__':
    uvicorn.run(app='server:app', host="127.0.0.1", port=8000, reload=True, debug=True)

