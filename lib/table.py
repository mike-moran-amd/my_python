#!/usr/bin/python
# encoding=UTF-8
from collections import OrderedDict


class Table:
    """
    >>> t = Table([('row', 'col', 'val')])
    >>> list(t.tup_gen())
    [('row', 'col', 'val')]
    >>> list(t.tup_gen(title='mt'))
    [(0, 0, 'mt'), (0, 1, 'col'), (1, 0, 'row'), (1, 1, 'val')]
    >>> t.pformat()
    'val'
    >>> mt = Table(t.tup_gen(title='mt'))
    >>> print(mt.pformat())
    mt  | col
    row | val
    >>> print(mt.pformat(title='mmt'))
    mmt |   0 |   1
      0 | mt  | col
      1 | row | val
    >>> mmt = Table(mt.tup_gen(title='mmt'))
    >>> print(mmt.pformat())
    mmt |   0 |   1
      0 | mt  | col
      1 | row | val
    """

    def __init__(self, tups):
        """
        Create a new Table with the given tuple list
        :param tups: list(tuple(row, col, val)) - can be empty or sparse
        """
        self.__od = OrderedDict()
        for tup in tups:
            row, col, val = tup
            self.__od[row, col] = val

    def row_gen(self):
        seen = []
        for key in self.__od.keys():
            row, col = key
            if row not in seen:
                yield row
                seen.append(row)

    def col_gen(self):
        seen = []
        for key in self.__od.keys():
            row, col = key
            if col not in seen:
                yield col
                seen.append(col)

    def get_val(self, row, col):
        return self.__od.get((row, col), None)

    def set_val(self, row, col, val):
        self.__od[row, col] = val

    def tup_gen(self, rows=None, cols=None, title=None):
        rows = rows or list(self.row_gen())
        cols = cols or list(self.col_gen())

        if title is not None:
            yield 0, 0, title
            col_ndx = 1
            for col in cols:
                yield 0, col_ndx, col
                col_ndx += 1
        row_ndx = 1
        for row in rows:
            if title is not None:
                yield row_ndx, 0, row
            col_ndx = 1
            for col in cols:
                val = self.get_val(row, col)
                if title is not None:
                    yield row_ndx, col_ndx, val
                else:
                    yield row, col, val
                col_ndx += 1
            row_ndx += 1

    def col_widths(self, cols_mask):
        ret_dict = {}
        for k, val in self.__od.items():
            row, col = k
            if not cols_mask or col in cols_mask:
                try:
                    width = ret_dict[col]
                except KeyError:
                    width = 0
                ret_dict[col] = max(width, len(str(val)))
        return ret_dict

    def pformat(self, csep=' | ', rsep='\n', rows=None, cols=None, title=None):
        t = self if title is None else Table(self.tup_gen(rows=rows, cols=cols, title=title))
        widths = t.col_widths(cols)
        rows = []
        for row in t.row_gen():
            cols = []
            for col in t.col_gen():
                val = t.get_val(row, col)
                # left justify strings, numbers to the right
                cell = f'{val:{widths[col]}}'
                # TODO: add heights - left for future programmer
                cols.append(cell)
            rows.append(csep.join(cols))
        return rsep.join(rows)
