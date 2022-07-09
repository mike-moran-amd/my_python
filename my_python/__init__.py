import pathlib
VERSION = '0.1'
PARENT_PATH = pathlib.Path(__file__).parent


def py_modules():
    """
    >>> for name in py_modules():
    ...     print(name)
    __init__
    data
    fastapi_main
    jenkins
    lib
    my_vbox
    prime
    prime_test
    setup
    ssh
    table

    """
    ret_list = []
    for path in PARENT_PATH.glob('*'):
        if path.is_file() and path.name.endswith('.py'):
            ret_list.append(path.name[:-3])
        if path.is_dir() and pathlib.Path(path, '__init__.py').exists():
            ret_list.append(path.name)
        pass
    return sorted(ret_list)
