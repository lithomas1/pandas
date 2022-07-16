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
_hashtable_class_helper = custom_target('hashtable_class_helper_pxi',
    output: 'hashtable_class_helper.pxi',
    input: 'hashtable_class_helper.pxi.in',
    command: [
        py, tempita, '@INPUT@', '-o', '@OUTDIR@'
    ]
)
_hashtable_func_helper = custom_target('hashtable_func_helper_pxi',
    output: 'hashtable_func_helper.pxi',
    input: 'hashtable_func_helper.pxi.in',
    command: [
        py, tempita, '@INPUT@', '-o', '@OUTDIR@'
    ]
)
_index_class_helper = custom_target('index_class_helper_pxi',
    output: 'index_class_helper.pxi',
    input: 'index_class_helper.pxi.in',
    command: [
        py, tempita, '@INPUT@', '-o', '@OUTDIR@'
    ]
)
_sparse_op_helper = custom_target('sparse_op_helper_pxi',
    output: 'sparse_op_helper.pxi',
    input: 'sparse_op_helper.pxi.in',
    command: [
        py, tempita, '@INPUT@', '-o', '@OUTDIR@'
    ]
)
_intervaltree_helper = custom_target('intervaltree_helper_pxi',
    output: 'intervaltree.pxi',
    input: 'intervaltree.pxi.in',
    command: [
        py, tempita, '@INPUT@', '-o', '@OUTDIR@'
    ]
)
_algos_common_helper_dep = declare_dependency(sources: _algos_common_helper)
_algos_take_helper_dep = declare_dependency(sources: _algos_take_helper)
_khash_primitive_helper_dep = declare_dependency(sources: _khash_primitive_helper)
_hashtable_class_helper_dep = declare_dependency(sources: _hashtable_class_helper)
_hashtable_func_helper_dep = declare_dependency(sources: _hashtable_func_helper)
_index_class_helper_dep = declare_dependency(sources: _index_class_helper)
_sparse_op_helper_dep = declare_dependency(sources: _sparse_op_helper)
_intervaltree_helper_dep = declare_dependency(sources: _intervaltree_helper)
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

#py.extension_module(
#    'parsing',
#    ['tslibs/parsing.pyx'],
#    include_directories: [inc_np, klib_include, 'src/parser', 'src', 'tslibs/src/datetime'],
#    dependencies: [py_dep],
#   subdir: 'pandas/_libs/tslibs',
#    install: true
#)

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

py.extension_module(
    'hashtable',
    [cython_sources['hashtable.pyx'], _khash_primitive_helper, _hashtable_class_helper, _hashtable_func_helper],
    include_directories: [inc_np, klib_include],
    dependencies: [py_dep, _khash_primitive_helper_dep, _hashtable_class_helper_dep, _hashtable_func_helper_dep],
    subdir: 'pandas/_libs',
    install: true
)

#py.extension_module(
#    'index',
#    [cython_sources['index.pyx'], _index_class_helper],
#    include_directories: [inc_np, klib_include],
#    dependencies: [py_dep, _index_class_helper_dep],
#    subdir: 'pandas/_libs',
#    install: true
#)

py.extension_module(
    'indexing',
    ['indexing.pyx'],
    include_directories: [inc_np],
    dependencies: py_dep,
    subdir: 'pandas/_libs',
    install: true
)

py.extension_module(
    'internals',
    ['internals.pyx'],
    include_directories: [inc_np],
    dependencies: py_dep,
    subdir: 'pandas/_libs',
    install: true
)

#py.extension_module(
#    'interval',
#    [cython_sources['interval.pyx'], _intervaltree_helper],
#    include_directories: [inc_np, klib_include],
#    dependencies: [py_dep, _intervaltree_helper_dep],
#    subdir: 'pandas/_libs',
#    install: true
#)

py.extension_module(
    'join',
    [cython_sources['join.pyx'], _khash_primitive_helper],
    include_directories: [inc_np, klib_include],
    dependencies: [py_dep, _khash_primitive_helper_dep],
    subdir: 'pandas/_libs',
    install: true
)

py.extension_module(
    'lib',
    ['lib.pyx', 'src/parser/tokenizer.c'],
    include_directories: [inc_np, klib_include, inc_datetime],
    dependencies: [py_dep],
    subdir: 'pandas/_libs',
    install: true
)

#py.extension_module(
#    'parsers',
#    [cython_sources['parsers.pyx'], _khash_primitive_helper, 'src/parser/tokenizer.c', 'src/parser/io.c'],
#    include_directories: [inc_np, klib_include, 'src/parser', 'src'],
#    dependencies: [py_dep, _khash_primitive_helper_dep],
#    subdir: 'pandas/_libs',
#    install: true
#)

py.extension_module(
    'reduction',
    ['reduction.pyx'],
    include_directories: [inc_np],
    dependencies: [py_dep],
    subdir: 'pandas/_libs',
    install: true
)

py.extension_module(
    'ops',
    ['ops.pyx'],
    include_directories: [inc_np],
    dependencies: [py_dep],
    subdir: 'pandas/_libs',
    install: true
)

py.extension_module(
    'ops_dispatch',
    ['ops_dispatch.pyx'],
    include_directories: [inc_np],
    dependencies: [py_dep],
    subdir: 'pandas/_libs',
    install: true
)

py.extension_module(
    'properties',
    ['properties.pyx'],
    include_directories: [inc_np],
    dependencies: [py_dep],
    subdir: 'pandas/_libs',
    install: true
)

py.extension_module(
    'reshape',
    ['reshape.pyx'],
    include_directories: [inc_np],
    dependencies: [py_dep],
    subdir: 'pandas/_libs',
    install: true
)

py.extension_module(
    'sparse',
    [cython_sources['sparse.pyx'], _sparse_op_helper],
    include_directories: [inc_np],
    dependencies: [py_dep, _sparse_op_helper_dep],
    subdir: 'pandas/_libs',
    install: true
)

py.extension_module(
    'tslib',
    ['tslib.pyx', 'tslibs/src/datetime/np_datetime.c'],
    include_directories: [inc_np, inc_datetime],
    dependencies: [py_dep],
    subdir: 'pandas/_libs',
    install: true
)
