FROM python:3.7.8-buster

MAINTAINER Mike Moran, mike.moran@amd.com

ENV APP_PATH=/opt
ENV APP_PORT=8000

COPY requirements.txt $APP_PATH/.
RUN apt-get update \
 && apt-get -y install python python-pip \
 && python -m pip install --upgrade pip \
 && pip install -r $APP_PATH/requirements.txt

COPY my_python $APP_PATH/.
WORKDIR $APP_PATH
EXPOSE $APP_PORT
CMD ["gunicorn", "--bind", "127.0.0.1:$APP_PORT", "fastapi_main:APP"]

