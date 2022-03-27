#!python3
# encoding=UTF-8
"""


"""
import re
import shutil
import subprocess
import lib


NL = '\n'  # doctests hate newlines in the source


class Vagrant:
    def __init__(self):
        """
        #>>> for k, v in vars(Vagrant()).items():
        ...     print(repr(k), '=', repr(v))
        '_Vagrant__which' = '/usr/local/bin/vagrant'
        '_Vagrant__version' = 'Installed Version: 2.2.19'

        """
        self.__which = shutil.which("vagrant")
        if not self.__which:
            # It is good to know this before hand, yes?
            raise RuntimeError("Which vagrant?")
        self.__version = self.invoke(['version']).split('\n')[0]

    def global_status_table(self):
        """
        #>>> for line in Vagrant().global_status_table().pf(title='STATUS').split(NL):
        ...     print(repr(line))
        'STATUS | id      | name    | provider   | state   | directory                  '
        '     1 | 2d9d7d5 | default | virtualbox | running | /Users/mfm/vagrant         '
        '     2 | fe8bcba | default | virtualbox | running | /Users/mfm/vagrant/U2010   '
        '     3 | ea0bb41 | default | virtualbox | running | /Users/mfm/vagrant/C8S     '
        '     4 | d11e797 | default | virtualbox | running | /Users/mfm/vagrant/centos/8'
        '     5 | a4d9a67 | default | virtualbox | running | /Users/mfm/vagrant/centos  '
        '     6 | b25e420 | default | virtualbox | running | /Users/mfm/vagrant/centos8 '
        """
        ss = self.invoke(['global-status']).split('\n \n')
        # the first part is a table frame to decode
        return lib.Table.from_frame(ss[0])

    def invoke(self, args_list):
        """
        #>>> for line in Vagrant().invoke(['global-status']).split(NL):
        ...     print(repr(line))
        'id       name    provider   state   directory                           '
        '------------------------------------------------------------------------'
        '2d9d7d5  default virtualbox running /Users/mfm/vagrant                  '
        'fe8bcba  default virtualbox running /Users/mfm/vagrant/U2010            '
        'ea0bb41  default virtualbox running /Users/mfm/vagrant/C8S              '
        'd11e797  default virtualbox running /Users/mfm/vagrant/centos/8         '
        'a4d9a67  default virtualbox running /Users/mfm/vagrant/centos           '
        'b25e420  default virtualbox running /Users/mfm/vagrant/centos8          '
        ' '
        'The above shows information about all known Vagrant environments'
        'on this machine. This data is cached and may not be completely'
        'up-to-date (use "vagrant global-status --prune" to prune invalid'
        'entries). To interact with any of the machines, you can go to that'
        'directory and run Vagrant, or you can use the ID directly with'
        'Vagrant commands from any directory. For example:'
        '"vagrant destroy 1a2b3c4d"'
        ''
        """
        command_list = [self.__which]
        command_list.extend(args_list)
        raw_bytes = subprocess.check_output(command_list)
        return raw_bytes.decode(encoding='UTF-8')

    def box_list_table(self):
        """

        #>>> for line in Vagrant().box_list_table().pf(title='box list').split(NL):
        ...     print(repr(line))
        'box list | name               | provider   | version'
        '       1 | generic/centos8    | virtualbox | 3.6.8  '
        '       2 | generic/ubuntu2004 | virtualbox | 3.6.8  '
        '       3 | generic/ubuntu2010 | virtualbox | 3.6.8  '
        """
        output = self.invoke(['box', 'list'])
        t = lib.Table([])
        row_ndx = 0
        for name, provider, version in re.findall('(.+?) +\((.+?), +(.+?)\)', output):
            row_ndx += 1
            t.set_val(row_ndx, 'name', name)
            t.set_val(row_ndx, 'provider', provider)
            t.set_val(row_ndx, 'version', version)

        return t
