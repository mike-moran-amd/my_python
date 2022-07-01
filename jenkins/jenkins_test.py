# encoding=UTF-8
"""
"""
import data
import jenkins
from table.text import TextTable
from jenkins import JobTable


JENKINS_ROOT_HTML = 'JENKINS_ROOT.htm'


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


def test_job_table():
    jt = JobTable.from_text(data.text_from(JENKINS_ROOT_HTML))
    print()
    print(jt.pf('jt'))
