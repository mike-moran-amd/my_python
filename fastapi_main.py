import fastapi
from jenkins.dashboard import DashboardTable
from jenkins import JobTable
APP = fastapi.FastAPI()


@APP.get("/")
async def get_root():
    return {"message": "Hello World"}


@APP.get("/jenkins_dashboard")
async def jenkins_dashboard():
    jt = JobTable.from_jenking_host()
    dt = DashboardTable.from_job_table(jt)
    html = ''.join(list(dt.html_gen()))
    return html
