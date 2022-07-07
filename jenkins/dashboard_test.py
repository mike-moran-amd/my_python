# encoding=UTF-8
"""
"""
import data
from jenkins import JobTable
from jenkins.dashboard import DashboardTable
JENKINS_ROOT_HTML = 'JENKINS_ROOT.htm'



def test_dashboard_table(mocker):
    mocker.patch('jenkins.get_host_url', return_value='http://127.0.0.1:8080')
    mocker.patch('jenkins.get_response_text', return_value=data.text_from(JENKINS_ROOT_HTML))
    jt = JobTable.from_jenkins_host()
    dt = DashboardTable.from_job_table(jt)
    print()
    print(dt.pf('HOST~GUEST'))
    pass
