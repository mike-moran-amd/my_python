"""
Interestingly there is no "table" module in the standard python library.
This is a good first stab at it.

DOCTEST EXAMPLES:

>>> t = Table([('row', 'col', 'val')])
>>> list(t.tup_gen())
[('row', 'col', 'val')]

>>> list(t.tup_gen(title='mt'))
[(0, 0, 'mt'), (0, 1, 'col'), (1, 0, 'row'), (1, 1, 'val')]

>>> print(t.pf())
val

>>> mt = Table(t.tup_gen(title='mt'))
>>> print(mt.pf())
mt  | col
row | val

>>> print(mt.pf(title='mmt'))
mmt |   0 |   1
  0 | mt  | col
  1 | row | val

>>> mmt = Table(mt.tup_gen(title='mmt'))
>>> print(mmt.pf())
mmt |   0 |   1
  0 | mt  | col
  1 | row | val

>>> a_frame_str = 'id       name    provider   state   directory                           ' + \
DEFAULT_ROW_SEP + '------------------------------------------------------------------------' + \
DEFAULT_ROW_SEP + '2d9d7d5  default virtualbox running /Users/mfm/vagrant                  ' + \
DEFAULT_ROW_SEP + 'fe8bcba  default virtualbox running /Users/mfm/vagrant/U2010            ' + \
DEFAULT_ROW_SEP + 'ea0bb41  default virtualbox running /Users/mfm/vagrant/C8S              ' + \
DEFAULT_ROW_SEP + 'd11e797  default virtualbox running /Users/mfm/vagrant/centos/8         ' + \
DEFAULT_ROW_SEP + 'a4d9a67  default virtualbox running /Users/mfm/vagrant/centos           ' + \
DEFAULT_ROW_SEP + 'b25e420  default virtualbox running /Users/mfm/vagrant/centos8          ' # noqa

>>> ft = Table.from_frame(a_frame_str)
>>> ft.print_repr_lines(title='BOXES')
'BOXES | id      | name    | provider   | state   | directory                  '
'    1 | 2d9d7d5 | default | virtualbox | running | /Users/mfm/vagrant         '
'    2 | fe8bcba | default | virtualbox | running | /Users/mfm/vagrant/U2010   '
'    3 | ea0bb41 | default | virtualbox | running | /Users/mfm/vagrant/C8S     '
'    4 | d11e797 | default | virtualbox | running | /Users/mfm/vagrant/centos/8'
'    5 | a4d9a67 | default | virtualbox | running | /Users/mfm/vagrant/centos  '
'    6 | b25e420 | default | virtualbox | running | /Users/mfm/vagrant/centos8 '

>>> dynamic_table, static_table = ft.split_static()
>>> dynamic_table.print_repr_lines('')
'  | id      | directory                  '
'1 | 2d9d7d5 | /Users/mfm/vagrant         '
'2 | fe8bcba | /Users/mfm/vagrant/U2010   '
'3 | ea0bb41 | /Users/mfm/vagrant/C8S     '
'4 | d11e797 | /Users/mfm/vagrant/centos/8'
'5 | a4d9a67 | /Users/mfm/vagrant/centos  '
'6 | b25e420 | /Users/mfm/vagrant/centos8 '

>>> static_table.print_repr_lines('')
'  | name    | provider   | state  '
'0 | default | virtualbox | running'

>>> dynamic_table.count_unique_col('id')
6

>>> static_table.count_unique_col('name')
1

"""
from collections import OrderedDict


DEFAULT_ROW_SEP = '\n'
DEFAULT_COL_SEP = ' | '


