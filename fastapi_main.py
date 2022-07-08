import fastapi
from fastapi.responses import HTMLResponse
from jenkins.dashboard import DashboardTable
from jenkins import JobTable
APP = fastapi.FastAPI()


@APP.get("/")
async def get_root():
    return {"message": "Hello World"}


@APP.get("/jenkins_dashboard", response_class=HTMLResponse)
async def jenkins_dashboard():
    jt = JobTable.from_jenkins_host()
    dt = DashboardTable.from_job_table(jt)
    html = ''.join(list(dt.html_gen()))
    return html
