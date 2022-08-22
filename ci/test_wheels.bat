PYTHON_VERSION=$(python -c "import platform; print(platform.python_version())")
if $IS_32_BIT (exit 0) # No way to test Windows 32-bit (no Docker image)
docker pull python:$PYTHON_VERSION-windowsservercore
docker run -v %cd%:c:\pandas python:$PYTHON_VERSION-windowsservercore \
cmd.exe "python --version &&
        pip install pytz six numpy python-dateutil &&
        pip install --find-links=pandas/pandas/dist --no-index pandas &&
        python -c 'import pandas as pd; 
                    print(pd.__version__);
                    pandas.test(extra_args=["-m not clipboard and not single_cpu", "--skip-slow", "--skip-network", "--skip-db", "-n=2"]);
                    pandas.test(extra_args=["-m not clipboard and single_cpu", "--skip-slow", "--skip-network", "--skip-db"])'"