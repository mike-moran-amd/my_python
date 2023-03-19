# encoding=UTF-8
"""
>>> JobTable2.from_text(data.text_from('Jenkins_root.htm')).print_repr_lines('jt')

"""
import logging
import os
import re
import requests
from my_python import data, table
from my_python.table.href import HrefTable

JENKINS_HOST_URL = 'JENKINS_HOST_URL'  # the environment variable that has URL to Jenkins server


def get_host_url():
    # this should be set in Dockerfile e.g. ENV JENKINS_HOST_URL=http://IP.ADD.RE.SS:PORT/
    host_url = os.environ.get(JENKINS_HOST_URL)
    return host_url


def get_response_text(url):
    requests_response = requests.get(url)
    if requests_response.status_code != 200:
        raise RuntimeError(f'INVALID RETURN CODE: {requests_response.status_code}')
    return requests_response.text


class JenkinsHost:
    def __init__(self, url=None):
        url = url or get_host_url()
        if not url:
            raise RuntimeError(f'Set environment variable "{JENKINS_HOST_URL}", for example "http://127.0.0.1:8080/"')
        self.__url = url

    def get_text(self, local_url):
        url = self.__url + '/' + local_url
        text = get_response_text(url)
        return text

    def install_jenkins_docker(self):
        if not self.ssh('which docker'):
            logging.error('DOCKER IS NOT INSTALLED')
            return
        self.ssh('docker network create jenkins')
        # TODO I think with a name, below does not restart on reboot and will not "start" unless container removed.
        self.ssh(
            f'docker run --restart=on-failure --detach --privileged --network jenkins --network-alias docker --env DOCKER_TLS_CERTDIR=/certs --volume jenkins-docker-certs:/certs/client --volume /var/jenkins_home:/var/jenkins_home --publish 2376:2376 docker:dind --storage-driver overlay2')

        jenkins_docker_version = '2.387.1'
        build_number = 4
        dockerfile_text = f'''
FROM jenkins/jenkins:{jenkins_docker_version}
USER root
RUN apt-get update && apt-get install -y lsb-release
RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
  https://download.docker.com/linux/debian/gpg
RUN echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
  https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
RUN apt-get update && apt-get install -y docker-ce-cli
RUN apt-get install -y python3-pip && pip3 install pexpect pytest-mock
USER jenkins
RUN jenkins-plugin-cli --plugins "blueocean docker-workflow"
'''[1:]  # REF: https://www.jenkins.io/doc/book/installing/docker/

        self.scp_text_file(dockerfile_text, 'Dockerfile')

        self.ssh(f'docker build -t myjenkins-blueocean:{jenkins_docker_version}-{build_number} .', timeout=120)
        # TODO sometimes this fails, check status code

        cid = self.ssh(
            f'docker run --name jenkins-blueocean --restart=on-failure --detach --network jenkins --env DOCKER_HOST=tcp://docker:2376 --env DOCKER_CERT_PATH=/certs/client --env DOCKER_TLS_VERIFY=1 --publish 8080:8080 --publish 50000:50000 --volume /var/jenkins_home:/var/jenkins_home --volume jenkins-docker-certs:/certs/client:ro -u $(id -u) myjenkins-blueocean:{jenkins_docker_version}-{build_number}')
        logging.debug(f'CID: {cid}')
        return cid

        '''
        log = self.ssh(f'docker logs {cid}')
        ss = log.split('Please use the following password to proceed to installation:')
        if len(ss) != 2:
            logging.error(f'CAN NOT FIND AUTIMATICALLY-GENERATED PASSWORD IN DOCKER LOG, len(ss): {len(ss)}')

        agpw = ss[1].lstrip().split('\n')[0].strip()
        logging.debug(f'AUTIMATICALLY-GENERATED PASSWORD: {agpw}')
        '''
        # TODO browse to http://localhost:8080 to unlock it using an automatically-generated password
        # TODO CLICK install suggested plugins
        # TODO ENTER admin credentials


