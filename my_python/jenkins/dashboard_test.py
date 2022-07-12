# encoding=UTF-8
"""
"""
from my_python import data
from my_python.jenkins import JobTable
from my_python.jenkins.dashboard import DashboardTable, run_in_docker
JENKINS_ROOT_HTML = 'JENKINS_ROOT.htm'


def test_dashboard_table(mocker):
    mocker.patch('my_python.jenkins.get_host_url', return_value='http://127.0.0.1:8080')
    mocker.patch('my_python.jenkins.get_response_text', return_value=data.text_from(JENKINS_ROOT_HTML))
    jt = JobTable.from_jenkins_host()
    dt = DashboardTable.from_job_table(jt)
    print()
    print(dt.pf('HOST~GUEST'))
    pass


def test_run_in_docker(mocker):
    mocker.patch('my_python.lib.invoke_subprocess', return_value='')
    # TODO yield NL then OID_NL in side_effect (above)
    import os
    #result = run_in_docker(os.environ.get('JENKINS_HOST_URL'))
    result = run_in_docker(jenkins_url='http://localhost:8080')
    # TODO assert OID_NL == result
    pass