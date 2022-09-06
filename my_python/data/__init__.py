import pathlib
import re
from my_python import table, lib

NL = '\n'


class SessionTable(table.Table):
    @classmethod
    def from_text(cls, text):
        #pattern = '(.+?) +\((.+?), +(.+?)\)'
        # "^.+?@.+?:.+?# .+\n.*"gm
        # root@mm36:~# lscpu
        st = cls()
        for tup in re.findall('^(.+?)@(.+?):(.+?)# (.+$)', text):
            st.set_val('row', 'tup', tup)
            #st.set_val('row', 'hostname', hostname)
            #st.set_val('row', 'cwd', cwd)
            #st.set_val('row', 'command_response', command_response)
        return st



def path_gen(
        rglob_pattern='*',
        path=pathlib.Path(__file__).parent,
        is_file=True,
        is_dir=True):
    """
    generate paths from (default here)

    >>> len(list(path_gen()))
    75
    """
    for path in path.rglob(rglob_pattern):
        if is_file and path.is_file() or is_dir and path.is_dir():
            yield path


def text_from(file, path=pathlib.Path(__file__).parent):
    """
    return a string read from the given file path

    #>>> len(string_from(__file__))  # this file's signature 9-)
    4669
    """
    if path is not None:
        file = pathlib.Path(path, file)
    with open(file, "r", encoding='UTF-8') as fp:
        return fp.read()


TEXT_BEFORE_PROMPT = '''Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

'''


def find_prompt(text, bbp=TEXT_BEFORE_PROMPT):
    ss = text.split(bbp)
    if len(ss) == 2:
        if ss[1].startswith('root@'):
            ndx = ss[1].index(':')
            if ndx != -1:
                prompt = ss[1][:ndx + 1]
                return prompt


class SessionData:
    def __init__(self, text, prompt=None):
        """
        #>>> SessionData(text_from('mm18')).prompt
        'root@mm18:'
        """
        self.prompt = prompt or find_prompt(text)
        if not self.prompt:
            raise ValueError(f"UNABLE TO FIND PROMPT {self.prompt} IN TEXT")
        self.blocks = text.split(self.prompt)

    def get_text(self):
        ret = ""
        for block in self.blocks:
            ret += block
        return self.prompt.join(self.blocks)

    def session_table(self):
        """
        >>> st = SessionData(text_from('mm18')).session_table()
        >>> print(st.pf(title='block', cols=['cwd', 'command', 'count']))  # omit "lines" (its huge)
        block | cwd | command                                         | count
            1 | ~   | uname -a                                        |     2
            2 | ~   | apt install hwloc                               |    91
            3 | ~   | lstopo-no-graphics --no-io --no-legend --of txt |    43
            4 | ~   | lstopo                                          |   123
            5 | ~   | cat /proc/cpuinfo                               |  1297
            6 | ~   | cat /proc/meminfo                               |    54
        """
        st = table.Table()
        counter = -1
        for block in self.blocks:
            counter += 1
            if counter == 0:
                continue  # this block before the first command prompt is ssh handshake
            block_lines = block.split('\n')
            first_line = block_lines[0]
            # st.set_val(counter, 'first line', first_line)
            ss = first_line.split('#')
            if len(ss) == 1 or not ss[1].startswith(' '):
                continue  # empty command blocks, resets, end of session
            cwd = ss[0]
            st.set_val(counter, 'cwd', cwd)
            command = ss[1][1:]
            st.set_val(counter, 'command', command)
            lines = block_lines[1:]
            st.set_val(counter, 'count', len(lines))
            st.set_val(counter, 'lines', lines)

        return st


def save_text(file, text, path=pathlib.Path(__file__).parent, rename_old=True):
    if path is not None:
        file = pathlib.Path(path, file)
    if rename_old and file.exists():
        old_text = text_from(file, path)
        if old_text == text:
            return
        # rename to a unique timestamp filename in the same directory
        new_path = pathlib.Path(path, file.name + '_' + lib.dt_str()[:12])
        file.rename(new_path)
    with open(file, 'w') as fp:
        fp.write(text)


class Content:
    """
    >>> c = Content(__file__, path=None)

    #>>> len(c.content)
    5701
    """
    def __init__(self,
                 name,  # if this is an absolute or relative path then pass path=None below
                 path=pathlib.Path(__file__).parent,  # this file's directory is the default path if not passed
                 default=None,  # default {path/}file content
                 ):
        self.path = pathlib.Path(name) if path is None else pathlib.Path(path, name)
        self.content = default or self.pull()

    def exists(self):
        return self.path.exists()

    def pull(self):
        try:
            with open(self.path, "r", encoding='UTF-8') as fp:
                return fp.read()
        except FileNotFoundError:
            return None

    def push(self, content, rename_old=True):
        """
        #>>> c = Content("BOGUS")
        #>>> c.push("Howdy")
        """
        if rename_old and self.exists():
            old_content = self.pull()
            if old_content == content:
                return
            # rename to a unique timestamp filename in the same directory
            old_name = self.path.name
            new_name = old_name + '_' + lib.dt_str()[:12]
            new_path = pathlib.Path(self.path.parent, new_name)
            self.path.rename(new_path)
        with open(self.path, 'w') as fp:
            fp.write(content)
        self.content = content
        return self
