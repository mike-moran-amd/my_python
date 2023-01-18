import logging
import pexpect
from pexpect.exceptions import EOF

DEFAULT_ENCODING = 'utf-8'


class Creds:
    def __init__(self, hostname, username, password, encoding='utf-8'):
        self.__hostname = hostname
        self.__username = username
        self.__password = password
        self.__encoding = encoding

    def user_at_host(self):
        return self.__username + '@' + self.__hostname

    def password_newline_bytes(self):
        return f'{self.__password}\n'.encode(encoding=self.__encoding)

    def spawn_ssh(self,
                  command,
                  expect_challenge='password:',
                  timeout=30,
                  expect_timeout=2,
                  ):
        table_tuples = []

        def append_table_tup(row):
            table_tuples.append((row, 'before', child.before))
            table_tuples.append((row, 'after', child.after))

        ssh_command = f'ssh {self.user_at_host()} {command}'
        child = pexpect.spawn(command=ssh_command, timeout=timeout)
        append_table_tup(ssh_command)

        self_read = None
        try:
            child.expect(pattern=expect_challenge, timeout=expect_timeout)
            append_table_tup(expect_challenge)

            child.sendline(self.__password)
            append_table_tup('PASSWORD SENT')

        except EOF:
            append_table_tup('EOF')
            self_read = child.before.decode(encoding=self.__encoding).strip()

        logging.log(logging.DEBUG, f'pexpect.spawn(command={repr(ssh_command)}, timeout={repr(timeout)}')
        return Child(child, self_read=self_read, encoding=self.__encoding), table_tuples


class Child:
    def __init__(self, spawn_child, self_read=None, encoding='utf-8'):
        self.__spawn_child = spawn_child
        self.__encoding = encoding
        self.__self_read = self_read

    def read(self, size=-1):
        if self.__self_read is not None:
            ret = self.__self_read
            self.__self_read = None
            return ret

        result_bytes = self.__spawn_child.read(size=size)
        return result_bytes.decode(encoding=self.__encoding).strip()

    def close(self):
        self.__spawn_child.close()

    def is_closed(self):
        return self.__spawn_child.close

    def signal_status(self):
        return self.__spawn_child.signalstatus

    def status(self):
        return self.__spawn_child.status
