#!python3
# encoding=utf-8
import getpass
from collections.abc import Iterable
import logging
import pexpect
import pprint
import socket
import time

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
        spawn.expect(EOF)
    """

    def __init__(self, *args, **kw):
        self.args = args
        self.kw = kw
        self.pexpect_spawn = pexpect.spawn(*self.args, **self.kw)

    def retry(self):
        if self.pexpect_spawn is not None:
            logging.debug('CLOSED')
            self.pexpect_spawn.close()
        logging.debug(f'RETRY')
        self.pexpect_spawn = pexpect.spawn(*self.args, **self.kw)

    def expect(self, *args, **kw):
        logging.debug(f'ndx = spawn.expect({repr_args_kw(args, kw)})')
        ndx = self.pexpect_spawn.expect(*args, **kw)
        logging.debug(f'# {ndx} --> {self.pexpect_spawn.match}')
        return ndx

    def sendline(self, s=''):
        logging.debug(f'spawn.sendline({repr_x(s)})')
        bytes_sent = self.pexpect_spawn.sendline(s=s)
        # logging.debug(f'# bytes_sent: {bytes_sent}')
        if bytes_sent < len(s):
            # Only a limited number of bytes may be sent for each line in the default terminal mode
            logging.warning(f'ONLY {bytes_sent} BYTES SENT OF LENGTH: {len(s)}')
        return bytes_sent

    '''
    def read(self, size=-1):
        bytes_read = self.pexpect_spawn.read(size=size)
        logging.debug(f'READ {bytes_read} BYTES')
        return bytes_read.decode(encoding='utf-8')
    '''

    def get_status(self):
        self.pexpect_spawn.close()
        status = self.pexpect_spawn.status
        logging.debug(f'# spawn.status: {status}')

    @property
    def before(self):
        before = self.pexpect_spawn.before
        logging.debug(f'# spawn.before: {before}')
        return before

    def get_before_lines(self):
        try:
            lines = self.pexpect_spawn.before.decode(encoding='utf-8').split('\r\n')
            logging.debug(f'GET BEFORE LINES: \n{pprint.pformat(lines)}')
            return lines
        except AttributeError:
            return list()


class SpawnBash(Spawn):
    def __init__(self,
                 hostname=socket.gethostname(),
                 username=getpass.getuser(),
                 password=None,
                 command='',
                 timeout=-1,
                 prompt=None,
                 banner=None,
                 send_sudo_password_limit=3):
        super(SpawnBash, self).__init__(f'bash {command}'.strip(), timeout=timeout)
        self.hostname = hostname
        self.username = username
        self.password = password
        self.prompt = prompt
        self.sudo_password_pattern = 'FIXME'  # TODO
        expect_pattern_list = [
            self.sudo_password_pattern,
            TIMEOUT]
        counter = 0
        while counter < send_sudo_password_limit:
            counter += 1
            if counter > 1:
                logging.debug(f'RETRY: {counter - 1}')
            ndx = self.expect(expect_pattern_list, timeout=4)
            if expect_pattern_list[ndx] == self.sudo_password_pattern:
                if counter > send_sudo_password_limit:
                    logging.error('INVALID PASSWORD LIMIT EXCEEDED: {counter}')
                    raise ValueError(counter)
                self.sendline(self.password)
                continue
            if expect_pattern_list[ndx] == TIMEOUT:
                logging.debug('BASH READY')
                break
        # end while
        self.prompt = prompt or self.get_before_lines()[-1]
        self.prompt = self.prompt.replace('$', '\\$')
        self.expect(self.prompt, timeout=1)
        logging.debug(f'self.before: {self.before}')


class SpawnSSH(Spawn):
    """
    """

    def handle_host_key_verification_failed(self):
        ss = self.before.decode('utf-8').split('remove with:')
        if len(ss) == 2:
            keygen_command = ss[1].strip()
            if keygen_command.startswith('ssh-keygen -f'):
                keygen_command = keygen_command.split('\n')[0].strip()
                logging.debug('REMOVING OLD KNOWN HOST')
                bash_spawn = SpawnBash(**LOCAL_CREDS)
                bash_spawn.sendline(keygen_command)
                bash_spawn.expect(bash_spawn.prompt, timeout=1)
                keygen_result = bash_spawn.get_before_lines()
                logging.debug(f'KEYGEN RESULT: {keygen_result}')
                bash_spawn.sendline('echo $?')
                bash_spawn.expect(bash_spawn.prompt, timeout=1)
                status_result = bash_spawn.get_before_lines()
                logging.debug(f'KEYGEN STATUS: {status_result}')
                bash_spawn.sendline('exit')
                bash_spawn.expect(EOF, timeout=1)
                assert status_result == '0'
                # the command will need to be retried
                logging.debug('RETRYING THE COMMAND')
                self.retry()

    def __init__(self,
                 hostname,
                 username,
                 password,
                 command='',
                 timeout=-1,
                 prompt=None,
                 banner_lines=None,
                 counter_limit=3):
        super(SpawnSSH, self).__init__(f'ssh {username}@{hostname} {command}'.strip(), timeout=timeout)
        self.hostname = hostname
        self.username = username
        self.password = password
        self.banner_lines = banner_lines
        self.prompt = prompt
        self.host_key_verification_failed_pattern = '\r\r\nHost key verification failed.\r\r\n'
        self.ssh_user_at_host_password_pattern = f"\r{self.username}@{self.hostname}'s password: "
        self.authenticity_pattern = '\? '  # 'Are you sure you want to continue connecting (yes/no/[fingerprint])\\? '
        expect_pattern_list = [
            self.host_key_verification_failed_pattern,
            self.authenticity_pattern,
            self.ssh_user_at_host_password_pattern,
            TIMEOUT]

        counter = 0
        while counter < counter_limit:
            counter += 1
            if counter > 1:
                logging.debug(f'RETRY: {counter - 1}')

            ndx = self.expect(expect_pattern_list, timeout=2)

            if expect_pattern_list[ndx] == self.host_key_verification_failed_pattern:
                if counter != 1:
                    logging.debug('WEIRD, THIS SHOULD HAVE BEEN FIXED LAST RETRY')
                    raise RuntimeError('INFINITE HOST KEY VALIDATION ERROR?')
                #  retry the spawn connection and replaces self.pexpect_spawn with new instance
                self.handle_host_key_verification_failed()
                continue
            elif expect_pattern_list[ndx] == self.authenticity_pattern:
                self.sendline('yes')
                self.expect('\r\n', timeout=1)
                continue
            elif expect_pattern_list[ndx] == self.ssh_user_at_host_password_pattern:
                self.sendline(self.password)
                self.expect('\r\n', timeout=1)
                continue
            elif expect_pattern_list[ndx] == TIMEOUT:
                self.banner_lines = banner_lines or self.get_before_lines()
                self.prompt = prompt or self.banner_lines[-1].replace('$', '\\$')
                self.expect(self.prompt, timeout=1)
                logging.debug('SpawnSSH READY')
                break

    def result_from_command(self, command, timeout=1.0) -> str:
        self.sendline(command)
        self.expect(self.prompt, timeout=timeout)
        lines = self.get_before_lines()
        assert lines[0] == command
        assert lines[-1] == ''
        result = '\n'.join(lines[1:])
        return result

    def result_status_from_command(self, command, timeout=30):
        result = self.result_from_command(command, timeout=timeout)
        status = self.result_from_command('echo $?', timeout=.1)
        status = status.strip()
        return result, status

    def command_lines(self, command, timeout=30):
        return [
            self.result_status_from_command(command, timeout=timeout),
            self.result_status_from_command('echo $?', timeout=1),
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


def repr_x(x):
    if x == TIMEOUT:
        return 'pexpect.exceptions.TIMEOUT'
    elif x == EOF:
        return 'pexpect.exceptions.EOF'
    elif isinstance(x, str):
        # str is iterable, next elif goes to infinity without this
        return pprint.pformat(x)
    elif isinstance(x, Iterable):
        return ', '.join([repr_x(i) for i in x])
    else:
        return pprint.pformat(x)


def repr_kw(kw):
    return ', '.join([f'{k}={repr_x(v)}' for k, v in kw.items()])


def repr_args_kw(args, kw):
    # logging.debug(f'ARGS: {args}')
    # logging.debug(f'KW: {kw}')

    #new_args = repr_x(args)
    new_args = pf(args)
    new_kw = repr_kw(kw)

    # logging.debug(f'NEW ARGS: {new_args}')
    # logging.debug(f'NEW KW: {new_kw}')
    result = f'{new_args}, {new_kw}'
    result = result.replace("<class 'pexpect.exceptions.TIMEOUT'>", 'TIMEOUT')
    result = result.replace("<class 'pexpect.exceptions.EOF'>", 'EOF')
    return result


def pf(x):
    return f'{pprint.pformat(x, compact=True, width=200)}'
