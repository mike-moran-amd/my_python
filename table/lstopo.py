#!python3
# encoding=UTF-8

import data
import lib
import table


def from_text(text):
    # parse the text (assumed to be the output of 'cat /proc/cpuinfo') and return a new table with the data
    ret = CpuInfoTable()
    # the cpu text blocks are separated by a newline
    blocks = text.split('\n\n')
    row_counter = -1
    for row in blocks:
        row_counter += 1
        for line in row.split('\n'):
            if line == '':
                continue
            try:
                col, val = line.split(': ')
            except ValueError as err:
                continue  # the line has no value after the colon (we will call it None)

            ret.set_val(row_counter, col.strip(), val)
    return ret



class CpuInfoTable(table.Table):
    def __init__(self):
        super().__init__()

    def topology_table(self):
        tt = TopologyTable()
        for row in self.row_gen():

            pid = self.get_val(row, 'processor')
            pid = int(pid)
            tt.set_val(row, 'PID', pid)

            core_id = self.get_val(row, 'core id')
            core_id = int(core_id)
            tt.set_val(row, 'CoreID', core_id)

            socket_id = self.get_val(row, 'physical id')
            socket_id = int(socket_id)
            tt.set_val(row, 'SocketID', socket_id)

            # TODO where do we find NUMA node definition
            tt.set_val(row, 'NUMANodeID', 0)

            # TODO where do we find uncore cache definition
            tt.set_val(row, 'UnCoreCacheID', 0)
        return tt


def from_command(cls):
    # return a CpuDetailsTable from text in the given filepath, or this system
    text = lib.invoke_subprocess(['lstopo'])
    # TODO check to see if the command (will fail) because hwloc is not installed using which and install
    return LsTopoTable.from_text(text)


class LsTopoTable(table.Table):
    @classmethod
    def from_text(cls, text):
        lt = data.LineTable(text)
        indent = 0
        for row in lt.row_gen():
            new_indent = 0
            for char in lt.get_val(row, 'line'):
                if not char.isspace():
                    break
                new_indent += 1


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
            core_id = self.get_val(row, 'CoreID')
            d[core_id] = None
        return len(d.keys())