class Table:

    def __init__(self, tuple_list=()):
        """
        Create a new Table with the given tuple list
        :param tuple_list: list(tuple(row, col, val)) - can be empty or sparse
        """
        self.__od = OrderedDict()
        self.extend(tuple_list)

    def extend(self, tuple_list):
        for tup in tuple_list:
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

    def get_val(self, row, col, default=None):
        val = self.__od.get((row, col))
        if val is None:
            val = default
        return val

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

    def col_widths(self, cols_mask=()):
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

    def pf(self,
           title=None,
           column_separator=DEFAULT_COL_SEP,
           row_separator=DEFAULT_ROW_SEP,
           empty_cell='',  # default cell display if None
           rows=None,  # only valid with title
           cols=None,  # only valid with title
           ):
        t = self if title is None else Table(self.tup_gen(title=title, rows=rows, cols=cols))
        widths = t.col_widths()
        rows = []
        for row in t.row_gen():
            cols = []
            for col in t.col_gen():
                val = t.get_val(row, col, default=empty_cell)
                # left justify strings, numbers to the right
                try:
                    cell = f'{val:{widths[col]}}'
                except TypeError:
                    # val is not a builtin type, render as str
                    cell = f'{str(val):{widths[col]}}'
                cols.append(cell)
            rows.append(column_separator.join(cols))
        return row_separator.join(rows)

    @classmethod
    def from_frame(cls,
                   frame_str,
                   row_sep=DEFAULT_ROW_SEP):
        """
        param frame_str: A string with equal length rows
        param row_sep: A string that separates the rows in the frame (default DEFAULT_ROW_SEP (newline))
        return: Table
        """
        t = cls([])
        row_lines = frame_str.split(row_sep)

        # figure column sizes from top row
        header = row_lines.pop(0)
        len_header = len(header)
        col_name = ""
        last_col_name = None
        for ndx in range(len_header):
            c = header[ndx]
            if not c.isspace():
                col_name += c
            elif col_name:
                # the beginning offset of this column, row name is arbitrary, but we need to remove it later
                t.set_val('start', col_name, ndx - len(col_name))
                if last_col_name is not None:
                    t.set_val('end', last_col_name, ndx - len(col_name) - 1)
                last_col_name = col_name
                col_name = ""
            # one may notice that 'end' is not set on last column, it gets fixed later when we pass default=len_header

        row_ndx = 0
        while row_lines:
            row_ndx += 1
            line = row_lines.pop(0)
            if len(line) != len_header:
                # every line in a frame should be the same length as the first line
                raise ValueError(f'ROW({row_ndx}): {len(line)} does not equal {len_header}')

            if row_ndx == 1 and line == line[0] * len(line):
                row_ndx -= 1
                continue  # this is a row separator line all the way across the frame, ignore it

            # otherwise, this row has data
            for col_name in list(t.col_gen()):
                start = t.get_val('start', col_name)
                # there is no 'end' on last column, use header_len as default
                end = t.get_val('end', col_name, default=len_header - 1)
                val = line[start:end]
                t.set_val(row_ndx, col_name, val.strip())

        t.del_rows(['start', 'end'])
        return t

    def del_rows(self, row_list):
        new_od = OrderedDict()
        for key, val in self.__od.items():
            row, col = key
            if row not in row_list:
                new_od[key] = val
        self.__od = new_od

    def del_cols(self, col_list):
        new_od = OrderedDict()
        for key, val in self.__od.items():
            row, col = key
            if col not in col_list:
                new_od[key] = val
        self.__od = new_od

    def split_static(self, dynamic_table=None, static_table=None):
        # add to existing table if provided, or create new ones
        dynamic_table = dynamic_table or Table()
        static_table = static_table or Table()
        for col in self.col_gen():
            # if any column has the same value for every row, it is "static" and will be added to the static table
            static_val = None
            is_static = True
            for row in self.row_gen():
                val = self.get_val(row, col)
                if val != static_val:
                    if static_val is None:
                        static_val = val
                        continue
                    # not all the columns have the same value. this is a dynamic (not static) column
                    is_static = False
                    break
            # end for row ...
            if is_static:
                static_table.set_val(0, col, static_val)
            else:
                # all the other cells will be put in the dynamic table
                for x in self.tup_gen(cols=[col]):
                    dynamic_table.set_val(*x)
        return dynamic_table, static_table

    def count_unique_col(self, col):
        d = {}
        for row in self.row_gen():
            val = self.get_val(row, col)
            d[val] = None
        return len(d.keys())

    def print_repr_lines(self, title=None, row_separator=DEFAULT_ROW_SEP):
        for line in self.pf(title=title, row_separator=DEFAULT_ROW_SEP).split(row_separator):
            print(repr(line))