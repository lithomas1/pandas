#!/bin/bash
PROJECT_DIR="$1"
PYTHON_VERSION=$(python -c "import platform; print(platform.python_version())")
if [[ $IS_32_BIT == "true" ]]; then
    if [[ $RUNNER_OS == "Windows" ]]; then
      exit 0
    fi
    docker pull quay.io/pypa/manylinux2014_i686
    docker run --platform linux/386 -v $(pwd):/pandas quay.io/pypa/manylinux2014_i686 \
    /bin/bash -xc "python --version \
                   pip install pytz six numpy python-dateutil \
                   pip install --find-links=pandas/dist --no-index pandas \
                   python -c 'import pandas as pd;
print(pd.__version__);
pandas.test(extra_args=["-m not clipboard and not single_cpu", "--skip-slow", "--skip-network", "--skip-db", "-n=2"]);
pandas.test(extra_args=["-m not clipboard and single_cpu", "--skip-slow", "--skip-network", "--skip-db"])'"
else
    if [[ $RUNNER_OS == "Windows" ]]; then
      docker pull python:$PYTHON_VERSION-windowsservercore
      echo $PROJECT_DIR
      docker run -v "$PROJECT_DIR:c:\pandas\" python:$PYTHON_VERSION-windowsservercore /pandas/ci/test_wheels_windows.bat
    else
      python -c "import pandas; print(pandas.__version__);
pandas.test(extra_args=['-m not clipboard and not single_cpu', '--skip-slow', '--skip-network', '--skip-db', '-n=2']);
pandas.test(extra_args=['-m not clipboard and single_cpu', '--skip-slow', '--skip-network', '--skip-db'])"
    fi
fi
