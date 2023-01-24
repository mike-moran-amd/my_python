import logging
import pexpect
from pexpect.exceptions import EOF

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
                  timeout=30,
                  expect_timeout=2,
                  ):

        ssh_command = f'ssh {self.user_at_host()} {command}'
        logging.debug(f'pexpect.spawn(command={repr(ssh_command)}, timeout={repr(timeout)}')
        child = pexpect.spawn(command=ssh_command, timeout=timeout)
        logging.debug(f'child spawned')

        logging.debug(f'BEFORE {repr(child.before)}')
        logging.debug(f'AFTER  {repr(child.after)}')

        self_read = None
        try:
            ndx = child.expect(pattern=expect_challenge, timeout=expect_timeout)
            logging.debug(f'EXPECT NDX: {ndx}')

            logging.debug(f'BEFORE {repr(child.before)}')
            logging.debug(f'AFTER  {repr(child.after)}')

            child.sendline(self.__password)
            logging.debug('PASSWORD SENT')

        except EOF as eof:
            logging.debug(f'EXCEPT EOF {eof}')
            self_read = child.before.decode(encoding=self.__encoding).strip()

        return Child(child, self_read=self_read, encoding=self.__encoding)


class Child:
    def __init__(self, spawn_child, self_read=None, encoding='utf-8'):
        self.__spawn_child = spawn_child
        self.__encoding = encoding
        self.__self_read = self_read

    def read(self, size=-1):
        if self.__self_read is not None:
            # if the challenge is not received, everything in the child.before buffer is the result
            ret = self.__self_read
            # disable this code path on next read()
            self.__self_read = None
            return ret
        # return read() from child
        result_bytes = self.__spawn_child.read(size=size)
        return result_bytes.decode(encoding=self.__encoding).strip()

    def sendline(self, s=''):
        return self.__spawn_child.sendline(s=s)

    def close(self):
        self.__spawn_child.close()

    def is_closed(self):
        return self.__spawn_child.close

    def signal_status(self):
        return self.__spawn_child.signalstatus

    def status(self):
        return self.__spawn_child.status
