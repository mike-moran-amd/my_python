import io
import pexpect

HOSTNAME = 'hostname'
USERNAME = 'username'
PASSWORD = 'password'


def test_test(caplog):
    command = f'ssh {USERNAME}@{HOSTNAME} sudo mkdir /opt/my_python'
    log_io = io.StringIO()
    child = pexpect.spawn(command=command, timeout=3, encoding='utf-8')
    child.logfile_read = log_io
    if child.expect([pexpect.EOF, "username@hostname's password: "], timeout=1):
        child.sendline(f'{PASSWORD}\r')
    pass


