from table import expect
from pexpect import exceptions

TEST_CREDS = expect.Creds(hostname='HOSTNAME', username='USERNAME', password='PASSWORD')


def test__pexpect_spawn_ssh__echo_text():
    echo_text = 'Hello world!'
    result, child = expect.pexpect_spawn_ssh(creds=TEST_CREDS, command=f'echo {echo_text}')
    assert child.signalstatus is None
    assert child.status == 0
    assert result == bytes(f' \r\n{echo_text}\r\n', encoding='utf-8')


def test__pexpect_spawn_ssh__fails_mkdir_etc():
    result, child = expect.pexpect_spawn_ssh(creds=TEST_CREDS, command='mkdir /etc')
    assert child.signalstatus is None
    assert child.status == 256
    assert result == b' \r\nmkdir: cannot create directory \xe2\x80\x98/etc\xe2\x80\x99: File exists\r\n'


def test__pexpect_spawn_ssh__timeout():
    timeout = 3
    try:
        result, child = expect.pexpect_spawn_ssh(creds=TEST_CREDS, command=f'sleep {timeout}', timeout=timeout - 1)
        raise RuntimeError('EXPECTED EXCEPTION')
    except exceptions.TIMEOUT as exc:
        pass

