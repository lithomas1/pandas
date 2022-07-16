# TODO: can this be removed, I wish meson copied .pyx source to the build dir automatically
tslibs_cython_sources_list = [
    # List of cython sources e.g. .pyx, .pxd & __init__.py
    # Does NOT include .pxi.in
    '__init__.py',
    'base.pxd',
    'base.pyx',
    'ccalendar.pxd',
    'ccalendar.pyx',
    'conversion.pxd',
    'conversion.pyx',
    'dtypes.pyx',
    'dtypes.pxd',
    'fields.pyx',
    'nattype.pyx',
    'nattype.pxd',
    'np_datetime.pxd',
    'np_datetime.pyx',
    'offsets.pxd',
    'offsets.pyx',
    'parsing.pxd',
    'parsing.pyx',
    'period.pyx',
    'period.pxd',
    'strptime.pyx',
    'timedeltas.pxd',
    'timedeltas.pyx',
    'timestamps.pyx',
    'timestamps.pxd',
    'timezones.pyx',
    'timezones.pxd',
    'tzconversion.pxd',
    'tzconversion.pyx',
    'util.pxd',
    'vectorized.pyx',
]
tslibs_cython_sources = {}

foreach source: tslibs_cython_sources_list
    source_pyx = configure_file(
        input: source,
        output: source,
        copy: true
    )
    tslibs_cython_sources += {source: source_pyx}
endforeach

# TODO: build a shared library for np_datetime and np_datetime_strings
# and use lto?

py.extension_module(
    'base',
    ['base.pyx'],
    include_directories: [inc_np],
    dependencies: [py_dep],
    subdir: 'pandas/_libs/tslibs',
    install: true
)

py.extension_module(
    'ccalendar',
    ['ccalendar.pyx'],
    include_directories: [inc_np],
    dependencies: [py_dep],
    subdir: 'pandas/_libs/tslibs',
    install: true
)

py.extension_module(
    'dtypes',
    ['dtypes.pyx'],
    include_directories: [inc_np],
    dependencies: [py_dep],
    subdir: 'pandas/_libs/tslibs',
    install: true
)

py.extension_module(
    'conversion',
    ['conversion.pyx', 'src/datetime/np_datetime.c'],
    include_directories: [inc_np, inc_datetime],
    dependencies: [py_dep],
    subdir: 'pandas/_libs/tslibs',
    install: true
)

py.extension_module(
    'fields',
    ['fields.pyx', 'src/datetime/np_datetime.c'],
    include_directories: [inc_np, inc_datetime],
    dependencies: [py_dep],
    subdir: 'pandas/_libs/tslibs',
    install: true
)

py.extension_module(
    'nattype',
    ['nattype.pyx'],
    include_directories: [inc_np, inc_datetime],
    dependencies: [py_dep],
    subdir: 'pandas/_libs/tslibs',
    install: true
)

py.extension_module(
    'np_datetime',
    ['np_datetime.pyx', 'src/datetime/np_datetime.c', 'src/datetime/np_datetime_strings.c'],
    include_directories: [inc_np, inc_datetime],
    dependencies: [py_dep],
    subdir: 'pandas/_libs/tslibs',
    install: true
)

py.extension_module(
    'offsets',
    ['offsets.pyx', 'src/datetime/np_datetime.c'],
    include_directories: [inc_np, inc_datetime],
    dependencies: [py_dep],
    subdir: 'pandas/_libs/tslibs',
    install: true
)

py.extension_module(
    'parsing',
    ['parsing.pyx', '../src/parser/tokenizer.c'],
    include_directories: [inc_np, klib_include],
    dependencies: [py_dep],
    subdir: 'pandas/_libs/tslibs',
    install: true
)

py.extension_module(
    'period',
    ['period.pyx', 'src/datetime/np_datetime.c'],
    include_directories: [inc_np, inc_datetime],
    dependencies: [py_dep],
    subdir: 'pandas/_libs/tslibs',
    install: true
)

py.extension_module(
    'strptime',
    ['strptime.pyx'],
    include_directories: [inc_np, inc_datetime],
    dependencies: [py_dep],
    subdir: 'pandas/_libs/tslibs',
    install: true
)

py.extension_module(
    'timedeltas',
    ['timedeltas.pyx', 'src/datetime/np_datetime.c'],
    include_directories: [inc_np, inc_datetime],
    dependencies: [py_dep],
    subdir: 'pandas/_libs/tslibs',
    install: true
)

py.extension_module(
    'timestamps',
    ['timestamps.pyx', 'src/datetime/np_datetime.c'],
    include_directories: [inc_np, inc_datetime],
    dependencies: [py_dep],
    subdir: 'pandas/_libs/tslibs',
    install: true
)

py.extension_module(
    'timezones',
    ['timezones.pyx'],
    include_directories: [inc_np, inc_datetime],
    dependencies: [py_dep],
    subdir: 'pandas/_libs/tslibs',
    install: true
)

py.extension_module(
    'tzconversion',
    ['tzconversion.pyx', 'src/datetime/np_datetime.c'],
    include_directories: [inc_np, inc_datetime],
    dependencies: [py_dep],
    subdir: 'pandas/_libs/tslibs',
    install: true
)

py.extension_module(
    'vectorized',
    ['tzconversion.pyx', 'src/datetime/np_datetime.c'],
    include_directories: [inc_np, inc_datetime],
    dependencies: [py_dep],
    subdir: 'pandas/_libs/tslibs',
    install: true
)
