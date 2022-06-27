# encoding=UTF-8
"""
"""
import enum
import re
import table
from urllib import parse


class Columns(enum.Enum):
    A = 'a'  # raw text
    A_UNQUOTE = 'parse.unquote(a)'  # remove pesky url encodings (so we can read it)
    A_VALUE = 'a_value'  # raw text sans key=value attributes which are added as columns in table

    @staticmethod
    def table_updated(at, row, col, val):
        # spread side effects
        if col == Columns.A or col == Columns.A.value:

            # update A_UNQUOTE
            at.set_val(row, Columns.A_UNQUOTE.value, parse.unquote(val))
            # get initial A_VALUE
            a_value = val
            for k, v in re.findall('(.+?)="(.+?)"', val):
                # these attributes will be columns in the table
                at.set_val(row, k, v)
                remove_me = f'{k}="{v}"'
                # remove matches from A_VALUE
                a_value = a_value.replace(remove_me, '')

            # update A_VALUE sans findall matches above
            at.set_val(row, Columns.A_VALUE.value, a_value)


class ATable(table.Table):
    @classmethod
    def from_text(cls, text):
        at = cls()
        row = 0
        # use regex to find all non-overlapping "a" tags in the given text string
        for a_ref in re.findall('<a (.+?)</a>', text):
            row += 1
            at.set_val(row, Columns.A.value, a_ref)
        return at

    def set_val(self, row, col, val):
        # Do what we usually do (set the value)
        super(ATable, self).set_val(row, col, val)
        # Then update dependant columns
        Columns.table_updated(self, row, col, val)

    def get_a(self, row):
        return self.get_val(row, Columns.A.value)

    def get_a_value(self, row):
        return self.get_val(row, Columns.A_VALUE.value)
