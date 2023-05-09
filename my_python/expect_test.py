import logging
from my_python import expect

HOSTNAME = 'hostname'
USERNAME = 'username'
PASSWORD = 'password'

TEST_CREDS_DICT = {
    'hostname': HOSTNAME,
    'username': USERNAME,
    'password': PASSWORD,
}


def print_caplog(x, startswith=''):
    print('\nCAPLOG:')
    for line in x.messages:
        if startswith and not line.startswith(startswith):
            continue
        print(' '*4 + line)


def test_spawn_pipe_redirect_example(caplog):
    caplog.set_level(0)  # capture all log messages

    spawn = expect.Spawn('bash -c "ls -l | grep LOG > /dev/null"')
    spawn.expect(expect.EOF)
    assert spawn.get_status() == 256  # nothing from grep return code

    spawn = expect.Spawn('bash -c "ls -l | grep log > /dev/null"')
    spawn.expect(expect.EOF)
    assert spawn.get_status() == 0  # log.py matches

    print_caplog(caplog)


def test_spawn_uname(caplog):
    caplog.set_level(0)  # capture all log messages
    spawn = expect.Spawn('uname -a')
    assert repr(spawn) == 'pexpect.spawn((\'uname -a\',), )'
    spawn.expect(expect.EOF)
    lines = spawn.get_before_lines()
    assert len(lines) == 2
    status = spawn.get_status()
    assert status == 0
    print_caplog(caplog, 'SPAWN')


def test_expect_spawn_bash(caplog):
    caplog.set_level(0)  # Everything
    spawn = expect.Spawn('bash')
    repr_spawn = repr(spawn)
    assert repr_spawn == 'pexpect.spawn((\'bash\',), )'
    print_caplog(caplog)


def test_run_command(caplog):
    caplog.set_level(0)  # Everything
    spawn = expect.SpawnSSH(**TEST_CREDS_DICT)
    result, error = spawn.result_status_from_command('uname -a')
    # assert result == 'Linux u20045 5.4.0-137-generic #154-Ubuntu SMP Thu Jan 5 17:03:22 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux\n'  # noqa
    assert result == 'Linux u20045 5.4.0-146-generic #163-Ubuntu SMP Fri Mar 17 18:26:02 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux\n'  # noqa
    assert error == '0'
    print_caplog(caplog)  # , startswith='self.before: ')


def test_spawn_bash(caplog):
    caplog.set_level(0)  # Everything
    spawn = expect.SpawnBash(**expect.LOCAL_CREDS)
    spawn.sendline('uname -a')
    spawn.expect(spawn.prompt, timeout=1)
    uname = spawn.get_before_lines()[1]
    assert uname.startswith('Linux ')
    assert uname.index('-Ubuntu') != -1
    # assert spawn.get_before_lines()[1] == 'Linux mm 5.4.0-144-generic #161-Ubuntu SMP Fri Feb 3 14:49:04 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux'
    spawn.sendline('whoami')
    spawn.expect(spawn.prompt, timeout=1)
    assert spawn.get_before_lines()[1] == TEST_CREDS_DICT["username"]
    print_caplog(caplog)  # , startswith='self.before: ')
    # TODO self.before ?= b'6.08s - pydevd: Sending message related to process being replaced timed-out after 5 seconds\r\n'


def test_run_logged_line_with_expected_results(caplog):
    caplog.set_level(0)  # Everything
    spawn = expect.SpawnSSH(**TEST_CREDS_DICT)
    lines = spawn.get_before_lines()

    spawn.sendline('uname -a')
    ndx = spawn.expect([spawn.prompt, expect.TIMEOUT], timeout=2)
    lines = spawn.get_before_lines()

    sudo_password_pattern = f' password for {TEST_CREDS_DICT["username"]}: '
    spawn.sendline('sudo bash')
    ndx = spawn.expect([sudo_password_pattern, expect.TIMEOUT], timeout=1)
    if ndx == 0:
        spawn.sendline(TEST_CREDS_DICT["password"])
    lines = spawn.get_before_lines()

    print_caplog(caplog)  # , startswith='spawn = pexpect.spawn(')


