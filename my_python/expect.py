#!python3
# encoding=utf-8
import getpass
import logging
import pexpect
import pprint
import socket
import time

EOF = pexpect.exceptions.EOF
TIMEOUT = pexpect.exceptions.TIMEOUT


def pf(x, compact=True, width=200):
    ret = f'{pprint.pformat(x, compact=compact, width=width)}'
    ret = ret.replace("<class 'pexpect.exceptions.TIMEOUT'>", 'TIMEOUT')
    ret = ret.replace("<class 'pexpect.exceptions.EOF'>", 'EOF')
    return ret


LOCAL_CREDS = {
    'hostname': socket.gethostname(),
    'username': getpass.getuser(),
}


def pattern_for_expect(pattern: str) -> str:
    retval = pattern
    # These symbols have special meanings in regular expression pattern matching and must be "escaped"
    retval = retval.replace('?', '\\?')
    retval = retval.replace('[', '\\[')
    retval = retval.replace(']', '\\]')
    retval = retval.replace('(', '\\(')
    retval = retval.replace(')', '\\)')
    return retval


class Spawn:
    """
    If you need to PIPE, REDIRECT or replace $parameters, then you need to run bash:
        spawn = Spawn('/bin/bash -c "ls -l | grep LOG > logs.txt"')
        spawn.expect(EOF)
    """

    def __init__(self, *args, **kw):
        self.args = args
        self.kw = kw
        self.pexpect_spawn = None
        self.invoke()

    def __repr__(self) -> str:
        s = f"({pf(self.args)}, {', '.join([f'{k}={pf(v)}' for k, v in self.kw.items()])})"
        return f'pexpect.spawn{s}'

    def invoke(self):
        logging.debug(f'SPAWN.INVOKE {self}')
        self.pexpect_spawn = pexpect.spawn(*self.args, **self.kw)

    def close(self):
        if self.pexpect_spawn is not None:
            logging.debug(f'SPAWN.CLOSE {self}')
            self.pexpect_spawn.close()
            self.pexpect_spawn = None

    def retry(self):
        logging.debug(f'SPAWN.RETRY {self}')
        self.close()
        self.invoke()

    def expect(self, *args, **kw):
        s = f"({pf(args)}, {', '.join([f'{k}={pf(v)}' for k, v in kw.items()])})"
        logging.debug(f'NDX = SPAWN.EXPECT{s}')
        ndx = self.pexpect_spawn.expect(*args, **kw)
        logging.debug(f'  {ndx} = {pf(self.pexpect_spawn.match)}')
        return ndx

    def sendline(self, s=''):
        logging.debug(f'SPAWN.SENDLINE({pf(s)})')
        bytes_sent = self.pexpect_spawn.sendline(s=s)
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
        logging.debug(f'SPAWN.STATUS: {status}')
        return status

    def get_before_lines(self):
        try:
            lines = self.pexpect_spawn.before.decode(encoding='utf-8').split('\r\n')
            logging.debug(f'GET BEFORE LINES: \n{pprint.pformat(lines, width=200)}\n')
            return lines
        except AttributeError:
            return list()

    '''
    @property
    def before(self):
        before = self.pexpect_spawn.before
        logging.debug(f'# spawn.before: {before}')
        return before
    '''

    def get_prompt(self) -> str:
        self.expect(TIMEOUT, timeout=1)
        lines = self.get_before_lines()
        prompt = lines[-1]
        if not prompt:
            logging.error(f'PROMPT IS INVALID - LINES: \n{pf(lines, compact=False)}\n')
            raise ValueError(lines)
        return pattern_for_expect(prompt)


