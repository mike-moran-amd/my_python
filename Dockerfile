FROM python:3.9
WORKDIR /opt
COPY my_python/requirements.txt /opt/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /opt/requirements.txt
COPY my_python /opt/my_python
ENV JENKINS_HOST_URL="$JENKINS_HOST_URL"
CMD ["uvicorn", "my_python.fastapi_main:APP", "--host", "0.0.0.0", "--port", "4230"]
