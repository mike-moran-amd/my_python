# encoding=UTF-8
"""
"""
import data
from jenkins import JobTable
from jenkins.dashboard import DashboardTable
JENKINS_ROOT_HTML = 'JENKINS_ROOT.htm'


def test_dashboard_table():
    text = data.text_from(JENKINS_ROOT_HTML)
    jt = JobTable.from_text(text)
    # jt = JobTable.from_jenkins_host()
    dt = DashboardTable.from_job_table(jt)
    print()
    print(dt.pf('dt'))
