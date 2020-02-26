from setuptools import setup
import sys
from pathlib import Path

if sys.version_info.major != 3:
    raise RuntimeError('cstr requires Python 3')


setup(name = 'cstr',
      version = "1.0",
      description = 'Colored str',
      long_description = Path('README.md').read_text('utf-8'),
      url = 'https://github.com/mvfki/cstr',
      author = 'Yichen Wang',
      author_email = 'wangych@bu.edu',
      packages = ['cstr'],
      package_dir = {'cstr':'cstr'}
      )

