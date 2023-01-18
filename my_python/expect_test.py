from my_python import expect
from pexpect import exceptions

TEST_CREDS = expect.Creds(hostname='HOSTNAME', username='USERNAME', password='PASSWORD')


def test__pexpect_spawn_ssh__echo_text():
    echo_text = 'Hello world!'
    child = TEST_CREDS.spawn_ssh(command=f'echo {echo_text}')
    result = child.read()
    child.close()
    assert child.signalstatus is None
    assert child.status == 0
    assert result == f' \r\n{echo_text}\r\n'
    pass


def test__pexpect_spawn_ssh__fails_mkdir_etc():
    child = TEST_CREDS.spawn_ssh(command='mkdir /etc')
    result = child.read()
    child.close()
    assert child.signalstatus is None
    assert child.status == 256
    assert result == b' \r\nmkdir: cannot create directory \xe2\x80\x98/etc\xe2\x80\x99: File exists\r\n'
    pass


def test__pexpect_spawn_ssh__timeout():
    timeout = 3
    try:
        _ = TEST_CREDS.spawn_ssh(command=f'sleep {timeout}', timeout=timeout - 1)
        raise RuntimeError('EXPECTED EXCEPTION')
    except exceptions.TIMEOUT:
        pass
