# encoding=UTF-8
"""
"""
import enum

import data
import jenkins
import os
import re
import table
from table.a import ATable
from table.href import HrefTable
from table.text import TextTable
from jenkins import JobTable
from urllib import parse

SPLIT_CHAR = '~'


class DashboardTable(table.Table):

    @classmethod
    def from_job_table(cls, jt, split_char=SPLIT_CHAR):
        t = table.Table()
        jenkins_url = os.environ.get('JENKINS_HOST_URL')
        for job_name in jt.row_gen():
            quote_job_name = parse.quote(job_name)
            last_build_number = jt.last_build_number(job_name)
            href_link = f'{jenkins_url}/job/{quote_job_name}/{last_build_number}/console'
            ss = job_name.split(split_char)
            if len(ss) < 3:
                continue
            host = ss[0]
            guest = ss[1]
            host_guest = f'{host}{split_char}{guest}'
            component = ss[2]
            pass_fail = 'pass' if jt.passed(job_name) else 'FAIL'
            status_href = f'{pass_fail}{split_char}{href_link}'
            t.set_val(host_guest, component, status_href)

        # end for job_name
        return t
