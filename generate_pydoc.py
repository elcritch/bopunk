#!/usr/bin/env python
import os, sys, glob, shutil
from os import path

sys.path.append('src/')
os.chdir('./src/')

print "Build Directory: ", os.path.abspath(os.curdir)
print """
Documentation Compiler: Note pydoc differs than javadoc in many respects, 
also compilation is different. This scripts provides a simple wrapper to
generate html files, but it does not include system libraries which are 
used in BoPunk.
"""

def build(doc):
    """builds ui interface files into python files"""
    command = "pydoc -w %s"%(doc)
    print "Running:", command 
    os.system(command)

docs = []

# add initial files
docs.extend( "./%s"%p for p in glob.glob('*.py'))
docs.append('BoPunk')

# now recursively add modules, dumb algorithm
def find_doc(path):
    print "path:",path
    files = glob.glob(os.path.join(path,'*'))
    
    dirs = [ d for d in files if os.path.isdir(d) ]
    docs.extend( d.replace(os.sep,'.').replace('.py','') for d in dirs )
    docs.extend( f.replace(os.sep,'.').replace('.py','') for f in files if f.endswith('.py') )
    for d in dirs:
        find_doc(d)

find_doc('BoPunk')

for doc in docs:
    build(doc)

try:
    os.mkdir('../html/')
except:
    pass


if not os.path.isdir('../html'):
    exit(1)

for html in glob.glob("*.html"):
    shutil.move(html,'../html')

