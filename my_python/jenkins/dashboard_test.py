# encoding=UTF-8
"""
"""
from my_python import data
from my_python.jenkins import JobTable
from my_python.jenkins.dashboard import DashboardTable
JENKINS_ROOT_HTML = 'JENKINS_ROOT.htm'


def test_dashboard_table(mocker):
    mocker.patch('my_python.jenkins.get_host_url', return_value='http://127.0.0.1:8080')
    mocker.patch('my_python.jenkins.get_response_text', return_value=data.text_from(JENKINS_ROOT_HTML))
    jt = JobTable.from_jenkins_host()
    dt = DashboardTable.from_job_table(jt)
    print()
    print(dt.pf('HOST~GUEST'))
    pass
