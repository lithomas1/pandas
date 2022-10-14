# This file is adapted from https://github.com/scipy/scipy/blob/main/meson.build
project(
    'pandas',
    'c', 'cpp', 'cython',
    version: '1.6.0.dev0',
    license: 'BSD-3',
    meson_version: '>=0.63',
    default_options: [
        'buildtype=release',
        'c_std=c99'
    ]
)

py_mod = import('python')
py = py_mod.find_installation('python')
py_dep = py.dependency()
tempita = files('generate_pxi.py')
versioneer = files('generate_version.py')

# TODO: Think about how this would work for an sdist
custom_target('write_version_file',
    output: '__version_meson.py',
    command: [
        py, versioneer, '-o', '@OUTPUT@'
    ],
    build_by_default: true,
    build_always_stale: true,
    install: true,
    install_dir: py.get_install_dir(pure: false) / 'pandas'
)

subdir('pandas')
