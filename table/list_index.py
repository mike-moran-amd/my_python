#!python3
# encoding=UTF-8
"""
Bucketizes items in a list

>>> lit = ListIndexTable.from_list(list('cabcbc'))
>>> for line in lit.pf('').split(NL):
...     print(repr(line))
'  | LIST_INDEX'
'c | [0, 3, 5] '
'a | [1]       '
'b | [2, 4]    '

>>> lit.list_index_from_row('b')
[2, 4]
"""
import enum
import table


NL = '\n'


class Columns(enum.Enum):
    LIST_INDEX = 'LIST_INDEX'


class ListIndexTable(table.Table):
    @classmethod
    def from_list(cls, from_list: list):
        t = cls()
        counter = -1
        for item in from_list:
            counter += 1
            val = t.get_val(item, Columns.LIST_INDEX.value)
            if val is None:
                # first time to see this value
                t.set_val(item, Columns.LIST_INDEX.value, [counter])
            else:
                # have seen this value
                val.append(counter)
        return t

    def list_index_from_row(self, row):
        val = self.get_val(row, Columns.LIST_INDEX.value)
        return val