class CredSpawn(Spawn):
    """
    Provides credentials for Spawn expect() commands
    """
    def __init__(
            self,
            command,
            hostname=socket.gethostname(),
            username=getpass.getuser(),
            password=None,
            **kw):
        kw['timeout'] = kw.get('timeout', -1)
        super(CredSpawn, self).__init__(command, **kw)
        self.hostname = hostname
        self.username = username
        self.password = password
        # useful inspection attributes tailored for debugging and logging
        self.before = ''
        self.lls = []

        if self.hostname != socket.gethostname():
            # expect these when invoking remote commands like "ssh"
            self.check_host_key_verification_failed()
            self.handle_authenticity_of_host_challenge()
            self.handle_ssh_username_at_hostname_password_challenge()
            pass

    def check_host_key_verification_failed(self):
        pattern = pattern_for_expect('\r\r\nHost key verification failed.\r\r\n')
        if 1 == self.expect([pattern, TIMEOUT], timeout=1):
            return
        logging.debug('HOST KEY VERIFICATION FAILED')
        keygen_command = f'ssh-keygen -R {self.hostname}'  # this default works, but offered methods may be better.
        # Ubuntu sends the ssh-keygen command we need to remove the offending host key, use it if present
        ss = self.before.split('remove with:')
        if len(ss) == 2:
            s = ss[1].strip()
            if s.startswith('ssh-keygen -f'):
                keygen_command = s.split('\n')[0].strip()
                logging.debug(f'KEYGEN COMMAND FROM EXPECT: {keygen_command}')

        if keygen_command is None:
            logging.debug('UNABLE TO DETERMINE SSH-KEYGEN COMMAND')
            raise RuntimeError()

        logging.debug('REMOVING OLD KNOWN HOST')
        spawn = Spawn(keygen_command)
        spawn.expect(EOF, timeout=1)
        status = spawn.get_status()
        if status != 0:
            logging.error(f'EXPECTED 0 == STATUS GOT: {status}')
            raise ValueError(status)
        self.retry()

    def handle_authenticity_of_host_challenge(self):
        #pattern = pattern_for_expect('Are you sure you want to continue connecting (yes/no/[fingerprint])? ')
        pattern = pattern_for_expect('continue connecting (yes/no/[fingerprint])? ')
        if 0 == self.expect([pattern, TIMEOUT], timeout=1):
            logging.debug("handle_authenticity_of_host_challenge")
            self.sendline('yes')
            self.expect(['\r\n'], timeout=1)

    def handle_ssh_username_at_hostname_password_challenge(self):
        pattern = f"{self.username}@{self.hostname}'s password: "
        if 0 == self.expect([pattern, TIMEOUT], timeout=1):
            logging.debug("handle_ssh_username_at_hostname_password_challenge")
            self.sendline(self.password)
            self.expect(['\r\n'], timeout=1)

    def expect(self, *args, **kw):
        ndx = super(CredSpawn, self).expect(*args, **kw)
        self.before = self.pexpect_spawn.before.decode(encoding='utf-8')
        self.lls.append(self.before.split('\r\n'))
        return ndx


class SpawnBash(Spawn):
    def __init__(self,
                 command='',
                 hostname=socket.gethostname(),
                 username=getpass.getuser(),
                 password=None,
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
            #self.sudo_password_pattern,
            TIMEOUT]
        counter = 0
        while counter < send_sudo_password_limit:
            counter += 1
            if counter > 1:
                logging.debug(f'RETRY: {counter - 1}')
            # TODO the sudo password could be expected for all overloaded expect(), maybe?
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
        logging.debug(f'HANDLE HOSTKEY VERIFICATION: {ss}')
        if len(ss) == 2:
            keygen_command = ss[1].strip()
            if keygen_command.startswith('ssh-keygen -f'):
                logging.debug(f'KEYGEN COMMAND: {keygen_command}')
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
                assert status_result == ['echo $?', '0', '']


                # Instead of trying to exit gracefully (which is causing problems) just retry
                #bash_spawn.sendline('exit')
                #ndx = bash_spawn.expect([EOF, TIMEOUT], timeout=1)


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
                 counter_limit=4):
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
                return
        logging.error(f'COUNTER_LIMIT: {counter_limit} EXCEEDED')
        raise ValueError(counter_limit)

    def result_from_command(self, command, timeout=1.0) -> str:
        self.sendline(command)
        self.expect(self.prompt, timeout=timeout)
        lines = self.get_before_lines()
        assert lines[0] == command
        assert lines[-1] == ''
        result = '\n'.join(lines[1:])
        return result

    def status_from_command(self, command, timeout=1.0) -> str:
        self.sendline(command)
        self.expect(self.prompt, timeout=timeout)
        status = self.result_from_command('echo $?', timeout=.1)
        status = status.strip()
        return status

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

    def sudo_bash(self):
        self.sendline('sudo bash')
        self.expect('\r\n', timeout=1)
        ndx = self.expect([f'password for {self.username}: ', TIMEOUT], timeout=1)
        if ndx == 0:
            self.sendline(self.password)
            self.expect('\r\n', timeout=1)
        ndx = self.expect(TIMEOUT, timeout=.1)
        new_prompt = self.get_before_lines()[0]
        self.expect(new_prompt, timeout=1)
        logging.debug('SUDO BASH READY')
        return new_prompt


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


