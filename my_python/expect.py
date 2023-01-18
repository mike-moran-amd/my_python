import logging
import pexpect

DEFAULT_ENCODING = 'utf-8'


class Creds:
    def __init__(self, hostname, username, password, encoding='utf-8'):
        self.__hostname = hostname
        self.__username = username
        self.__password = password
        self.__encoding = encoding

    def user_at_host(self):
        return self.__username + '@' + self.__hostname

    def password_newline_bytes(self):
        return f'{self.__password}\n'.encode(encoding=self.__encoding)

    def spawn_ssh(self,
                  command,
                  expect_challenge='password:',
                  child_logfile=None,
                  child_logfile_read=None,
                  child_logfile_send=None,
                  timeout=30,
                  ):
        ssh_command = f'ssh {self.user_at_host()} {command}'
        child = pexpect.spawn(command=ssh_command, timeout=timeout)
        logging.log(logging.DEBUG, f'pexpect.spawn(command={repr(ssh_command)}, timeout={repr(timeout)}')

        # make io available for progress watching
        child.logfile = child_logfile
        child.logfile_read = child_logfile_read
        child.logfile_send = child_logfile_send

        pattern = [
            pexpect.TIMEOUT,
            'Are you sure you want to continue connecting (yes/no/[fingerprint])? ',
            expect_challenge,
        ]
        logging.log(logging.DEBUG, f'pattern = {pattern}')

        expect_ndx = child.expect(pattern=pattern)
        logging.debug(f'expect_ndx = {expect_ndx}')

        if expect_ndx == 0:
            logging.log(logging.DEBUG, f'child = {child}')
        elif expect_ndx == 1:
            child.send(bytes('yes\r'))
            pass
        else:
            child.send(self.password_newline_bytes())
            logging.log(logging.DEBUG, f'SENT CREDS')
        # end with child, close() sets child exit/signal status
        return Child(child, encoding=self.__encoding)


class Child:
    def __init__(self, spawn_child, encoding='utf-8'):
        self.__spawn_child = spawn_child
        self.__encoding = encoding

    def read(self, size=-1):
        result_bytes = self.__spawn_child.read(size=size)
        return result_bytes.decode(encoding=self.__encoding)

    def close(self):
        self.__spawn_child.close()

    def is_closed(self):
        return self.__spawn_child.close

    def signal_status(self):
        return self.__spawn_child.signalstatus

    def status(self):
        return self.__spawn_child.status
