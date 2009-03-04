from distutils.core import setup
import os, sys, shutil

pth = os.path.abspath("src")
sys.path.insert(1,pth)
print "path",pth 
version = "0.4"
dist_pth = "./build/"

setup(
    name = "BoPunk",
    version = version,
    description = "BoPunk Firmware Management Script",
    scripts = ['src/runner'],
    packages=['BoPunk'],
    package_dir={'BoPunk': 'src/BoPunk'},
    # package_data={'BoPunk': ['data/*.dat']},
)



