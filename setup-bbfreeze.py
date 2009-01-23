import os, sys
sys.path.insert(0,os.path.abspath(os.path.join('.','src')))

from bbfreeze import Freezer
f = Freezer("BoPunk-0.1", includes=("_strptime",))
f.addScript("src/mainwindow.py", gui_only=False)
f.addModule("BoPunk")
f()    # starts the freezing process