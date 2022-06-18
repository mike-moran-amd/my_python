# encoding=UTF-8
"""
>>> tt = TextTable.from_string(' first line'+NL+'line # 2 '+NL+'  ')  # a simple example line table
>>> print(tt.pf(title=''))
  | LINE        | LS | TS | LEN | WORD
0 |  first line |  1 |  0 |  11 |    2
1 | line # 2    |  0 |  1 |   9 |    3
2 |             |  2 |  0 |   2 |    0

>>> tt.get_val(0, Columns.LEADING_SPACES.value)
1

>>> tt.get_val(1, Columns.TRAILING_SPACES.value)
1

>>> tt.get_val(0, Columns.LINE.value)
' first line'

>>> tt.get_val(2, Columns.LEN.value)
2

>>> tt.get_val(1, Columns.WORD_COUNT.value)
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
    LEADING_SPACES = 'LS'
    LEN = 'LEN'
    LINE = 'LINE'
    TRAILING_SPACES = 'TS'
    WORD_COUNT = 'WORD'

    @staticmethod
    def is_line(col):
        return col == Columns.LINE or col == Columns.LINE.value


class TextTable(table.Table):

    @classmethod
    def from_string(cls, s: str, sep=NL):
        t = cls()
        row = -1
        for line in s.split(sep):
            row += 1
            t.set_row_line(row, line)
        return t

    def set_row_line(self, row, line):
        self.set_val(row, Columns.LINE.value, line)

    def set_val(self, row, col, val):
        # Overload super to recalculate dependant fields if LINE changes value
        super(TextTable, self).set_val(row, col, val)
        if Columns.is_line(col):
            # dependant cols need to be recalculated
            lead_space = leading_isspace(val)
            tail_space = trailing_isspace(val)
            line_len = len(val)
            if lead_space + tail_space > line_len:
                # the line is all space(s)
                tail_space = 0
            self.set_val(row, Columns.LEADING_SPACES.value, lead_space)
            self.set_val(row, Columns.TRAILING_SPACES.value, tail_space)
            self.set_val(row, Columns.LEN.value, line_len)
            self.set_val(row, Columns.WORD_COUNT.value, len(val.split()))
