from my_python import jenkins, table
from urllib import parse

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
        yield '<style>table, th, td, p { border: 1px solid black; border-collapse: collapse; padding: 5px; text-align:center;"}</style>'  # noqa
        yield '</head>'
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
                ss = val.split('~')
                link_text = ss[0]
                href = split_char.join(ss[1:])
                if link_text == 'FAIL':
                    style = 'style="color:red;" '
                else:
                    style = ''
                a_ref = f'<a {style}href={href}>{link_text}</a>'
                yield f'<td>{a_ref}</td>'
            yield '</tr>'
        # end for row
        yield '</table'
        yield '</body>'
        yield '</html>'
