#!python3
# encoding=UTF-8
import pathlib
import random
import table

NL = '\n'


class IndexTable(table.Table):
    """
    "bucketizes" the items in a list.
    This pattern is frequently used
    """
    @classmethod
    def from_list(cls, l: list):
        """
        >>> it = IndexTable.from_list(list('abbccc'))
        >>> for item in it.row_gen():
        ...     print(item, it.get_val(item, 'INDEXES'))
        a [0]
        b [1, 2]
        c [3, 4, 5]

        """
        t = cls()
        counter = -1
        for item in l:
            counter += 1
            val = t.get_val(item, 'INDEXES')
            if val is None:
                t.set_val(item, 'INDEXES', [counter])
            else:
                val.append(counter)
        return t
