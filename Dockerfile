FROM python:3.7.8-buster

MAINTAINER Mike Moran, mike.moran@amd.com

ENV APP_PATH=/opt
ENV APP_PORT=8000

COPY * $APP_PATH/.
WORKDIR $APP_PATH
RUN apt-get update \
 && apt-get -y install python python-pip \
 && python -m pip install --upgrade pip \
 && pip install -r requirements.txt

EXPOSE $APP_PORT
# TODO add: ENV JENKINS_HOST_URL=http://your.own.ip.address:port/
CMD ["gunicorn", "--bind", "127.0.0.1:$APP_PORT", "fastapi_main:APP"]

