FROM python:3.7.8-buster

MAINTAINER Mike Moran, mike.moran@amd.com

ENV APP_PATH=/opt/my_python

COPY * $APP_PATH/.
WORKDIR $APP_PATH
RUN apt-get update \
 && apt-get -y install python python-pip \
 && python -m pip install --upgrade pip \
 && pip install -r requirements.txt

ENV APP_PORT=4230
EXPOSE $APP_PORT
# TODO add: ENV JENKINS_HOST_URL=http://your.own.ip.address:port/
#CMD ["gunicorn", "--bind", "127.0.0.1:$APP_PORT", "fastapi_main:APP"]
CMD "gunicorn --bind 127.0.0.1:$APP_PORT fastapi_main:APP"

