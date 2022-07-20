import sys
import matplotlib.pyplot as plt
import time
from tf_pose import common
import cv2
import numpy as np
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
import io
from PIL import Image

import global_var  # 调用全局变量


def estimation_process(binary_image):
    """、
    处理图片
    post请求从streamlit拉取下来的图片为二进制，首先用io.BytesIO(binary_image)转为PIL处理格式
    openpose处理的图片格式为numpy.ndarray  所以这里先将PIL转numpy输入openpose网络，再将输出转PIL进行下一步处理
    """
    input_image = Image.open(io.BytesIO(binary_image)).convert("RGB")  # io.BytesIO 为 bytes 转 PIL.Image.Image
    image = np.asarray(input_image)  # PIL.Image.Image转numpy.ndarray

    e = TfPoseEstimator(get_graph_path('mobilenet_thin'), target_size=(432, 368))  # 选择模型
    # estimate human poses from a single image !
    humans = e.inference(image, resize_to_default=0, upsample_size=4.0)
    # 输出人体关键点图片
    estimat_image = TfPoseEstimator.image_draw_humans(image, humans, imgcopy=False)

    estimat_image = Image.fromarray(np.uint8(estimat_image))  # numpy.ndarray 转 PIL.Image.Image

    return estimat_image


def video_process(model, binary_video):
    """
    视频处理
    model: 选择对应体测
    """
    import tempfile

    global_var._init()  # 初始化全局变量

    outfile_name = 'output.mp4'  # 输出结果文件名

    binary_video = io.BytesIO(binary_video)  # binary_video写入内存

    tfile = tempfile.NamedTemporaryFile(delete=False)  # 创建临时文件
    tfile.write(binary_video.read())  # 写入临时文件

    cap = cv2.VideoCapture(tfile.name)  # 打开文件
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 获取视频图像宽
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 获取视频图像高
    fps = cap.get(cv2.CAP_PROP_FPS)  # 读取图像显示帧率
    fourcc = int(cv2.VideoWriter_fourcc(*'vp90'))  # streamlit不支持显示MPV4编码方式 需要选择合适的编码方式
    #  linux环境下使用vp90编码或者直接将fourcc设置为0x39307076
    #  在windows下编码方式改为avc1
    out = cv2.VideoWriter(outfile_name, fourcc, fps, (width, height))  # 创建视频

    e = TfPoseEstimator(get_graph_path('cmu'), target_size=(432, 368))  # 选择模型  一定要放在处理视频帧循环外部 否则每次都要加载模型

    fps_time = 0

    if cap.isOpened() is False:  # 判断是否成功读入视频
        print("Error opening video stream or file")
    while cap.isOpened():
        ret_val, image = cap.read()  # 按帧读取视频   ret_val表示是否读取成功  image为每一帧图像

        if not ret_val:
            break
        # 画出人体姿态图
        humans = e.inference(image, resize_to_default=0, upsample_size=4.0)  # 对一帧图像进行处理
        image = TfPoseEstimator.draw_humans(model, image, humans, imgcopy=False)  # 画出人体姿态连接图

        '''显示计数结果以及帧数'''
        cv2.putText(image, "FPS: %f" % (1.0 / (time.time() - fps_time)), (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)  # 显示帧率
        wide = image.shape[1]  # 获得图像的宽 让count显示在图像正中央
        count = global_var.get_value('count')  # 从estimator.py中读count的全局变量
        cv2.putText(image, "COUNT: %d" % count, (wide // 2 - 100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255),
                    2)  # 计数显示  cv2.puttext（图片，添加的文字，左上角坐标，字体，字体大小，颜色，字体粗细）

        out.write(image)  # 写入每一帧图像ok
        fps_time = time.time()

        if cv2.waitKey(1) == 27:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return outfile_name


if __name__ == '__main__':
    # 选择模型 help='cmu / mobilenet_thin / mobilenet_v2_large / mobilenet_v2_small'
    e = TfPoseEstimator(get_graph_path('cmu'), target_size=(432, 368))

    # estimate human poses from a single image !
    image = common.read_imgfile('D:\openpose_test\image\p1.jpg', None, None)  # arg.image根据上面输入参数选择图片
    # type(image) = numpy.ndarray

    t = time.time()  # 时间戳
    humans = e.inference(image, resize_to_default=0, upsample_size=4.0)

    elapsed = time.time() - t

    # 输出人体关键点图片
    image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
    # 展示结果图
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # 转换RGB颜色
    plt.show()
