incdir_numpy = run_command(py,
  [
    '-c',
    'import os; os.chdir(".."); import numpy; print(numpy.get_include())'
  ],
  check: true
).stdout().strip()

inc_np = include_directories(incdir_numpy)
klib_include = include_directories('_libs/src/klib')
configure_file(
    input: '__init__.py',
    output: '__init__.py',
    copy: true
)
subdir('_libs')

#install_subdir('_config', install_dir: meson.current_build_dir() + 'pandas/_config')
#py.install_sources('__init__.py',
#                    pure: false,
#                    subdir: 'pandas/__init__.py')
