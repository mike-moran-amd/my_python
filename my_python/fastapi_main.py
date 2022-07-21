import fastapi
from fastapi.responses import HTMLResponse
from my_python.jenkins.dashboard import DashboardTable
from my_python.jenkins import JobTable
APP = fastapi.FastAPI()


@APP.get("/")
async def get_root():
    return {"message": "Hello World"}


@APP.get("/SEV_Dashboard", response_class=HTMLResponse)
async def get_jenkins_dashboard():
    jt = JobTable.from_jenkins_host()
    dt = DashboardTable.from_job_table(jt)
    html = ''.join(list(dt.html_gen()))
    return html
