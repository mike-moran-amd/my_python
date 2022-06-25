# encoding=UTF-8
"""
"""
import os
import requests


def get_response_text(url):
    requests_response = requests.get(url)
    if requests_response.status_code != 200:
        raise RuntimeError(f'INVALID RETURN CODE: {requests_response.status_code}')
    return requests_response.text


class JenkinsHost:
    def __init__(self, url=os.environ.get('JENKINS_HOST_URL', None)):
        if not url:
            raise RuntimeError('pass in host url or set environment variable "JENKINS_HOST_URL" to point to host root')
        self.__url = url

    def get_text(self, local_url):
        url = self.__url + '/' + local_url
        return get_response_text(url)
