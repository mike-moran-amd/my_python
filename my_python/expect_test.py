from my_python import expect
from pexpect import exceptions

TEST_CREDS = expect.Creds(hostname='hostname', username='username', password='password')


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


def print_caplog(x):
    print('\nCAPLOG:')
    for log in x.messages:
        print('\t' + log)
