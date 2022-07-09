FROM tiangolo/uvicorn-gunicorn:python3.7

RUN mkdir /fastapi

COPY requirements.txt /fastapi

WORKDIR /fastapi

COPY . /fastapi

RUN apt-get update
RUN apt-get install sudo
RUN sudo apt-get install g++
RUN sudo apt-get install gcc
RUN sudo apt-get install libpcre3 libpcre3-dev


RUN cd /fastapi/swig-4.0.2 \ 
    && ./configure --prefix=/fastapi/swig \ 
    && make \
    && make install 
   

ENV PATH=/fastapi/swig/bin:$PATH 
    

RUN pip install numpy

RUN cd /fastapi/tf_pose/pafprocess \
    && swig -python -c++ pafprocess.i && python setup.py build_ext --inplace \
    && python setup.py install

   
RUN pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html
RUN sudo apt install libgl1-mesa-glx -y

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
