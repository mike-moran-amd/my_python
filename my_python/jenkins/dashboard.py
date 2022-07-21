import pathlib
from urllib import parse
from my_python import lib, jenkins, table, VERSION
SPLIT_CHAR = '~'


class DashboardTable(table.Table):

    @classmethod
    def from_job_table(cls, jt, split_char=SPLIT_CHAR):
        t = cls()
        jenkins_url = jenkins.get_host_url()
        for job_name in sorted(list(jt.row_gen())):
            quote_job_name = parse.quote(job_name)
            last_build_number = jt.last_build_number(job_name)
            href_link = f'{jenkins_url}/job/{quote_job_name}/{last_build_number}/console'
            ss = job_name.split(split_char)
            if len(ss) < 3:
                continue
            host = ss[0]
            guest = ss[1]
            host_guest = f'{host}{split_char}{guest}'
            component = ss[2]
            pass_fail = 'pass' if jt.passed(job_name) else 'FAIL'
            status_href = f'{pass_fail}{split_char}{href_link}'
            t.set_val(host_guest, component, status_href)
        # end for job_name
        return t

    def html_gen(self, split_char=SPLIT_CHAR):
        yield '<!DOCTYPE html>'
        yield '<html>'
        yield '<head>'
        yield '<title>Latest Jenkins Build Results</title>'
        yield '</head>'
        yield '<style>table, th, td, p { border: 1px solid black; border-collapse: collapse; padding: 5px; text-align:center;"}</style>'  # noqa
        yield '<body>'
        yield '<table>'
        yield '<tr>'
        yield '<th>HOST</th>'
        yield '<th>GUEST</th>'
        for component in self.col_gen():
            yield f'<th>{component}</th>'
        last_host = None
        for host_guest in self.row_gen():
            yield '<tr>'
            ss = host_guest.split(split_char)
            host = ss[0]
            if host == last_host:
                host = ''
            else:
                last_host = host
            guest = ss[1]
            yield f'<td>{host}</td>'
            yield f'<td>{guest}</td>'
            for component in self.col_gen():
                val = self.get_val(host_guest, component)
                a_ref = ''
                bgColor = 'grey'
                if val is not None:
                    ss = val.split('~')
                    link_text = ss[0]
                    href = split_char.join(ss[1:])
                    if link_text == 'FAIL':
                        style = 'style="backround-color:red;" '
                        bgColor = 'red'
                    elif link_text == 'pass':
                        style = 'style="background-color:green;" '
                        bgColor = 'green'
                    else:
                        style = 'style="background-color:grey;" '
                        bgColor = 'red'
                    #a_ref = f'<a {style}href={href}>{link_text}</a>'
                    a_ref = f'<a href={href}>{link_text}</a>'
                yield f'<td bgcolor="{bgColor}">{a_ref}</td>'
            yield '</tr>'
        # end for row
        yield '</table'
        yield '</body>'
        yield '</html>'


def run_in_docker(jenkins_url,
                  host_port=4231,
                  docker_port=4231,
                  is_detached=True,
                  tag='jenkins_dashboard',
                  version=VERSION,
                  work_dir='/opt'):
    cmd_list = [lib.path_for_command('docker'), 'build']
    image_name = ':'.join([tag, version])
    cmd_list.extend(['-t', image_name])
    dockerfile_parent_path = pathlib.Path(__file__).parent.parent.parent
    cmd_list.append(str(dockerfile_parent_path))
    dockerfile_path = pathlib.Path(dockerfile_parent_path, 'Dockerfile')
    with open(dockerfile_path, 'w') as df:
        lines = [
            'FROM python:3.9\n',
            'COPY requirements.txt /opt/requirements.txt\n',
            'RUN pip install --no-cache-dir --upgrade -r /opt/requirements.txt\n',
            f'WORKDIR {work_dir}\n',
            f'COPY my_python {work_dir}/my_python\n',
            f'ENV JENKINS_HOST_URL={jenkins_url}\n',
            f'CMD ["uvicorn", "my_python.fastapi_main:APP", "--host", "0.0.0.0", "--port", "{docker_port}"]\n',
        ]
        df.writelines(lines)
    build_output = lib.invoke_subprocess(cmd_list)  # noqa
    # TODO error checking, we assume now that if the command above had non-zero exit code that it failed

    # Dockerfile contains confidential info, toast when done!
    dockerfile_path.unlink()
    cmd_list = [lib.path_for_command('docker'), 'run']
    cmd_list.extend(['-p', f'{host_port}:{docker_port}'])
    if is_detached:
        cmd_list.append('-d')
        # NOTE otherwise the subprocess will block (below)
    cmd_list.extend(['-t', image_name])
    run_output = lib.invoke_subprocess(cmd_list)
    # this is oid then newline
    return run_output
    # TODO refactor above to my_python.docker module call
