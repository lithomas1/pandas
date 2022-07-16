# This file is adapted from https://github.com/scipy/scipy/blob/main/meson.build
project(
    'pandas',
    'c', 'cpp', 'cython',
    version: '1.5.0.dev0',
    license: 'BSD-3',
    meson_version: '>=0.60',
    default_options: [
        'buildtype=debugoptimized',
        'c_std=c99'
    ]
)

py_mod = import('python')
py = py_mod.find_installation('python3')
py_dep = py.dependency()
tempita = files('generate_pxi.py')

subdir('pandas')
