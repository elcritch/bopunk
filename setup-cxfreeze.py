from cx_Freeze import setup, Executable
import os, sys
pth = os.path.abspath("src")
sys.path.insert(1,pth)
print "path",pth 

exe = Executable(
    "src/bopunk.py",
    includes=["BoPunk",'encodings'],
    path=[pth,],
    # targetDir="win-dist/"
)

setup(
        name = "BoPunk",
        version = "0.1",
        description = "BoPunk Firmware Management Script",
        executables = [exe],
)