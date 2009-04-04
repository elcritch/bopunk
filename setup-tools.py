#!/usr/bin/env python
from setuptools import setup, find_packages

APP = ['src/bopunk.py']
DATA_FILES = []

setup(
    name='BoPunk',
    version='0.5',
    description='Graphical Interface to manage BoPunk firmware',
    author='BocoLabs',
    author_email='support@bocolab.org',
    url='http://www.bocolab.org',
    
    package_dir = {'': 'src'},
    scripts = ['src/bopunk'],
    packages=find_packages('src'),
    include_package_data = True,
    
    # Extra PyPI metadata
    long_description="""\
    Graphical Interface to manage BoPunk firmware
    """,
    classifiers=[
      "License :: OSI Approved :: GNU General Public License (GPL)",
      "Programming Language :: Python",
      "Development Status :: 4 - Beta",
      "Intended Audience :: Users",
      "Topic :: Internet",
    ],
    keywords='device firmware bopunk bocolab',
    license='GPL',
    install_requires=[
    'setuptools',
    'PyQt4',
    ],
)


# package_dir = {'': 'src'},
# packages=find_packages('src'),
