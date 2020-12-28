from setuptools import setup

long_description=\
"""
Column.py
===============

This is a modern re-implementation of the venerable old ``column`` application
available on most Unix / Linux systems today.

Why re-implement this ancient tool?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


BSD ``column`` has been, for many, the tool that *almost* works for every
situation where we want to pretty-print a delimited table in textual form.
Unfortunately, it lacks two highly desirable features.

1. It has no option to right-justify columns instead of left-justifying them.
2. It has no option to specify the output delimiter, and has two spaces
   hardcoded.

Why not just modify the original code?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The original code is over 20 years old, is written in a cryptic C style which
does not lend itself to easy modification, and uses the  compiler-dependent
``wchar_t`` type is not actually wide enough for Unicode.

Example Usage & Output
^^^^^^^^^^^^^^^^^^^^^^

Consider the following  input file, named ``Sample.txt``::

    Benchmark,Count,Avg,StdDev,Median,Min,Max
    Core 1 to Core 2,3000000,125,431.937128,122,87,294738
    Core 1 to Core 3,3000000,128,58.326363,123,87,54313
    Core 2 to Core 1,3000000,129,323.379763,123,87,291708
    Core 2 to Core 3,3000000,128,45.726372,123,74,37875
    Core 3 to Core 1,3000000,128,42.615930,123,87,44093
    Core 3 to Core 2,3000000,128,172.090219,122,78,266052

Under traditional `column`, the output looks like this::

    $ column -t -s, Sample.txt 
    Benchmark         Count    Avg  StdDev      Median  Min  Max
    Core 1 to Core 2  3000000  125  431.937128  122     87   294738
    Core 1 to Core 3  3000000  128  58.326363   123     87   54313
    Core 2 to Core 1  3000000  129  323.379763  123     87   291708
    Core 2 to Core 3  3000000  128  45.726372   123     74   37875
    Core 3 to Core 1  3000000  128  42.615930   123     87   44093
    Core 3 to Core 2  3000000  128  172.090219  122     78   266052


With `column.py`, the output looks like this with default options::

    $ column.py -s, Sample.txt 
    Benchmark           Count  Avg      StdDev  Median  Min     Max
    Core 1 to Core 2  3000000  125  431.937128     122   87  294738
    Core 1 to Core 3  3000000  128   58.326363     123   87   54313
    Core 2 to Core 1  3000000  129  323.379763     123   87  291708
    Core 2 to Core 3  3000000  128   45.726372     123   74   37875
    Core 3 to Core 1  3000000  128   42.615930     123   87   44093
    Core 3 to Core 2  3000000  128  172.090219     122   78  266052
"""

setup(
  name="column.py",
  version='0.1.2',
  scripts=['column.py'],
  install_requires=['docopt>=0.2'],
  author="Henry Qin",
  author_email="root@hq6.me",
  description="A newer and more modern Unix column formatting tool.",
  long_description=long_description,
  platforms=["Any"],
  license="MIT",
  url="https://github.com/hq6/column"
)
