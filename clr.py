"""
Legacy Python.NET loader for backwards compatibility
"""

def _get_netfx_path():
    import os, sys

    if sys.maxsize > 2 ** 32:
        arch = "amd64"
    else:
        arch = "x86"

    return os.path.join(os.path.dirname(__file__), "pythonnet", "netfx", arch, "clr.pyd")


def _get_mono_path():
    import os, glob

    file_path = os.path.dirname(__file__)
    expected_path_match = os.path.join(file_path, "pythonnet", "mono", "clr.*so")
    paths = glob.glob(expected_path_match)
    if paths:
        return paths[0]
    raise Exception("Mono not found.")


def _load_clr():
    import sys
    from importlib import util

    path = _get_netfx_path() if sys.platform == "win32" else _get_mono_path()
    del sys.modules[__name__]

    spec = util.spec_from_file_location("clr", path)
    clr = util.module_from_spec(spec)
    spec.loader.exec_module(clr)

    sys.modules[__name__] = clr


_load_clr()
