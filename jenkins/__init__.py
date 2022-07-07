# encoding=UTF-8
"""
"""
import os
import requests
import table
from table.href import HrefTable

JENKINS_HOST_URL = 'JENKINS_HOST_URL'  # the environment variable that has URL to Jenkins server


def get_host_url():
    # this should be set in Dockerfile e.g. ENV JENKINS_HOST_URL=http://IP.ADD.RE.SS:PORT/
    host_url = os.environ.get(JENKINS_HOST_URL)
    return host_url


def get_response_text(url):
    requests_response = requests.get(url)
    if requests_response.status_code != 200:
        raise RuntimeError(f'INVALID RETURN CODE: {requests_response.status_code}')
    return requests_response.text


class JenkinsHost:
    def __init__(self, url=None):
        url = url or get_host_url()
        if not url:
            raise RuntimeError(f'Set environment variable "{JENKINS_HOST_URL}", for example "http://127.0.0.1:8080/"')
        self.__url = url

    def get_text(self, local_url):
        url = self.__url + '/' + local_url
        text = get_response_text(url)
        return text


class JobTable(table.Table):

    @classmethod
    def from_jenkins_host(cls, jh=None):
        jh = jh or JenkinsHost()
        text = jh.get_text('')
        jt = JobTable.from_text(text)
        return jt

    @classmethod
    def from_text(cls, text, href_starts_with='job/'):
        ht = HrefTable.from_text(text, href_starts_with=href_starts_with)
        jt = cls()
        for ht_row in ht.row_gen():
            href = ht.get_href(ht_row)
            ss = href.split('/')
            if len(ss) < 3:
                continue
            job_name = ss[1]
            job_item = ss[2]
            job_value = ht.get_href_value(ht_row)
            jt.set_val(job_name, job_item, job_value)
        return jt

    def last_failed_build(self, job_name, col_label='lastFailedBuild'):
        val = self.get_val(job_name, col_label)
        if not val:
            return 0
        if val.startswith('>#'):
            val = val[2:]
        return int(val)

    def last_successful_build(self, job_name, col_label='lastSuccessfulBuild'):
        val = self.get_val(job_name, col_label)
        if not val:
            return 0
        if val.startswith('>#'):
            val = val[2:]
        return int(val)

    def passed(self, job_name):
        f = self.last_failed_build(job_name)
        p = self.last_successful_build(job_name)
        if not f:
            return True
        return p > f

    def last_build_number(self, job_name):
        if self.passed(job_name):
            return self.last_successful_build(job_name)
        return self.last_failed_build(job_name)