class JobTable2(table.Table):

    @classmethod
    def from_text(cls, text):


        jt = cls()
        row = 0
        pre_name_re = '</td><td>'  # '</div></td><td>'
        post_name_pre_last_success = ''  # '</td>'
        post_last_success_pre_last_failure = ''  # '</td>' #'</td><td.+?>' #'</td>'
        post_last_failure_pre_last_duration = ''  # '</td>' #'</td><td.+?>' #</td>'
        post_last_duration = '</td><td></td><td>'  # '</td>'
        # for name, last_success, last_failure, last_duration in re.findall(
        for matches in re.findall(
                # pre_name_re + '(.+?)' +
                # post_name_pre_last_success + '(.+?)' +
                # post_last_success_pre_last_failure + '(.+?)' +
                # post_last_failure_pre_last_duration + '(.+?)' +
                # '        - <a href="job/Fedora%2036%7EFedora%2036%7Eqemu%20(ES)/lastFailedBuild/" class="model-link inside">#9</a></td><td data="125321">2 min 5 sec</td><td></td><td> '
                # '(.*?)<a href="(.+?)" class="model-link inside">(.*)</a></td><td data=".*">(.*)' + '</td><td></td><td>', text):
                # '(.+?)</td><td></td><td>(.+?)</td></tr>', text):
                # '(.+?)</table></div></td><td><a href="job/Fedora%2036%7EFedora%2036%7Eqemu%20\(ES\)/" class="model-link inside">Fedora 36<wbr>~Fedora 36<wbr>~qemu <wbr>\(ES\)</a></td><td data="2022-06-30T21:39:58Z">\n        5 days 3 hr\n        - <a href="job/Fedora%2036%7EFedora%2036%7Eqemu%20\(ES\)/lastSuccessfulBuild/" class="model-link inside">#12</a></td><td data="2022-06-29T22:03:03Z">\n        6 days 3 hr\n        - <a href="job/Fedora%2036%7EFedora%2036%7Eqemu%20\(ES\)/lastFailedBuild/" class="model-link inside">#9</a></td><td data="125321">2 min 5 sec</td><td></td><td>\xa0</td></tr>', text, re.DOTALL):
                #'</table></div></td><td><a href="(\w+)/Fedora%2036%7EFedora%2036%7Eqemu%20\(ES\)/" class="model-link inside">Fedora 36<wbr>~Fedora 36<wbr>~qemu <wbr>\(ES\)</a></td><td data="2022-06-30T21:39:58Z">\n        5 days 3 hr\n        - <a href="job/Fedora%2036%7EFedora%2036%7Eqemu%20\(ES\)/lastSuccessfulBuild/" class="model-link inside">#12</a></td><td data="2022-06-29T22:03:03Z">\n        6 days 3 hr\n        - <a href="job/Fedora%2036%7EFedora%2036%7Eqemu%20\(ES\)/lastFailedBuild/" class="model-link inside">#9</a></td><td data="125321">2 min 5 sec</td><td></td><td>\xa0</td></tr>',
                #'</tr><tr (.+?)><td data="\d+"><span (.+?)><span (.+?)"><svg(.+?)><use href="(.+?)"></use></svg></td><td>(.+?)</td><td align="right">(.+?)</td></tr></tbody></table></div></td><td>(.+?)</td><td data="\d+-\d+-\d+T\d+:\d+:\d+Z">(.+?)</td><td data="\d+-\d+-\d+T\d+:\d+:\d+Z">(.+?)</td><td data="\d+">(.+?)</td><td></td><td>\xa0</td></tr>',
                # '</td><td(.+?)</td><td(.+?)</td><td(.+?)</td><td(.+?)</td><td(.+?)</td><td(.+?)</td><td(.+?)</td><td(.+?)</td><td></td><td>\xa0</td></tr>',
                '<table(.*?)>(.+?)</table>',
                text, re.DOTALL):
            row += 1
            '''
            jt.set_val(row, 'tr_properties', matches[-11])
            jt.set_val(row, 'span1_properties', matches[-10])
            jt.set_val(row, 'span2_properties', matches[-9])
            jt.set_val(row, 'svg_properties', matches[-8])
            jt.set_val(row, 'use_href', matches[-7].replace('\n', '').replace('        ', ' ').strip())
            jt.set_val(row, 'build_stability', matches[-6])
            jt.set_val(row, 'percentage', matches[-5])
            jt.set_val(row, 'name', matches[-4])
            jt.set_val(row, 'last_success', matches[-3].replace('\n', '').replace('        ', ' ').strip())
            jt.set_val(row, 'last_failure', matches[-2].replace('\n', '').replace('        ', ' ').strip())
            jt.set_val(row, 'last_duration', matches[-1])
            '''
            #if row == 1:
            #    continue
            if isinstance(matches, str):
                matches = [matches]
            for counter in range(len(matches)):
                match = matches[counter]
                match.replace('\n', ' ')
                match.replace('\t', ' ')
                match = ' '.join(match.split())
                jt.set_val(row, f'{counter}_len', len(match))
                jt.set_val(row, counter, match)

        # end for matches
        for col in jt.col_gen():
            jt.right_pad_col(col)
        return jt


class JobTable(table.Table):

    @classmethod
    def from_jenkins_host(cls, jh=None):
        jh = jh or JenkinsHost()
        text = jh.get_text('')
        jt = JobTable.from_text(text)
        return jt

    @classmethod
    def from_text(cls, text, href_starts_with='job/'):
        ht = HrefTable.from_text(text, href_starts_with=href_starts_with)
        jt = cls()
        for ht_row in ht.row_gen():
            href = ht.get_href(ht_row)
            ss = href.split('/')
            if len(ss) < 3:
                continue
            job_name = ss[1]
            job_item = ss[2]
            job_value = ht.get_href_value(ht_row)
            jt.set_val(job_name, job_item, job_value)
        return jt

    def last_failed_build(self, job_name, col_label='lastFailedBuild'):
        val = self.get_val(job_name, col_label)
        if not val:
            return 0
        if val.startswith('>#'):
            val = val[2:]
        return int(val)

    def last_successful_build(self, job_name, col_label='lastSuccessfulBuild'):
        val = self.get_val(job_name, col_label)
        if not val:
            return 0
        if val.startswith('>#'):
            val = val[2:]
        return int(val)

    def passed(self, job_name):
        f = self.last_failed_build(job_name)
        p = self.last_successful_build(job_name)
        if not f:
            return True
        return p > f

    def last_build_number(self, job_name):
        if self.passed(job_name):
            return self.last_successful_build(job_name)
        return self.last_failed_build(job_name)
