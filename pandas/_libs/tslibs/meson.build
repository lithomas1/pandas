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
