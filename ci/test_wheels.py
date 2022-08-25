import platform
import os
import sys
import subprocess
py_ver = platform.python_version()
is_32_bit = (os.getenv('IS_32_BIT') == "true")
print(f"IS_32_BIT is {is_32_bit}")
if os.name == "nt":
    if is_32_bit:
        sys.exit(0) # No way to test Windows 32-bit(no docker image)
    print(f"Pulling docker image to test Windows 64-bit Python {py_ver}")
    subprocess.run(f"docker pull python:{py_ver}-windowsservercore", check=True)
    pandas_base_dir = os.path.join(os.path.dirname(__file__), '..')
    print(f"pandas project dir is {pandas_base_dir}")
    subprocess.run(f'cd {pandas_base_dir} && docker run -v "`pwd`:`pwd`" -w `pwd` '
                   f'python:{py_ver}-windowsservercore ci/test_wheels_windows.bat', check=True, shell=True)
else:
    import pandas as pd
    pandas.test(extra_args=['-m not clipboard and not single_cpu', '--skip-slow', '--skip-network', '--skip-db', '-n=2'])
    pandas.test(extra_args=['-m not clipboard and single_cpu', '--skip-slow', '--skip-network', '--skip-db'])
