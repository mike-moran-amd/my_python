#!python3
# encoding=UTF-8

import data
import lib
import table
from table.line import LineTable


def from_system():
    # return a CpuDetailsTable from text in the given filepath, or this system
    text = lib.invoke_subprocess(['lstopo'])
    # TODO check to see if the command (will fail) because hwloc is not installed using which and install
    return LsTopoTable.from_text(text)


class LsTopoTable(table.Table):
    def __init__(self):
        super().__init__()
        self.numanodeid = 0
        self.uncorecacheid = 0
        self.socketid = 0
        self.coreid = 0


    @classmethod
    def from_text(cls, text):
        retval = cls()
        lt = LineTable.from_string(text)
        indent = -1
        for row in lt.row_gen():
            line = lt.line_from_row(row)
            new_indent = lt.leading_spaces_from_row(row)
            if indent == -1:
                if not line.startswith('Machine' or new_indent != 0):
                    raise ValueError(f'EXPECTED: {line}')
                indent = new_indent
            if indent > 0 and new_indent == 0:
                break  # end of lstopo output
            retval.parse_line(line.strip())
        return retval

    def parse_line(self, line):
        for blob in line.split(' + '):
            ss = blob.split(' ')
            thing = ss[0]
            if thing == 'Machine':
                pass
            elif thing == 'Package':
                if not ss[1].startswith('L#'):
                    raise ValueError(f'UNEXPECTED: {ss}')
                val = ss[1][2:]
                self.socketid = int(val)
            elif thing == 'NUMANode':
                if not ss[1].startswith('L#'):
                    raise ValueError(f'UNEXPECTED: {ss}')
                val = ss[1][2:]
                self.numanodeid = int(val)
            elif thing == 'L3':
                if not ss[1].startswith('L#'):
                    raise ValueError(f'UNEXPECTED: {ss}')
                val = ss[1][2:]
                self.uncorecacheid = int(val)
            elif thing == 'L2':
                if not ss[1].startswith('L#'):
                    raise ValueError(f'UNEXPECTED: {ss}')
            elif thing == 'L1d':
                if not ss[1].startswith('L#'):
                    raise ValueError(f'UNEXPECTED: {ss}')
            elif thing == 'L1i':
                if not ss[1].startswith('L#'):
                    raise ValueError(f'UNEXPECTED: {ss}')
            elif thing == 'Core':
                if not ss[1].startswith('L#'):
                    raise ValueError(f'UNEXPECTED: {ss}')
                val = ss[1][2:]
                self.coreid = int(val)
            elif thing == 'PU':
                current_row = len(list(self.row_gen()))
                if not ss[1].startswith('L#'):
                    raise ValueError(f'UNEXPECTED: {ss}')
                if not ss[2].startswith('(P#') or not ss[2].endswith(')'):
                    raise ValueError(f'UNEXPECTED: {ss}')
                val = ss[2][3:-1]
                self.set_val(current_row, 'PID', int(val))
                self.set_val(current_row, 'CoreID', self.coreid)
                self.set_val(current_row, 'SocketID', self.socketid)
                self.set_val(current_row, 'NUMANodeID', self.numanodeid)
                self.set_val(current_row, 'UnCoreCacheID', self.uncorecacheid)
            else:
                if thing not in (
                    'HostBridge',
                    'PCIBridge',
                    'PCI',
                    'Net',
                    'OpenFabrics',
                    'Block(Disk)',
                    '',
                ):
                    raise ValueError(f'UNEXPECTED: {thing}')

    def print_golang_struct(self, name):
        print(f'    {name} = &topology.CPUTopology' + '{')
        print(f'        NumCPUs:      {self.count_cpus()},')
        print(f'        NumCores:     {self.count_cores()},')
        print(f'        NumSockets:   {self.count_sockets()},')
        print(f'        NumNUMANodes: {self.count_numa_nodes()},')
        print('        CPUDetails: map[int]topology.CPUInfo{')
        for row in self.row_gen():
            pid = self.get_val(row, "PID")
            cid = self.get_val(row, 'CoreID')
            sid = self.get_val(row, 'SocketID')
            nid = self.get_val(row, 'NUMANodeID')
            uid = self.get_val(row, 'UnCoreCacheID')
            print('            %s: {CoreID: %s, SocketID: %s, NUMANodeID: %s, UnCoreCacheID: %s},'% (pid, cid, sid, nid, uid))
        print('        },')
        print('    }')

    def count_cpus(self):
        return len(list(self.row_gen()))

    def count_cores(self):
        d = {}
        for row in self.row_gen():
            core_id = self.get_val(row, 'CoreID')
            d[core_id] = None
        return len(d.keys())

    def count_sockets(self):
        d = {}
        for row in self.row_gen():
            socket_id = self.get_val(row, 'SocketID')
            d[socket_id] = None
        return len(d.keys())

    def count_numa_nodes(self):
        d = {}
        for row in self.row_gen():
            core_id = self.get_val(row, 'NUMANodeID')
            d[core_id] = None
        return len(d.keys())
