py.extension_module(
    '_sas',
    ['sas.pyx'],
    include_directories: [inc_np],
    dependencies: [py_dep],
    subdir: 'pandas/io/sas',
    install: true
)
top_level_py_list = [
    '__init__.py',
    'sas7bdat.py',
    'sas_constants.py',
    'sas_xport.py',
    'sasreader.py'
]
foreach file: top_level_py_list
    py.install_sources(file,
                       pure: false,
                       subdir: 'pandas/io/sas')
endforeach
