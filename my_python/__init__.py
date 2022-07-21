import pathlib
VERSION = '0.2'
PARENT_PATH = pathlib.Path(__file__).parent.parent


def py_modules():
    """
    >>> for name in py_modules():
    ...     print(name)
    my_python

    """
    ret_list = []
    for path in PARENT_PATH.glob('*'):
        if path.is_dir() and pathlib.Path(path, '__init__.py').exists():
            ret_list.append(path.name)
        pass
    return sorted(ret_list)
