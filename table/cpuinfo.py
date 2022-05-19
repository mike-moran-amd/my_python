#!python3
# encoding=UTF-8

import lib
import table


def from_text(text):
    # parse the text (assumed to be the output of 'cat /proc/cpuinfo') and return a new table with the data
    ret = CpuDetailsTable()
    # the cpu text blocks are separated by a newline
    blocks = text.split('\n\n')
    row_counter = -1
    for row in blocks:
        row_counter += 1
        for line in row.split('\n'):
            if line == '':
                continue
            col, val = line.split(': ')
            ret.set_val(row_counter, col.strip(), val)
    return ret


def from_file(filepath='/proc/cpuinfo'):
    # return a CpuDetailsTable from text in the given filepath, or this system
    text = lib.invoke_subprocess(['cat', filepath])
    return from_text(text)


class CpuDetailsTable(table.Table):
    def __init__(self):
        super().__init__()
    # TODO add cpuinfo specific methods here ...
