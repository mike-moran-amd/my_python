import logging
import pexpect

DEFAULT_ENCODING = 'utf-8'


class Creds:
    def __init__(self, hostname, username, password):
        self.__hostname = hostname
        self.__username = username
        self.__password = password

    def user_at_host(self):
        return self.__username + '@' + self.__hostname

    def password_newline_bytes(self, encoding=DEFAULT_ENCODING):
        return f'{self.__password}\n'.encode(encoding=encoding)


def pexpect_spawn_ssh(
        creds,
        command,
        expect_challenge='password:',
        child_logfile=None,
        child_logfile_read=None,
        child_logfile_send=None,
        timeout=3,
        encoding=DEFAULT_ENCODING):
    with pexpect.spawn(f'ssh {creds.user_at_host()} {command}', timeout=timeout) as child:
        # make io available for progress watching
        child.logfile = child_logfile
        child.logfile_read = child_logfile_read
        child.logfile_send = child_logfile_send

        expect_ndx = child.expect([pexpect.TIMEOUT, expect_challenge])

        if expect_ndx == 0:
            logging.log(logging.INFO, f'TIMEOUT:  before={child.before}  after={child.after}')
            return None, child
        else:
            child.send(creds.password_newline_bytes(encoding=encoding))
        result = child.read()
    # end with child, close() sets child exit/signal status
    return result, child
