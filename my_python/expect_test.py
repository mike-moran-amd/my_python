from my_python import expect, table
from pexpect import exceptions

TEST_CREDS = expect.Creds(hostname='10.0.1.6', username='username', password='password')


def test__pexpect_spawn_ssh__echo_text():
    echo_text = 'Hello world!'
    child, table_tups = TEST_CREDS.spawn_ssh(command=f'echo "{echo_text}"')
    print(f'\n{table.Table(table_tups).pf("echo_text")}')
    result = child.read()
    child.close()
    assert child.signal_status() is None
    assert child.status() == 0
    assert result == f'{echo_text}'
    pass


def test__pexpect_spawn_ssh__fails_mkdir_etc():
    child, table_tups = TEST_CREDS.spawn_ssh(command='mkdir /etc')
    print(f'\n{table.Table(table_tups).pf("echo_text")}')
    result = child.read()
    child.close()
    assert child.signal_status() is None
    assert child.status() == 256
    assert result == 'mkdir: cannot create directory ‘/etc’: File exists'
    pass


def test__pexpect_spawn_ssh__timeout():
    timeout = 5
    try:
        _, table_tups = TEST_CREDS.spawn_ssh(command=f'sleep {timeout}', timeout=timeout - 1)
        print(f'\n{table.Table(table_tups).pf("echo_text")}')
        raise RuntimeError('EXPECTED EXCEPTION')
    except exceptions.TIMEOUT:
        pass
