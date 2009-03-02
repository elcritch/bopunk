from cx_Freeze import setup, Executable
import os, sys, shutil

pth = os.path.abspath("src")
sys.path.insert(1,pth)
print "path",pth 
version = 0.4
dist_pth = "./build/"
plugins_pth = r"C:\Python26\Lib\site-packages\PyQt4\plugins"

exe = Executable(
    "src/bopunk.py",
    includes=["BoPunk",'encodings'],
    path=[pth,],
    # copyDependentFiles=True,
    # targetDir="win-dist/"
)
execs = [exe]

buildOptions = dict(
        compressed = False,
        include_files=[(plugins_pth,"PyQt4/plugins/" ),('etc/qt.conf','qt.conf')]
        # includes = ["testfreeze_1", "testfreeze_2"],
        # path = sys.path + ["modules"]
)

setup(
        name = "BoPunk",
        version = "0.4",
        description = "BoPunk Firmware Management Script",
        options = dict(build_exe = buildOptions),
        executables = execs,
)



