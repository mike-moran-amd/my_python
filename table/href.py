# encoding=UTF-8
"""
"""
import enum
import table
from table.a import ATable


class Columns(enum.Enum):
    HREF = 'href'
    HREF_VALUE = 'href_value'

    @staticmethod
    def table_updated(at, row, col, val):
        # spread side effects
        if col == Columns.HREF or col == Columns.HREF.value:
            pass


class HrefTable(table.Table):
    @classmethod
    def from_atable(cls, at, href_starts_with=None):
        ht = cls()
        row = 0
        # use regex to find all non-overlapping "a" tags in the given text string
        for at_row in at.row_gen():
            href = at.get_val(at_row, Columns.HREF.value)
            if not href:
                continue
            href_value = at.get_a_value(at_row)
            if not href_value or not href_value.strip():
                continue
            if href_starts_with and href.startswith(href_starts_with):
                row += 1
                ht.set_val(row, Columns.HREF.value, href)
                ht.set_val(row, Columns.HREF_VALUE.value, href_value)
        return ht

    @classmethod
    def from_text(cls, text, href_starts_with=None):
        at = ATable.from_text(text)
        return HrefTable.from_atable(at, href_starts_with=href_starts_with)

    def set_val(self, row, col, val):
        # Do what we usually do (set the value)
        super(HrefTable, self).set_val(row, col, val)
        # Then update dependant columns
        Columns.table_updated(self, row, col, val)

    def get_href(self, row):
        return self.get_val(row, Columns.HREF.value)

    def get_href_value(self, row):
        return self.get_val(row, Columns.HREF_VALUE.value)
