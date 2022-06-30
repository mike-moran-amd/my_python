# encoding=UTF-8
"""
"""
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


JENKINS_ROOT_HTML = 'JENKINS_ROOT.htm'  # this name allows browser view with code highlighting 9-)


def xtest_get_from_server():
    # This will fetch the current text and replace the current data file.
    # Remove the "x" in front of the function name above to run this test now!
    jh = jenkins.JenkinsHost()
    text = jh.get_text('')
    data.save_text(JENKINS_ROOT_HTML, text)


def test_href_table_from_root():
    text = data.text_from(JENKINS_ROOT_HTML)
    tt = TextTable.from_string(text)
    print()
    print(tt.pf(''))
    assert len(list(tt.row_gen())) == 74
    pass


def test_test():
    text = data.text_from(JENKINS_ROOT_HTML)
    #t = ATable.from_text(text)
    href_table = HrefTable.from_text(text, href_starts_with='job/')
    scrape_table = table.Table()
    for href_table_row in href_table.row_gen():
        href = href_table.get_href(href_table_row)

        # TODO JenkinsJobTable...

        ss = href.split('/')
        assert ss[0] == 'job'
        job_name = parse.unquote(ss[1])
        job_item = ss[2]
        if job_name and job_name.lower().endswith('guest'):
            if job_item in ['lastSuccessfulBuild', 'lastFailedBuild']:
                value = href_table.get_href_value(href_table_row)
                if value.startswith('>#'):
                    value = value[2:]
                scrape_table.set_val(job_name, job_item, int(value))
    print()
    print(scrape_table.pf('scrape_table'))

    ht = table.Table()
    for job_name in scrape_table.row_gen():
        last_fail = scrape_table.get_val(job_name, 'lastFailedBuild', 0)
        last_pass = scrape_table.get_val(job_name, 'lastSuccessfulBuild', 0)
        url = os.environ.get('JENKINS_HOST_URL')
        if not last_fail or last_pass > last_fail:
            status = 'pass'
            href_link = f'{url}/job/{parse.quote(job_name)}/{last_pass}/console'
        else:
            status = 'FAIL'
            href_link = f'{url}/job/{parse.quote(job_name)}/{last_fail}/console'

        ss = job_name.split('host_')
        if len(ss) == 2:
            host = ss[0]
            guest = ss[1][:-5].strip()
        else:
            ss = job_name.split(' Host ')
            if len(ss) == 2:
                host = ss[0]
                guest = ss[1][:-5].strip()
            else:
                ss = job_name.split(' host ')
                if len(ss) == 2:
                    host = ss[0]
                    guest = ss[1][:-5].strip()
                else:
                    raise RuntimeError(job_name)

        ht.set_val(host, guest, f'{status}:{href_link}')

    print()
    print(ht.pf(''))
    pass


def test_job_table():
    jt = JobTable.from_text(data.text_from(JENKINS_ROOT_HTML))
    print()
    print(jt.pf('jt'))
