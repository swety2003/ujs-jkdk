FROM python:3.10
ADD ./server/ /code
WORKDIR /code
RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ \
    && apt update \
    && apt install -y nodejs
CMD python3 main.py