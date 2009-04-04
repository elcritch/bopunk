from distutils.core import setup
# from setuptools import find_packages as setuptools_find

import os, sys, shutil

# pth = os.path.abspath("src")
# sys.path.insert(1,pth)
# packages = setuptools_find('src/')
packages = ['BoPunk', 'BoPunk.lib', 'BoPunk.ui', 'BoPunk.lib.serial']

print "packages:",packages


setup(
    name = "BoPunk",
    version='0.5',
    description='Graphical Interface to manage BoPunk firmware',
    author='BocoLabs',
    author_email='support@bocolabs.org',
    url='http://www.bocolabs.org',    
    scripts = ['src/bopunk'],
    packages=packages,
    package_dir={'': 'src'},
    # package_data={'BoPunk': ['data/*.dat']},
)



