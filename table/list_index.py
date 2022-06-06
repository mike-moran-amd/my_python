#!python3
# encoding=UTF-8
import table


INDEX_COL_LABEL = 'NDX_LIST'
NL = '\n'


class ListIndexTable(table.Table):
    @classmethod
    def from_list(cls, from_list: list, index_col_label=INDEX_COL_LABEL):
        """
        "bucketizes" the items in a list and returns a table

        >>> for line in ListIndexTable.from_list(list('cabcbc')).pf('').split(NL):  # noqa
        ...     print(repr(line))
        '  | NDX_LIST '
        'c | [0, 3, 5]'
        'a | [1]      '
        'b | [2, 4]   '
        """
        t = cls()
        counter = -1
        for item in from_list:
            counter += 1
            val = t.get_val(item, index_col_label)
            if val is None:
                # first time to see this value
                t.set_val(item, index_col_label, [counter])
            else:
                # have seen this value
                val.append(counter)
        return t

    def ndx_from_row(self,
                     row,
                     index_col_label=INDEX_COL_LABEL):
        """
        >>> ListIndexTable.from_list(list('cabcbc')).ndx_from_row('b')  # noqa
        [2, 4]
        """
        val = self.get_val(row, index_col_label)
        return val
