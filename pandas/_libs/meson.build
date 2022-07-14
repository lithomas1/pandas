_algos_common_helper = custom_target('algos_common_helper_pxi',
    output: 'algos_common_helper.pxi',
    input: 'algos_common_helper.pxi.in',
    command: [
        py, tempita, '@INPUT@', '-o', '@OUTDIR@'
    ]
)
_algos_take_helper = custom_target('algos_take_helper_pxi',
    output: 'algos_take_helper.pxi',
    input: 'algos_take_helper.pxi.in',
    command: [
        py, tempita, '@INPUT@', '-o', '@OUTDIR@'
    ]
)
_khash_primitive_helper = custom_target('khash_primitive_helper_pxi',
    output: 'khash_for_primitive_helper.pxi',
    input: 'khash_for_primitive_helper.pxi.in',
    command: [
        py, tempita, '@INPUT@', '-o', '@OUTDIR@'
    ]
)
_algos_common_helper_dep = declare_dependency(sources: _algos_common_helper)
_algos_take_helper_dep = declare_dependency(sources: _algos_take_helper)
_khash_primitive_helper_dep = declare_dependency(sources: _khash_primitive_helper)
# TODO: can this be removed, I wish meson copied .pyx source to the build dir automatically
# The reason we can't build the pyx files inplace and copy to build dir is because
# the generated pxi files cannot be written to the source directory.
# (Meson only supports out of tree builds)
cython_sources_list = [
    # List of cython sources e.g. .pyx, .pxd & __init__.py
    # Does NOT include .pxi.in
    '__init__.py',
    'algos.pxd',
    'algos.pyx',
    'arrays.pxd',
    'arrays.pyx',
    'dtypes.pxd',
    'groupby.pyx',
    'hashing.pyx',
    'hashtable.pxd',
    'hashtable.pyx',
    'index.pyx',
    'indexing.pyx',
    'internals.pyx',
    'interval.pyx',
    'join.pyx',
    'khash.pxd',
    'lib.pyx',
    'lib.pxd',
    'missing.pxd',
    'missing.pyx',
    'ops.pyx',
    'ops_dispatch.pyx',
    'parsers.pyx',
    'properties.pyx',
    'reduction.pyx',
    'reshape.pyx',
    'sparse.pyx',
    'testing.pyx',
    'tslib.pyx',
    'util.pxd',
    'writers.pyx'
]
cython_sources = {}

foreach source: cython_sources_list
    source_pyx = configure_file(
        input: source,
        output: source,
        copy: true
    )
    cython_sources += {source: source_pyx}
endforeach

subdir('tslibs')

py.extension_module(
    'algos',
    [_algos_common_helper, _algos_take_helper, _khash_primitive_helper, cython_sources['algos.pyx']],
    include_directories: [inc_np, klib_include],
    dependencies: [py_dep, _algos_common_helper_dep, _algos_take_helper_dep, _khash_primitive_helper_dep],
    subdir: 'pandas/_libs',
    install: true
)

py.extension_module(
    'arrays',
    cython_sources['arrays.pyx'],
    include_directories: [inc_np],
    dependencies: py_dep,
    subdir: 'pandas/_libs',
    install: true
)

py.extension_module(
    'groupby',
    cython_sources['groupby.pyx'],
    include_directories: [inc_np],
    dependencies: py_dep,
    subdir: 'pandas/_libs',
    install: true
)

py.extension_module(
    'hashing',
    cython_sources['hashing.pyx'],
    include_directories: [inc_np],
    dependencies: py_dep,
    subdir: 'pandas/_libs',
    install: true
)
