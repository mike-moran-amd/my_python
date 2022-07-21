from my_python import table


def allocation_gen(number):
    """
    >>> len(list(allocation_gen(17)))
    65536
    """
    # say you have a number of items, how would you distribute them (in groups), all possibilities
    yield [number]
    # the first choice is to take all items (above), then choose a progressive number and recursively extend
    for n in range(number - 1, 0, -1):
        for rval in allocation_gen(number - n):
            l = [n]
            l.extend(rval)
            yield l


class AllocationTable(table.Table):
    @classmethod
    def from_max_allocation(cls, max_allocation):
        """
        >>> AllocationTable.from_max_allocation(5).print_repr_lines('MAX ALLOCATION(5)')
        'MAX ALLOCATION(5) | 0 |    1 |    2 |    3 |    4'
        '                0 | 5 |      |      |      |     '
        '                1 | 4 |    1 |      |      |     '
        '                2 | 3 |    2 |      |      |     '
        '                3 | 3 |    1 |    1 |      |     '
        '                4 | 2 |    3 |      |      |     '
        '                5 | 2 |    2 |    1 |      |     '
        '                6 | 2 |    1 |    2 |      |     '
        '                7 | 2 |    1 |    1 |    1 |     '
        '                8 | 1 |    4 |      |      |     '
        '                9 | 1 |    3 |    1 |      |     '
        '               10 | 1 |    2 |    2 |      |     '
        '               11 | 1 |    2 |    1 |    1 |     '
        '               12 | 1 |    1 |    3 |      |     '
        '               13 | 1 |    1 |    2 |    1 |     '
        '               14 | 1 |    1 |    1 |    2 |     '
        '               15 | 1 |    1 |    1 |    1 |    1'
        """
        t = cls()
        row = 0
        for allocation in allocation_gen(max_allocation):
            col = 0
            for take in allocation:
                t.set_val(row, col, take)
                col += 1
            row += 1
        return t
