#!python3
# encoding=UTF-8
from table import list_index


NL = '\n'


class CharIndexTable(list_index.ListIndexTable):
    @classmethod
    def from_string(cls, s: str):
        """
        >>> for line in CharIndexTable.from_string('cabcbc').pf('').split(NL):
        ...     print(repr(line))
        '  | ORD | NDX_LIST '
        'c |  99 | [0, 3, 5]'
        'a |  97 | [1]      '
        'b |  98 | [2, 4]   '
        """
        lit = list_index.ListIndexTable.from_list(list(s))
        t = cls()
        for row in lit.row_gen():
            # This forces the column order of the final table, not required, but is a good example.
            t.set_val(row, 'ORD', ord(row))
        t.extend(lit.tup_gen())
        return t

