# encoding=UTF-8
"""

"""
import requests
import urllib.parse


def get_response(url):
    raw_response = requests.get(url)
    if raw_response.status_code != 200:
        raise RuntimeError(f'INVALID RETURN CODE: {raw_response.status_code}')
    # response = urllib.parse.unquote(raw_response.text)
    response = raw_response.text
    return response