FROM python:3.7.8-buster

MAINTAINER Mike Moran, mike.moran@amd.com

ENV APP_PATH=/opt

COPY my_python $APP_PATH/.
WORKDIR $APP_PATH
RUN apt-get update \
 && apt-get -y install python python-pip \
 && python -m pip install --upgrade pip \
 && pip install -r my_python/requirements.txt

EXPOSE 4230
#ENV JENKINS_HOST_URL=http://145.40.81.55:8080
CMD ["gunicorn", "--bind", "127.0.0.1:4230", "my_python.fastapi_main:APP"]
