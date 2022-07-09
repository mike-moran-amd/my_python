FROM python:3.7.8-buster

RUN apt-get update
RUN apt-get -y install python python-pip
RUN python -m pip install --upgrade pip

ENV APP_PATH=/opt
COPY my_python $APP_PATH/my_python
WORKDIR $APP_PATH
RUN pip install -r $APP_PATH/my_python/requirements.txt

EXPOSE 8000
ENV JENKINS_HOST_URL "$JENKINS_HOST_URL"
#CMD ["gunicorn", "--bind", "127.0.0.1:8000", "my_python.fastapi_main:APP"]
CMD ["uvicorn", "my_python.fastapi_main:APP", "--reload"]