def test_enable_passwordless_sudo(caplog):
    caplog.set_level(0)  # Everything
    hostname = TEST_CREDS_DICT['hostname']
    username = TEST_CREDS_DICT['username']
    password = TEST_CREDS_DICT['password']

    spawn = expect.SpawnSSH(hostname=hostname, username=username, password=password)
    spawn.sendline('sudo -S bash')
    ndx = spawn.expect([f'password for {username}: ', expect.TIMEOUT], timeout=1)
    if ndx == 0:
        spawn.sendline(f'{password}')
        spawn.expect(expect.TIMEOUT, timeout=2)
    else:
        pass
    spawn.sendline(f'echo "{username}  ALL=(ALL:ALL) NOPASSWD:ALL" >> /etc/sudoers')
    spawn.expect(expect.TIMEOUT, timeout=2)
    spawn.sendline('exit')
    spawn.expect(expect.TIMEOUT, timeout=2)
    spawn.sendline('exit')
    spawn.expect(expect.EOF, timeout=1)
    print_caplog(caplog)


def test_expect_spawn_ssh(caplog):
    caplog.set_level(0)  # Everything
    # using only expect.SpawnSSH methods, make it ssh to username@hostname, provide password, then run uname
    spawn = expect.SpawnSSH(**TEST_CREDS_DICT)
    spawn.sendline('uname -a')
    spawn.expect(spawn.prompt, timeout=1)
    spawn.sendline('echo $?')
    spawn.expect(spawn.prompt, timeout=1)
    spawn.sendline('exit')
    spawn.expect(expect.EOF, timeout=1)
    print_caplog(caplog)


def test_pexpect_spawn_ssh(caplog):
    import pexpect
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
    assert spawn.before == b'uname -a\r\nLinux u20045 5.4.0-137-generic #154-Ubuntu SMP Thu Jan 5 17:03:22 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux'  # noqa

    spawn.sendline('exit')
    spawn.expect(pexpect.exceptions.EOF, timeout=1)
    assert spawn.before == b'echo $?\r\n0\r\nusername@u20045:~$ exit\r\nlogout\r\nConnection to hostname closed.\r\r\n'
    print_caplog(caplog)



BEFORE = '''@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

@       WARNING: POSSIBLE DNS SPOOFING DETECTED!          @

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

The ECDSA host key for hostname has changed,

and the key for the corresponding IP address 10.0.1.10

is unknown. This could either mean that

DNS SPOOFING is happening or the IP address for the host

and its host key have changed at the same time.

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!

Someone could be eavesdropping on you right now (man-in-the-middle attack)!

It is also possible that a host key has just been changed.

The fingerprint for the ECDSA key sent by the remote host is
SHA256:qEUuq22o4TcnqUqVRhUKL/vhx8pSb1LSGZS/AudZxn4.

Please contact your system administrator.

Add correct host key in /Users/mfm/.ssh/known_hosts to get rid of this message.

Offending ECDSA key in /Users/mfm/.ssh/known_hosts:1

ECDSA host key for hostname has changed and you have requested strict checking.'''


def test_cred_spawn_ssh(caplog):
    caplog.set_level(0)
    spawn_ssh = expect.CredSpawn("ssh username@hostname", **TEST_CREDS_DICT)
    # Here the prompt must be waiting for input...
    spawn_ssh.expect([expect.TIMEOUT], timeout=1)
    banner = spawn_ssh.get_before_lines()

    # lines = spawn_ssh.get_before_lines()
    prompt = spawn_ssh.get_prompt()
    spawn_ssh.expect(prompt, timeout=1)
    spawn_ssh.sendline('uname -a')
    spawn_ssh.expect(prompt, timeout=1)
    lines = spawn_ssh.get_before_lines()
    assert lines == [
        'uname -a',
        'Linux u20045 5.4.0-146-generic #163-Ubuntu SMP Fri Mar 17 18:26:02 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux',
        '']
    logging.debug('SpawnSSH READY')
    print_caplog(caplog)


def test_cred_spawn_bash(caplog):
    caplog.set_level(0)
    bash = expect.CredSpawn('bash', password=TEST_CREDS_DICT['password'])
    prompt = bash.get_prompt()
    bash.sendline('uname -a')
    bash.expect(prompt, timeout=1)
    bash.sendline('exit')
    bash.expect(expect.EOF, timeout=1)
    status = bash.get_status()
    assert status == 0
    print_caplog(caplog)


def test_cred_spawn_bash_lscpu(caplog):
    caplog.set_level(0)
    bash = expect.CredSpawn('bash', password=TEST_CREDS_DICT['password'])
    prompt = bash.get_prompt()
    bash.sendline('lscpu')
    bash.expect(prompt, timeout=1)
    bash.sendline('exit')
    bash.expect(expect.EOF, timeout=1)
    status = bash.get_status()
    assert status == 0
    print_caplog(caplog)
