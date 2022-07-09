# Scoring-system-of-physical-fitness-test-based-on-OpenPose
## **在linux系统中opencv无法找到合适编码方式，暂无法实现项目整体功能！**

本项目使用**OpenPose**检测人体关键节点并对体测项目进行自动计数，通过**streamlit**以及**fastapi**来搭建前后端用来展示**OpenPose**处理结果。 

运行前先安装好**docker**以及**compose**

### 运行步骤：

1. 请在`./fastapi/models/graph/cmu`中运行`.sh`文件进行**cmu**模型下载，并在`./fastapi/openpose.py`中24行以及58行代码中更换为cmu模型
2. 运行终端打开文件位置输入`docker compose build`在本地创建镜像  
3. 镜像创建完成后输入`docker compose up`创建容器并运行  

***
- 直接下载压缩文件，在创建镜像过程中可能会报错，建议采用本地仓库拉取方式  

- 若在**windows**环境下无法使用**docker**，可根据`安装过程.txt`中步骤手动进行环境配置  

- 在**fastapi**文件夹中的**openpose.py**中可以更换模型，其中**cmu**模型识别效果最好

- 在**window**系统中**opencv**可以使用**avc1**的编码方式，但无法在**linux**环境中无法使用，可能需要安装**ffempg**，暂未解决

  
