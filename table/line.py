# encoding=UTF-8
"""
>>> lt = LineTable.from_string(' first line'+NL+'line # 2 '+NL+'  ')  # a simple example line table
>>> print(lt.pf(title=''))
  | LINE        | LS | TS | LEN | WORD
0 |  first line |  1 |  0 |  11 |    2
1 | line # 2    |  0 |  1 |   9 |    3
2 |             |  2 |  0 |   2 |    0

>>> lt.leading_spaces_from_row(0)
1

>>> lt.trailing_spaces_from_row(1)
1

>>> lt.line_from_row(0)
' first line'

>>> lt.len_from_row(2)
2

>>> lt.word_count_from_row(1)
3

"""
import table


NL = '\n'
LINE_COL_LABEL = 'LINE'
LEADING_SPACES_COL_LABEL = 'LS'
TRAILING_SPACES_COL_LABEL = 'TS'
LEN_COL_LABEL = 'LEN'
WORD_COUNT_COL_LABEL = 'WORD'


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


class LineTable(table.Table):
    @classmethod
    def from_string(cls, s: str, sep=NL):
        t = cls()
        row = -1
        for line in s.split(sep):
            row += 1
            t.set_val(row, LINE_COL_LABEL, line)
        return t

    def set_val(self, row, col, val):
        # Overload super to recalculate dependant fields if LINE changes value
        super(LineTable, self).set_val(row, col, val)
        if col == LINE_COL_LABEL:
            # dependant fields need to be recalculated
            self.set_val(row, LEADING_SPACES_COL_LABEL, leading_isspace(val))
            self.set_val(row, TRAILING_SPACES_COL_LABEL, trailing_isspace(val))
            self.set_val(row, LEN_COL_LABEL, len(val))
            self.set_val(row, WORD_COUNT_COL_LABEL, len(val.split()))
            if self.get_val(row, LEADING_SPACES_COL_LABEL) + self.get_val(row, TRAILING_SPACES_COL_LABEL) > len(val):
                # the line is all isspace(), and TS has recounted the space, reset TS to 0
                self.set_val(row, TRAILING_SPACES_COL_LABEL, 0)

    def leading_spaces_from_row(self, row):
        return self.get_val(row, LEADING_SPACES_COL_LABEL)

    def trailing_spaces_from_row(self, row):
        return self.get_val(row, TRAILING_SPACES_COL_LABEL)

    def line_from_row(self, row):
        return self.get_val(row, LINE_COL_LABEL)

    def len_from_row(self, row):
        return self.get_val(row, LEN_COL_LABEL)

    def word_count_from_row(self, row):
        return self.get_val(row, WORD_COUNT_COL_LABEL)
