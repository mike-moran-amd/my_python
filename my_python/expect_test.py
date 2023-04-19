import logging
import pprint
from my_python import expect

TEST_CREDS_DICT = {
    'hostname': 'hostname',
    'username': 'username',
    'password': 'password',
}


def test_run_command(caplog):
    caplog.set_level(0)  # Everything
    spawn = expect.SpawnSSH(**TEST_CREDS_DICT)
    result, error = spawn.result_status_from_command('uname -a')
    assert result == 'Linux u20045 5.4.0-137-generic #154-Ubuntu SMP Thu Jan 5 17:03:22 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux\n'  # noqa
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


def test_repr_x(caplog):
    caplog.set_level(0)  # Everything
    args_expected_tups = [
        (('ssh username@hostname',), 'ssh username@hostname'),
        # ('a string', '"a string"'),  # strings get double quoted
        # ("string with single 'quotes'", '"string with single \'quotes\'"'),  # single quotes are ignored
        # ('string with double "quotes"', 'string with double "quotes"'),  # embedded double quotes get escaped
        # (('string in parens is not a tuple'), '"string in parens is not a tuple"'),  # noqa - Remove Rednundant Parens
        # (('string in a tuple',), '"string in a tuple"'),  # the comma on the end forces a tuple of one thing
    ]
    table_tups = []
    row = -1
    for args, expected in args_expected_tups:
        row += 1
        table_tups.append((row, 'args', args))
        repr_x = expect.repr_x(args)
        table_tups.append((row, 'pf(args)', pprint.pformat(args)))
        table_tups.append((row, 'pf(repr_x(args))', pprint.pformat(repr_x)))
        table_tups.append((row, 'repr_x(args)', repr_x))
        table_tups.append((row, 'TEST', 'pass' if expected == repr_x else 'FAIL'))
        table_tups.append((row, 'expected', expected))
        table_tups.append((row, 'RESULT', pprint.pformat(repr_x) == pprint.pformat(args)))
    # t = table.Table(table_tups)
    print()
    # print(t.pf('row'))
    print_caplog(caplog)


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


def print_caplog(x, startswith=''):
    print('\nCAPLOG:')
    for line in x.messages:
        if startswith and not line.startswith(startswith):
            continue
        print('\t' + line)


def test_cred_spawn_ssh(caplog):
    caplog.set_level(0)
    spawn_ssh = expect.CredSpawn('ssh username@hostname', **TEST_CREDS_DICT)
    prompt = spawn_ssh.get_prompt()
    spawn_ssh.expect(prompt, timeout=1)
    spawn_ssh.sendline('uname -a')
    spawn_ssh.expect(prompt, timeout=1)
    logging.debug('SpawnSSH READY')
    print_caplog(caplog)
