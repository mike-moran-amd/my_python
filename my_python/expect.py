import getpass
from collections.abc import Iterable
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
    def __init__(self, *args, **kw):
        logging.debug(f"spawn = pexpect.spawn({repr_args_kw(args, kw)})")
        self.pexpect_spawn = pexpect.spawn(*args, **kw)

    def expect(self, *args, **kw):
        #logging.debug(f"ndx = spawn.expect({repr_args_kw(args, kw)})")
        ndx = self.pexpect_spawn.expect(*args, **kw)
        logging.debug(f'ndx = spawn.expect({repr_args_kw(args, kw)})  # ndx: {ndx}  --> {self.pexpect_spawn.match}')
        return ndx

    def sendline(self, s=''):
        logging.debug(f'spawn.sendline({repr(s)})')
        bytes_sent = self.pexpect_spawn.sendline(s=s)
        # logging.debug(f'# bytes_sent: {bytes_sent}')
        return bytes_sent

    '''
    def read(self, size=-1):
        bytes_read = self.pexpect_spawn.read(size=size)
        logging.debug(f'READ {bytes_read} BYTES')
        return bytes_read.decode(encoding='utf-8')
    '''

    def get_status(self):
        self.pexpect_spawn.close()
        return self.pexpect_spawn.status
        # or?? self.pexpect_spawn.signalstatus

    @property
    def before(self):
        before = self.pexpect_spawn.before
        logging.debug(f'# spawn.before: {before}')
        return before


class SpawnSSH(Spawn):
    """
    """
    def __init__(self, hostname, username, password, command='', timeout=-1, prompt=None, banner=None, **kw):
        super(SpawnSSH, self).__init__(f'ssh {username}@{hostname} {command}'.strip(), timeout=timeout, **kw)
        self.hostname = hostname
        self.username = username
        self.password = password
        self.banner = banner
        self.prompt = prompt
        ndx = self.expect([f"\r{self.username}@{self.hostname}'s password: ", TIMEOUT], timeout=3)
        if ndx == 0:
            self.sendline(self.password)
            self.expect('\r\n', timeout=1)
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
        #self.expect(TIMEOUT, timeout=1)
        self.expect(TIMEOUT, timeout=.1)


        return self.get_before_lines()

    def command_lines(self, command, timeout=30):
        return [
            self.run_command(command, timeout=timeout),
            self.run_command('echo $?', timeout=1),
        ]

    def sendline(self, s=''):
        bytes_sent = super(SpawnSSH, self).sendline(s)
        if bytes_sent < len(s):
            # Only a limited number of bytes may be sent for each line in the default terminal mode
            logging.warning(f'ONLY {bytes_sent} BYTES SENT OF LENGTH: {len(s)}')


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


def repr_args(x):
    if isinstance(x, str):
        return repr(x)
    elif isinstance(x, int):
        return x
    elif x == pexpect.exceptions.TIMEOUT:
        return 'pexpect.exceptions.TIMEOUT'
    elif x == pexpect.exceptions.EOF:
        return 'pexpect.exceptions.EOF'
    elif isinstance(x, tuple):
        tup = x
        new_args = []
        for x in tup:
            if x == pexpect.exceptions.TIMEOUT:
                new_args.append('pexpect.exceptions.TIMEOUT')
                continue
            elif x == pexpect.exceptions.EOF:
                new_args.append('pexpect.exceptions.EOF')
                continue
            elif isinstance(x, int):
                new_args.append(x)
                continue
            elif isinstance(x, str):
                new_args.append(repr(x))
                continue
            elif isinstance(x, Iterable):
                for arg in x:
                    if arg == pexpect.exceptions.TIMEOUT:
                        new_args.append('pexpect.exceptions.TIMEOUT')
                    elif arg == pexpect.exceptions.EOF:
                        new_args.append('pexpect.exceptions.EOF')
                    else:
                        new_args.append(arg)
            else:
                raise ValueError(type(x))
        return ', '.join([repr(a) for a in new_args])
    else:
        raise ValueError(x)


def my_repr(c):
    if isinstance(c, pexpect.exceptions.TIMEOUT):
        return 'pexpect.exceptions.TIMEOUT'
    else:
        return repr(c)


def repr_kw(kw):
    return ', '.join([f' {k}={my_repr(v)}' for k, v in kw.items()])


def repr_args_kw(args, kw):
    return f'{repr_args(args)},{repr_kw(kw)}'

