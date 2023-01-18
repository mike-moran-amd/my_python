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
                  child_logfile=None,
                  child_logfile_read=None,
                  child_logfile_send=None,
                  timeout=30,
                  expect_timeout=2,
                  ):
        table_tups = []

        def append_table_tup(row):
            table_tups.append((row, 'before', child.before))
            table_tups.append((row, 'after', child.after))

        ssh_command = f'ssh {self.user_at_host()} {command}'
        child = pexpect.spawn(command=ssh_command, timeout=timeout)

        append_table_tup(ssh_command)

        # NEW CODE BELOW
        self_read = None
        try:
            child.expect(pattern=expect_challenge, timeout=expect_timeout)
            append_table_tup(expect_challenge)
            child.sendline(self.__password)
            append_table_tup('PASSWORD SENT')

        except EOF as exc:
            append_table_tup('EOF')
            self_read = child.before.decode(encoding=self.__encoding).strip()


        # NEW CODE ABOVE
        logging.log(logging.DEBUG, f'pexpect.spawn(command={repr(ssh_command)}, timeout={repr(timeout)}')
        return Child(child, self_read=self_read, encoding=self.__encoding), table_tups



        # make io available for progress watching
        child.logfile = child_logfile
        child.logfile_read = child_logfile_read
        child.logfile_send = child_logfile_send

        pattern = [
            pexpect.TIMEOUT,
            expect_challenge,
        ]
        logging.log(logging.DEBUG, f'pattern = {pattern}')

        try:
            expect_ndx = child.expect(pattern=pattern)
        except EOF as eof:
            # this happens when there is no challenge, likely the command succeeded because of ssh authorized_keys
            # caller can read() the result or interact with it
            print(f'EOF:\n{eof}')
            return Child(child, encoding=self.__encoding)
        logging.debug(f'expect_ndx = {expect_ndx}')

        if expect_ndx == 0:
            logging.log(logging.DEBUG, f'child = {child}')
        else:
            child.send(self.password_newline_bytes())
            logging.log(logging.DEBUG, f'SENT CREDS')
        # end with child, close() sets child exit/signal status
        return Child(child, encoding=self.__encoding)


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
