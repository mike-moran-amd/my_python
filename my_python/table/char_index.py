#!python3
# encoding=UTF-8
"""
Similar to a list_index, a string is a list, so this is a table of characters and their properties

>>> cit = CharIndexTable.from_string('cabcbc')  # noqa
>>> for line in cit.pf('').split(NL):
...     print(repr(line))
'  | ORD | LIST_INDEX'
'c |  99 | [0, 3, 5] '
'a |  97 | [1]       '
'b |  98 | [2, 4]    '

>>> cit.ord_from_row('b')
98

"""
import enum
from my_python.table import list_index

NL = '\n'


class Columns(enum.Enum):
    ORD = 'ORD'


class CharIndexTable(list_index.ListIndexTable):

    @classmethod
    def from_string(cls, s: str):
        lit = list_index.ListIndexTable.from_list(list(s))
        t = cls()
        for row in lit.row_gen():
            # This forces the column order of the final table, not required, but is a good example.
            t.set_val(row, Columns.ORD.value, ord(row))
        t.extend(lit.tup_gen())
        return t

    def ord_from_row(self, row):
        val = self.get_val(row, Columns.ORD.value)
        return val
