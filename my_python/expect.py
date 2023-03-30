import getpass
import logging
import socket
import time

import pexpect

DEFAULT_ENCODING = 'utf-8'
EOF = pexpect.exceptions.EOF
TIMEOUT = pexpect.exceptions.TIMEOUT
LOCAL_CREDS = {
    'hostname': socket.gethostname(),
    'username': getpass.getuser(),
}


class Spawn:
    """
    If you need to PIPE, REDIRECT or replace $parameters, then you need to run bash:
        spawn = Spawn('/bin/bash -c "ls -l | grep LOG > logs.txt"')
        spawn.expect(pexpect.EOF)
    """
    def __init__(self, command, timeout=30, **kw):
        self.kw = dict(kw)
        self.pexpect_spawn = pexpect.spawn(command=command, timeout=timeout)

    def expect(self, pattern, timeout=3):
        logging.debug(f'EXPECT: {pattern}  timeout: {timeout}')
        ndx = self.pexpect_spawn.expect(pattern=pattern, timeout=timeout)
        logging.debug(f'   NDX: {ndx} --> {self.pexpect_spawn.match}')
        return ndx

    def sendline(self, s=''):
        logging.debug(f'SENDLINE: {s}')
        bytes_sent = self.pexpect_spawn.sendline(s=s)
        if bytes_sent < len(s):
            # Only a limited number of bytes may be sent for each line in the default terminal mode
            logging.warning(f'ONLY {bytes_sent} BYTES SENT OF LENGTH: {len(s)}')

    def read(self, size=-1):
        bytes_read = self.pexpect_spawn.read(size=size)
        logging.debug(f'READ {bytes_read} BYTES')
        return bytes_read.decode(encoding='utf-8')

    def get_status(self):
        self.pexpect_spawn.close()
        return self.pexpect_spawn.status
        # or?? self.pexpect_spawn.signalstatus


class SpawnSSH(Spawn):
    def __init__(self, hostname, username, password, command='', timeout=30, prompt=None, banner=None, **kw):
        super(SpawnSSH, self).__init__(
            f'ssh {username}@{hostname} {command}'.strip(),
            hostname=hostname,
            username=username,
            password=password,
            timout=timeout,
            **kw)
        ndx = self.expect([f"\r{self.kw['username']}@{self.kw['hostname']}'s password: ", TIMEOUT], timeout=3)
        if ndx == 0:
            self.sendline(self.kw['password'])
            self.expect('\r\n', timeout=1)
        self.sendline()
        self.expect(TIMEOUT, 1)
        self.banner = list(self.get_before_lines())
        self.prompt = prompt or self.banner[-1]
        self.prompt = self.prompt.replace('$', '\\$')
        pass

    def get_before_lines(self):
        try:
            return self.pexpect_spawn.before.decode(encoding='utf-8').split('\r\n')
        except AttributeError:
            return list()

    def run_command(self, command, timeout=30):
        self.sendline(command)
        self.expect(self.prompt, timeout=timeout)
        return self.get_before_lines()

    def result_error_from_command(self, command, timeout=30):
        result_lines = self.run_command(command, timeout=timeout)
        error_lines = self.run_command('echo $?', timeout=1)
        return result_lines, error_lines


class Ilo5Creds:
    def __init__(self, hostname, username, password):
        # TODO default args to localhost
        self.hostname = hostname
        self.username = username
        self.password = password
        # self.prompt = r'\r\n</>hpiLO-> '
        self.prompt = r'>hpiLO-> '

    def spawn_ssh(self):
        spawn = pexpect.spawn(f'ssh {self.username}@{self.hostname}', timeout=-1)
        spawn.expect(f"\r{self.username}@{self.hostname}'s password: ", timeout=3)
        spawn.sendline(f'{self.password}')
        spawn.expect(self.prompt, timeout=3)
        return Ilo5Spawn(spawn, creds=self)


class Ilo5Spawn:
    def __init__(self, spawn, creds=None):
        self.spawn = spawn
        self.creds = creds
        # self.welcome_lines = spawn.before.decode(encoding='utf-8').split('\r\n')
        self.welcome_lines = self.lines()
        assert self.welcome_lines[1].startswith(f'User:{self.creds.username} logged-in to ILO')

    def sendline(self, s=''):
        logging.debug(f'SENDLINE: {s}')
        bytes_sent = self.spawn.sendline(s=s)
        if bytes_sent < len(s):
            # Only a limited number of bytes may be sent for each line in the default terminal mode
            logging.warning(f'ONLY {bytes_sent} BYTES SENT OF LENGTH: {len(s)}')

    def expect(self, pattern, timeout=-1):
        logging.debug(f'EXPECT: {pattern}  timeout: {timeout}')
        ndx = self.spawn.expect(pattern=pattern, timeout=timeout)
        logging.debug(f'NDX: {ndx}')
        return ndx

    @property
    def before(self):
        return self.spawn.before.decode(encoding='utf-8')

    def lines(self):
        raw_text = self.before
        return raw_text.split('\r\n')

    def show_virtual_cd_lines(self):
        self.spawn.sendline('cd /map1/oemhp_vm1/cddr1')
        self.spawn.expect(self.creds.prompt, timeout=3)

        self.spawn.sendline('show')
        self.spawn.expect(self.creds.prompt, timeout=3)

        return self.lines()

    def show_root_lines(self):
        self.spawn.sendline('cd /')
        self.spawn.expect(self.creds.prompt, timeout=3)

        self.spawn.sendline('show')
        self.spawn.expect(self.creds.prompt, timeout=3)

        return self.lines()

    def insert_virtual_cd(self):
        self.spawn.sendline('cd /map1/oemhp_vm1/cddr1')
        self.spawn.expect(self.creds.prompt, timeout=3)

        self.spawn.sendline('show')
        self.spawn.expect(self.creds.prompt, timeout=3)

        # before_lines = self.lines()

        # TODO pass this URI in
        self.spawn.sendline('set oemhp_image=http://10.216.178.67/all_in_one.iso')
        self.spawn.expect(self.creds.prompt, timeout=3)

        self.spawn.sendline('set oemhp_boot=connect')
        self.spawn.expect(self.creds.prompt, timeout=3)

        self.spawn.sendline('set oemhp_boot=once')
        self.spawn.expect(self.creds.prompt, timeout=3)

        self.spawn.sendline('show')
        self.spawn.expect(self.creds.prompt, timeout=3)

        return self.lines()

    def power_reset(self):
        self.spawn.sendline('power reset')
        self.spawn.expect(self.creds.prompt, timeout=3)
        time.sleep(15)
        return self.lines()
