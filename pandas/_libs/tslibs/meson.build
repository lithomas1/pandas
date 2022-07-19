# TODO: can this be removed, I wish meson copied .pyx source to the build dir automatically
tslibs_pxd_sources_list = [
    # List of cython sources e.g. .pyx, .pxd & __init__.py
    # Does NOT include .pxi.in
    '__init__.py',
    'base.pxd',
    'ccalendar.pxd',
    'conversion.pxd',
    'dtypes.pxd',
    'nattype.pxd',
    'np_datetime.pxd',
    'offsets.pxd',
    'parsing.pxd',
    'period.pxd',
    'timedeltas.pxd',
    'timestamps.pxd',
    'timezones.pxd',
    'tzconversion.pxd',
    'util.pxd',
]

foreach source: tslibs_pxd_sources_list
    source_pxd = configure_file(
        input: source,
        output: source,
        copy: true
    )
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

py.install_sources('__init__.py',
                    pure: false,
                    subdir: 'pandas/_libs/tslibs')
