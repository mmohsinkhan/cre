"""
(cre) module installation script.
"""

import sys
from setuptools import setup, Extension
from subprocess import check_output

MODULE_NAME = 'cre'


def get_pkgconfig(packages):
    """
    Get compile and link time configurations for package(s) using
    'pkg-config' utility.
    @param packages: List of packages names. (list)
    @return: Values for following distutils Extension class arguments,
    'include_dirs', 'extra_compile_args', 'library_dirs', 'libraries',
    'extra_link_args'. (dict)
    """
    # distutils configs to pkg-config options mapping:
    du_pc_map = {
        'include_dirs': ('--cflags-only-I', 2),
        'extra_compile_args': ('--cflags-only-other', 0),
        'library_dirs': ('--libs-only-L', 2),
        'libraries': ('--libs-only-l', 2),
        'extra_link_args': ('--libs-only-other', 0),
    }

    du_cfgs = dict()
    for du_cfg in du_pc_map:
        du_cfgs[du_cfg] = []

    for package in packages:
        for du_cfg, (pc_op, offset) in du_pc_map.items():
            output = check_output(['pkg-config', pc_op, package]) \
                     .decode('utf-8').strip()
            for cfg in output.split():
                du_cfgs[du_cfg].append(cfg[offset:])

    return du_cfgs


GLIBCONFIG = get_pkgconfig(['glib-2.0'])

try:
    # If installed, build with Cython:
    from Cython.Build import cythonize
    EXTENSION = cythonize([Extension(MODULE_NAME, [MODULE_NAME + '.pyx'],
                                     **GLIBCONFIG)],
                          build_dir='build',
                          language_level=sys.version_info[0])
except ImportError:
    # Build C file directly:
    EXTENSION = [Extension(MODULE_NAME, [MODULE_NAME + '_pp.c'],
                           **GLIBCONFIG)]

setup(
    name=MODULE_NAME,
    version='1.0.0',
    test_suite='tests',
    ext_modules=EXTENSION
)
