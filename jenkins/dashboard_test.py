# encoding=UTF-8
"""
"""
import data
import jenkins
from table.text import TextTable
from jenkins import JobTable
from jenkins.dashboard import DashboardTable


JENKINS_ROOT_HTML = 'JENKINS_ROOT.htm'


def test_dashboard_table():
    text = data.text_from(JENKINS_ROOT_HTML)
    jt = JobTable.from_text(text)
    dt = DashboardTable.from_job_table(jt)
    print()
    print(dt.pf('dt'))
