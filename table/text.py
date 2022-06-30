# encoding=UTF-8
"""
>>> tt = TextTable.from_string(' first line'+NL+'line # 2 '+NL+'  ')  # a simple example line table
>>> print(tt.pf(title=''))
  | LINE        | leading_isspace(LINE) | trailing_isspace(LINE) | len(LINE) | len(LINE.split())
1 |  first line |                     1 |                      0 |        11 |                 2
2 | line # 2    |                     0 |                      1 |         9 |                 3
3 |             |                     2 |                      0 |         2 |                 0

>>> tt.get_val(1, Columns.LINE_LEADING_SPACES.value)
1
>>> tt.line_leading_spaces(1)
1

>>> tt.get_val(2, Columns.LINE_TRAILING_SPACES.value)
1
>>> tt.line_trailing_spaces(2)
1

>>> tt.get_val(1, Columns.LINE.value)
' first line'
>>> tt.line(1)
' first line'

>>> tt.get_val(3, Columns.LINE_LEN.value)
2
>>> tt.line_len(3)
2

>>> tt.get_val(2, Columns.LINE_WORD_COUNT.value)
3
>>> tt.line_word_count(2)
3

"""
import enum
import table


NL = '\n'


def leading_isspace(s: str):
    count = 0
    for char in s:
        if not char.isspace():
            break
        count += 1
    return count


def trailing_isspace(s: str):
    count = 0
    for char in s[::-1]:
        if not char.isspace():
            break
        count += 1
    return count


class Columns(enum.Enum):
    LINE = 'LINE'
    LINE_LEADING_SPACES = 'leading_isspace(LINE)'
    LINE_LEN = 'len(LINE)'
    LINE_TRAILING_SPACES = 'trailing_isspace(LINE)'
    LINE_WORD_COUNT = 'len(LINE.split())'

    @staticmethod
    def is_line(col):
        return col == Columns.LINE or col == Columns.LINE.value

    @staticmethod
    def table_updated(tt, row, col, val):
        # spread side effects
        if col == Columns.LINE or col == Columns.LINE.value:
            # dependant cols need to be recalculated
            lead_space = leading_isspace(val)
            tail_space = trailing_isspace(val)
            line_len = len(val)
            if lead_space + tail_space > line_len:
                # the line is all space(s)
                tail_space = 0
            tt.set_val(row, Columns.LINE_LEADING_SPACES.value, lead_space)
            tt.set_val(row, Columns.LINE_TRAILING_SPACES.value, tail_space)
            tt.set_val(row, Columns.LINE_LEN.value, line_len)
            tt.set_val(row, Columns.LINE_WORD_COUNT.value, len(val.split()))


class TextTable(table.Table):

    @classmethod
    def from_string(cls, s: str, sep=NL):
        t = cls()
        row = 0
        for line in s.split(sep):
            row += 1
            t.set_row_line(row, line)
        return t

    def set_row_line(self, row, line):
        self.set_val(row, Columns.LINE.value, line)

    def set_val(self, row, col, val):
        super(TextTable, self).set_val(row, col, val)
        Columns.table_updated(self, row, col, val)

    def line(self, row):
        line = self.get_val(row, Columns.LINE.value)
        return line

    def line_leading_spaces(self, row):
        ls = self.get_val(row, Columns.LINE_LEADING_SPACES.value)
        return ls

    def line_trailing_spaces(self, row):
        ts = self.get_val(row, Columns.LINE_TRAILING_SPACES.value)
        return ts

    def line_len(self, row):
        n = self.get_val(row, Columns.LINE_LEN.value)
        return n

    def line_word_count(self, row):
        wc = self.get_val(row, Columns.LINE_WORD_COUNT.value)
        return wc
