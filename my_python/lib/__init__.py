#!python3
# encoding=UTF-8
import datetime
import shutil
import subprocess


def dt_str(dt=None):
    """
    Creates a timestamp that is sorta readable but uniquely sortable
    :param dt: datetime or None (default) to use now()
    :return: 18 character string with 2 digits (zero filled) for year, month, day, ..., and 6 for the microsecond

    EXAMPLE:
    >>> dt_str(datetime.datetime(2022, 3, 24, 19, 23, 0, 123456))
    '220324192300123456'

    """
    dt = dt or datetime.datetime.now()
    return '%0.2d' * 6 % (dt.year % 100, dt.month, dt.day, dt.hour, dt.minute, dt.second) + '%0.6d' % dt.microsecond


def path_for_command(word):
    """
    This is called "which" or "where" on windows
    :param word: word
    :return: path or None

    EXAMPLE:
    >>> path_for_command('vboxmanage')  # noqa
    '/usr/local/bin/vboxmanage'

    """
    try:
        return shutil.which(word)
    except:  # noqa
        # TODO fix for windows, "where", or "Get-Command"
        # https://www.shellhacks.com/windows-which-equivalent-cmd-powershell/
        raise


def invoke_subprocess(word_list, encoding='UTF-8'):
    """
    Call a subprocess and return the decoded bytes

    EXMPLE:
    >>> invoke_subprocess([path_for_command('vboxmanage'), '--version']).strip()  # noqa
    '6.1.32r149290'

    """
    # TODO where do we get stderr (below)?
    raw_bytes = subprocess.check_output(word_list, stderr=subprocess.PIPE)
    return raw_bytes.decode(encoding=encoding)
