import logging
import pexpect
from pexpect.exceptions import EOF, TIMEOUT

DEFAULT_ENCODING = 'utf-8'


class Creds:
    def __init__(self, hostname, username, password, encoding='utf-8'):
        self.__hostname = hostname
        self.__username = username
        self.__password = password
        self.__encoding = encoding

    def user_at_host(self):
        return self.__username + '@' + self.__hostname

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

    def pexpect_spawn(self, command, timeout=30):
        logging.debug(f'pexpect.spawn(command={repr(command)}, timeout={repr(timeout)}')
        child = pexpect.spawn(command=command, timeout=timeout)
        logging.debug(f'pexpect child spawned')

        return Child(child, self_read=None, creds=self, encoding=self.__encoding)

    def get_password(self):
        logging.debug(f'PASSWORD SENT')
        return self.__password

    def uname(self):
        child = self.pexpect_spawn(f'ssh {self.user_at_host()} uname -a', timeout=3)
        child.expect()
        result = child.read()
        child.close()
        logging.debug(f'uname={repr(result)}')
        return result


class Child:
    def __init__(self, spawn_child, self_read=None, creds=None, encoding='utf-8'):
        self.__spawn_child = spawn_child
        self.__self_read = self_read
        self.__creds = creds
        self.__encoding = encoding
        self.__before_read = ''

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
        return self.__spawn_child.closed

    def signal_status(self):
        return self.__spawn_child.signalstatus

    def status(self):
        return self.__spawn_child.status

    def expect(self, pattern=None, expect_timeout=2):

        pattern = pattern or {
            # pexpect.EOF: None,
            'password:': lambda: self.sendline(self.__creds.get_password()),
        }
        keys = list(pattern.keys())

        logging.debug(f'BEFORE {self.__spawn_child.before}')
        logging.debug(f'AFTER  {self.__spawn_child.after}')

        ndx = None
        while not ndx:
            try:
                logging.debug('calling expect')
                ndx = self.__spawn_child.expect(pattern=keys, timeout=expect_timeout)
                logging.debug(f'EXPECT NDX: {ndx}')
                key = keys[ndx]
                fn = pattern[key]
                if callable(fn):
                    logging.debug(f'CALLING fn() for challenge: {repr(key)}')
                    fn()
                    logging.debug(f'fn() CALLED')
                elif isinstance(fn, str):
                    self.sendline(fn)
                else:
                    logging.warning(f'UNKNOWN TYPE: {type(fn)}')
                return True
            except TIMEOUT:
                if self.before_endswith('continue connecting (yes/no/[fingerprint])? '):
                    logging.debug('SENT "yes" to connect')
                    self.sendline('yes')
                else:
                    raise
            except EOF:
                logging.debug('The pattern was not seen')
                # make the next read() get the result
                self.__self_read = self.before.decode(encoding=self.__encoding).strip()
                return False

    def before_endswith(self, s):
        value = self.__spawn_child.before
        if isinstance(value, bytes):
            value_str = value.decode(encoding=self.__encoding)
            if value_str.endswith(s):
                return True
        return False

    @property
    def before(self):
        return self.__spawn_child.before
