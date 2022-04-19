''' Converts all .ui files in the bin directory to .py files.
    os.path.relpath() is used to ensure the path mentioned at
    the top of the .py files is relative to the root directory.
    Run this script everytime you make a change to a .ui file. '''

import os
import glob

CWD = os.path.dirname(os.path.realpath(__file__))
for ui_file in glob.glob(os.path.join(CWD, 'bin', '*.ui')):
    path = os.path.relpath(ui_file, CWD)
    os.system(f'pyuic5 -x {path} -o {path[:-3]}.py')
