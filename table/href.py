# encoding=UTF-8
"""
"""
import enum
import table
from urllib import parse
from table.a import ATable


class Columns(enum.Enum):
    HREF = 'href'
    HREF_VALUE = 'href_value'


class HrefTable(table.Table):
    @classmethod
    def from_a_table(cls, at, href_starts_with=None):
        ht = cls()
        row = 0
        for at_row in at.row_gen():
            href = at.get_val(at_row, Columns.HREF.value)
            if not href:
                continue
            href_value = at.get_a_value(at_row)
            if not href_value or not href_value.strip():
                continue
            href = parse.unquote(href)
            if not href_starts_with or href.startswith(href_starts_with):
                row += 1
                ht.set_val(row, Columns.HREF.value, href)
                ht.set_val(row, Columns.HREF_VALUE.value, href_value)
        return ht

    @classmethod
    def from_text(cls, text, href_starts_with=None):
        at = ATable.from_text(text)
        return HrefTable.from_a_table(at, href_starts_with=href_starts_with)

    def get_href(self, row):
        return self.get_val(row, Columns.HREF.value)

    def get_href_value(self, row):
        return self.get_val(row, Columns.HREF_VALUE.value)
