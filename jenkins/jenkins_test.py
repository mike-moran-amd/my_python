# encoding=UTF-8
"""
"""
import data
import jenkins
import os
import re
import table
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
    pass


def test_test():
    text = data.text_from(JENKINS_ROOT_HTML)
    pattern = '<a '
    t = table.Table()
    t_row = 0
    for a_tag in re.findall('<a (.+?)</a>', text):
        t_row += 1
        unquote_a_tag = parse.unquote(a_tag)
        t.set_val(t_row, 'unquote_a_tag', unquote_a_tag)
        non_attrib = unquote_a_tag
        for attrib, value in re.findall('(.+?)="(.+?)"', unquote_a_tag):
            t.set_val(t_row, attrib, value)
            rep = f'{attrib}="{value}"'
            non_attrib = non_attrib.replace(rep, '')
        t.set_val(t_row, 'non_attrib', non_attrib)
        href = t.get_val(t_row, 'href')
        if href and href.startswith('job/'):
            ss = href.split('/')
            t.set_val(t_row, 'job_name', ss[1])
            t.set_val(t_row, 'job_item', ss[2])

    scrape_table = table.Table()
    for t_row in t.row_gen():
        job_name = t.get_val(t_row, 'job_name')
        if job_name and job_name.lower()[-5:] == 'guest':
            job_item = t.get_val(t_row, 'job_item')
            if job_item in ['lastSuccessfulBuild', 'lastFailedBuild']:
                value = t.get_val(t_row, 'non_attrib')
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
