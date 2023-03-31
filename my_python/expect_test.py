import io
import logging
import pprint

from my_python import expect
import pexpect
import sys

TEST_CREDS_DICT = {
    'hostname': 'hostname',
    'username': 'username',
    'password': 'password',
}


def print_caplog(x):
    print('\nCAPLOG:')
    for line in x.messages:
        print('\t' + line)


def test_new_school(caplog):
    caplog.set_level(0)  # Everything
    # using only expect.SpawnSSH methods, make it ssh to username@hostname, provide password, then run uname
    spawn = expect.SpawnSSH(**TEST_CREDS_DICT)
    # wait for a prompt
    banner = list(spawn.banner)
    pprint.pprint(banner)
    assert banner[0].startswith('Welcome to Ubuntu 20.04.5')

    spawn.sendline('uname -a')
    spawn.expect(spawn.prompt, timeout=1)
    spawn.sendline('echo $?')
    spawn.expect(spawn.prompt, timeout=1)
    spawn.sendline('exit')
    spawn.expect(pexpect.exceptions.EOF, timeout=1)
    print_caplog(caplog)


class PexpectSpawnWrapper:


    def __init__(self, *args, meta_varname='spawn', **kw):
        self.meta_varname = meta_varname
        logging.debug('import pexpect')
        # logging.debug(f"spawn = pexpect.spawn({','.join([repr(a) for a in args])},{', '.join([f' {k}={repr(v)}' for k,v in kwargs.items()])})")
        logging.debug(f"spawn = pexpect.spawn({repr_args(args)},{repr_kw(kw)})")
        self.spawn = pexpect.spawn('ssh username@hostname', timeout=-1)


    @property
    def before(self):
        before = self.spawn.before
        logging.debug(f'before: {before}')
        return before

    def expect(self, *args, **kw):
        #logging.debug(f"ndx = spawn.expect({','.join([repr(a) for a in args])},{', '.join([f' {k}={repr(v)}' for k, v in kwargs.items()])})")
        logging.debug(f"ndx = spawn.expect({repr_args_kw(args, kw)})")
        ndx = self.spawn.expect(*args, **kw)
        logging.debug(f'   ndx: {ndx}')
        return ndx

    def sendline(self, *args, **kwargs):
        logging.debug(f'sendline: {args}  {kwargs}')
        return self.spawn.sendline(*args, **kwargs)


def test_old_school(caplog):
    caplog.set_level(0)  # Everything
    # using only pexpect commands in a script here, make it ssh to username@hostname, provide password, then run uname
    spawn = pexpect.spawn('ssh username@hostname')

    pattern = [
        f"\rusername@hostname's password: ",
        pexpect.exceptions.TIMEOUT,
    ]
    ndx = spawn.expect(pattern=pattern, timeout=3)
    if ndx == 0:
        spawn.sendline('password')
        spawn.expect('\r\n', timeout=1)
    ndx = spawn.expect(pattern=pattern, timeout=1)
    if ndx == 1:
        raw_text = spawn.before.decode(encoding='utf-8')
        lines = raw_text.split('\r\n')
        welcome_to_ubuntu = '\r\n'.join(lines[:-2])
        assert welcome_to_ubuntu.startswith('Welcome to Ubuntu 20.04.5')
        prompt = '\r\n' + lines[-1]
        escaped_prompt = prompt.replace('$', '\\$')
    else:
        logging.debug(f'NDX: {ndx}')
        return

    spawn.sendline('uname -a')
    spawn.expect(escaped_prompt, timeout=1)

    spawn.sendline('echo $?')
    spawn.expect(escaped_prompt, timeout=1)
    assert spawn.before == b'uname -a\r\nLinux u20045 5.4.0-137-generic #154-Ubuntu SMP Thu Jan 5 17:03:22 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux'

    spawn.sendline('exit')
    spawn.expect(pexpect.exceptions.EOF, timeout=1)
    assert spawn.before == b'echo $?\r\n0\r\nusername@u20045:~$ exit\r\nlogout\r\nConnection to hostname closed.\r\r\n'
    print_caplog(caplog)
