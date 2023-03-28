import io
import logging
from my_python import expect
import pexpect
import sys

TEST_CREDS = expect.Creds(hostname='hostname', username='username', password='password')


def print_caplog(x):
    print('\nCAPLOG:')
    for line in x.messages:
        print('\t' + line)


def test_old_school(caplog):
    # using only pexpect commands in a script here, make it ssh to username@hostname, provide password, then run uname
    spawn = pexpect.spawn('ssh username@hostname', timeout=-1)

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


def test_creds_spawn_uname(caplog):
    caplog.set_level(0)  # Everything
    spawn = TEST_CREDS.spawn('uname -a')
    spawn.expect(pattern=[expect.EOF], timeout=3)
    print_caplog(caplog)
    assert expect.EOF == spawn.match
    assert 0 == spawn.get_status()
    print('\n' + spawn.before)


def test_creds_spawn_ssh(caplog):
    caplog.set_level(0)  # Everything
    spawn = TEST_CREDS.spawn_ssh()
    spawn.sendline('echo Hello')
    ndx = spawn.expect(pattern=[expect.TIMEOUT, 'echo Hello'],  timeout=3)
    assert ndx == 1
    assert 0 == spawn.get_status()


def test_pexpect_spawn_ssh__echo_text(caplog):
    caplog.set_level(0)  # Everything
    echo_text = 'Hello world!'
    child = TEST_CREDS.spawn_ssh(command=f'echo "{echo_text}"')
    result = child.read()
    child.close()
    assert child.signal_status() is None
    assert child.status() == 0
    assert result == f'{echo_text}'
    pass


def test_pexpect_spawn_ssh__fails_mkdir_etc():
    child = TEST_CREDS.spawn_ssh(command='mkdir /etc')
    result = child.read()
    child.close()
    assert child.signal_status() is None
    assert child.status() == 256
    assert result == 'mkdir: cannot create directory ‘/etc’: File exists'
    pass


def test_pexpect_spawn_ssh__timeout():
    timeout = 5
    try:
        TEST_CREDS.spawn_ssh(command=f'sleep {timeout}', timeout=timeout - 1)
        raise RuntimeError('EXPECTED EXCEPTION')
    except exceptions.TIMEOUT:
        pass


def test_pexpect_spawn__uname(caplog):
    caplog.set_level(level=0)  # Everything
    child = TEST_CREDS.pexpect_spawn(f'ssh {TEST_CREDS.user_at_host()} uname -a')
    child.expect()
    result = child.read()
    child.close()
    print('\ntest_pexpect_spawn__uname')
    for log in caplog.messages:
        print('\t' + log)
    assert child.signal_status() is None
    assert child.status() == 0
    assert result == 'Linux test-ubuntu 5.4.0-136-generic #153-Ubuntu SMP Thu Nov 24 15:56:58 UTC 2022 x86_64 x86_64 x86_64 GNU/Linux'  # noqa


def test_uname(caplog):
    caplog.set_level(level=0)  # Everything
    result = TEST_CREDS.uname()
    print(f'\n{repr(result)}')
    print_caplog(caplog)
