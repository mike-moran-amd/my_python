#!python3
# encoding=UTF-8

import enum
import lib
import table
from table.text import TextTable


def from_system():
    # TODO check to see if the command (will fail) because hwloc is not installed using which and install
    text = lib.invoke_subprocess(['lstopo'])
    return LsTopoTable.from_text(text)


class ColumnEnum(enum.Enum):
    # Machine
    Package = "Package"
    NUMANode = 'NUMANode'
    L3 = 'L3'
    L2 = 'L2'
    L1d = 'L1d'
    L1i = 'L1i'
    Core = 'Core'
    PU = 'PU'


COLUMNS = [e.value for e in ColumnEnum]


class LsTopoTable(table.Table):
    def __init__(self):
        super().__init__()

    @classmethod
    def from_text(cls, text):
        retval = cls()
        tt = TextTable.from_string(text)
        indent = -1
        tally = {}
        for row in tt.row_gen():
            line = tt.line_from_row(row)
            new_indent = tt.leading_spaces_from_row(row)
            if indent == -1:
                if not line.startswith('Machine' or new_indent != 0):
                    raise ValueError(f'UNEXPECTED: {line}')
                indent = new_indent
            if indent > 0 and new_indent == 0:
                break  # end of lstopo output
            retval.parse_line(line.strip(), tally)
        return retval

    def parse_line(self, line, tally):
        for blob in line.split(' + '):
            ss = blob.split(' ')
            facet = ss[0]
            if facet == 'Machine':
                pass
            elif facet == ColumnEnum.PU.value:
                row = len(list(self.row_gen()))
                if not ss[1].startswith('L#'):
                    raise ValueError(f'UNEXPECTED: {ss}')
                if not ss[2].startswith('(P#') or not ss[2].endswith(')'):
                    raise ValueError(f'UNEXPECTED: {ss}')
                val = ss[2][3:-1]
                tally[facet] = int(val)
                for e in ColumnEnum:
                    self.set_val(row, e.value, tally[e.value])
            elif facet in COLUMNS:
                if not ss[1].startswith('L#'):
                    raise ValueError(f'UNEXPECTED: {ss}')
                val = ss[1][2:]
                tally[facet] = int(val)
            else:
                if facet not in (
                    'Block(Disk)',
                    'HostBridge',
                    'Net',
                    'OpenFabrics',
                    'PCI',
                    'PCIBridge',
                    '',
                ):
                    raise ValueError(f'UNEXPECTED: {facet}')

    def print_golang_struct(self, name):
        print(f'    {name} = &topology.CPUTopology' + '{')
        print(f'        NumCPUs:      {self.count_unique_col(ColumnEnum.PU.value)},')
        print(f'        NumCores:     {self.count_unique_col(ColumnEnum.Core.value)},')
        print(f'        NumSockets:   {self.count_unique_col(ColumnEnum.Package.value)},')
        print(f'        NumNUMANodes: {self.count_unique_col(ColumnEnum.NUMANode.value)},')
        print('        CPUDetails: map[int]topology.CPUInfo{')
        for row in self.row_gen():
            pid = self.get_val(row, ColumnEnum.PU.value)
            cid = self.get_val(row, ColumnEnum.Core.value)
            sid = self.get_val(row, ColumnEnum.Package.value)
            nid = self.get_val(row, ColumnEnum.NUMANode.value)
            uid = self.get_val(row, ColumnEnum.L3.value)
            print('            %s: {CoreID: %s, SocketID: %s, NUMANodeID: %s, UnCoreCacheID: %s},' % (
                pid, cid, sid, nid, uid))
        print('        },')
        print('    }')
