import os
import sys
from distutils.ccompiler import new_compiler
from setuptools import setup

# Hack to silence atexit traceback in newer python versions.
try:
    import multiprocessing  # noqa
except ImportError:
    pass

# For now, GreenletProfiler includes a patched version of Sumer Cip's yappi.
# The original yappi source is at https://bitbucket.org/sumerc/yappi, and my
# fork is at https://bitbucket.org/emptysquare/gappi. The patched source is
# included in this project in the _vendorized_yappi directory, and the
# following extension configuration is adapted from yappi's setup.py.
user_macros = []
user_libraries = []
compile_args = []
link_args = []

if os.name == 'posix' and sys.platform != 'darwin':
    compiler = new_compiler()
    if compiler.has_function('timer_create', libraries=('rt',)):
        user_macros.append(('LIB_RT_AVAILABLE', '1'))
        user_libraries.append('rt')

classifiers = """\
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Development Status :: 1 - Planning
Natural Language :: English
Programming Language :: Python :: 2
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.2
Programming Language :: Python :: 3.3
Operating System :: MacOS :: MacOS X
Operating System :: Unix
Programming Language :: Python
Programming Language :: Python :: Implementation :: CPython
"""

description = 'Greenlet-aware Python performance profiler, built on yappi.'
long_description = open("README.rst").read()
packages = []
if 'nosetests' in sys.argv:
    packages.append('test')

setup(
    name='GreenletProfiler',
    version='0.1.1',
    packages=packages,
    ext_modules=[],
    # Include yappi.py along with our own GreenletProfiler.py.
    py_modules=[
        'GreenletProfiler',
    ],
    description=description,
    long_description=long_description,
    author='A. Jesse Jiryu Davis',
    author_email='jesse@emptysquare.net',
    url='http://github.com/ajdavis/GreenletProfiler/',
    license='http://www.apache.org/licenses/LICENSE-2.0',
    classifiers=filter(None, classifiers.split('\n')),
    keywords='greenlet gevent profiler asynchronous',
    install_requires=['greenlet', 'yappi'],
    # use python setup.py nosetests to test
    setup_requires=['nose'],
    test_suite='nose.collector',
    zip_safe=False)
