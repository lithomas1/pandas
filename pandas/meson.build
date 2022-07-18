incdir_numpy = run_command(py,
  [
    '-c',
    'import os; os.chdir(".."); import numpy; print(numpy.get_include())'
  ],
  check: true
).stdout().strip()

inc_np = include_directories(incdir_numpy)
klib_include = include_directories('_libs/src/klib')
inc_datetime = include_directories('_libs/tslibs')

configure_file(
    input: '__init__.py',
    output: '__init__.py',
    copy: true
)
subdir('_libs')
subdir('io/sas')
# TODO: this works but needs a patch in meson-python
# meson-python only looks in the meson-info/install_plan.json not in meson-info/installed.json
# However, subdirs are not listed in the install_plan only in installed.json
install_subdir('_config', install_dir: get_option('python.platlibdir') / 'pandas/_config')
py.install_sources('__init__.py',
                    pure: false,
                    subdir: 'pandas')
