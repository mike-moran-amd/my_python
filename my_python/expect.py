import getpass
import logging
import socket
import time

import pexpect

DEFAULT_ENCODING = 'utf-8'
EOF = pexpect.exceptions.EOF
TIMEOUT = pexpect.exceptions.TIMEOUT


class Creds:
    def __init__(self, password: str, hostname=None, username=None, encoding=None):
        self.__password = password
        self.hostname = hostname or socket.gethostname()
        self.username = username or getpass.getuser()
        self.encoding = encoding or 'utf-8'
        self.ssh_password_required = None

    def spawn(self, command, timeout=30):
        logging.debug(f'SPAWN: {command}  timeout: {timeout}')
        return Spawn(pexpect.spawn(command=command, timeout=timeout), creds=self)

    def user_at_host(self) -> str:
        return self.username + '@' + self.hostname

    def get_password(self):
        return self.__password

    def ssh_passsword_challenge(self):
        return f"\r{self.username}@{self.hostname}'s password: "

    def spawn_ssh(self, command='', timeout=-1):
        ssh_command = f'ssh {self.user_at_host()} {command}'.strip()
        spawn = self.spawn(ssh_command, timeout=timeout)
        if self.ssh_password_required in [None, True]:
            time.sleep(3)
            ndx = spawn.expect(pattern=[TIMEOUT, self.ssh_passsword_challenge()],  timeout=1)
            if ndx:
                logging.debug('PASSWORD REQUIRED')
                #self.ssh_password_required = True
            else:
                logging.debug('PASSWORD NOT REQUIRED')
                #self.ssh_password_required = False
        return spawn


class Spawn:
    """
    If you need to PIPE, REDIRECT or replace $parameters, then you need to run bash:
        spawn = Spawn('/bin/bash -c "ls -l | grep LOG > logs.txt"')
        spawn.expect(pexpect.EOF)
    """
    def __init__(self, pexpect_child, creds=None):
        self.pexpect_child = pexpect_child
        self.creds = creds

    def expect(self, pattern, timeout=-1, depth=2):
        logging.debug(f'EXPECT: {pattern}  timeout: {timeout}')
        counter = 0
        while depth - counter > 0:
            counter += 1
            ndx = self.pexpect_child.expect(pattern=pattern, timeout=timeout)
            logging.debug(f'  NDX: {ndx}')
            if pattern[ndx] == self.creds.ssh_passsword_challenge():
                logging.debug('GOT SSH PASSWORD CHALLENGE')
                self.sendline(self.creds.get_password())
                ndx = self.expect([TIMEOUT, '\r\n'], timeout=1)
                continue
            return ndx

    @property
    def before(self):
        return self.pexpect_child.before.decode(encoding=self.creds.encoding)

    @property
    def after(self):
        return self.pexpect_child

    @property
    def match(self):
        # no decode, could be EOF or TIMEOUT
        return self.pexpect_child.match

    def sendline(self, s=''):
        logging.debug(f'SENDLINE: {s}')
        bytes_sent = self.pexpect_child.sendline(s=s)
        if bytes_sent < len(s):
            # Only a limited number of bytes may be sent for each line in the default terminal mode
            logging.warning(f'ONLY {bytes_sent} BYTES SENT OF LENGTH: {len(s)}')

    def read(self, size=-1):
        bytes_read = self.pexpect_child.read(size=size)
        logging.debug(f'READ {bytes_read} BYTES')
        return bytes_read.decode(encoding=self.creds.encoding)

    def get_status(self):
        self.pexpect_child.close()
        return self.pexpect_child.status
        # or?? self.pexpect_child.signalstatus
