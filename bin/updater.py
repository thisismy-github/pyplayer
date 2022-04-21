''' Generic utility script for extracting a .zip file.
    Intended for use as part of an automatic-update utility.

    WARNING: When compiled, relative paths will not be
             consistent. Only pass in absolute paths.

    thisismy-github 3/19/22 '''

import os
import sys
import time
import argparse
import subprocess
from zipfile import ZipFile


# constants
IS_COMPILED = getattr(sys, 'frozen', False)
SCRIPT_PATH = sys.executable if IS_COMPILED else os.path.realpath(__file__)
CWD = os.path.dirname(SCRIPT_PATH)


# parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('zip', help='The zip file to unpack')
parser.add_argument('-d', '--destination', default=CWD, help='The destination to unpack the zip file')
parser.add_argument('-c', '--cmd', help='The command to run after unpacking')
parser.add_argument('-l', '--lock-files', nargs='*', default=None, help='File(s) that must be deleted before unpacking, typically PID files')
parser.add_argument('-a', '--add-to-report', nargs='*', default=[], help='Extra strings to include at the top of the report file')
parser.add_argument('-r', '--report-path', default=os.path.join(CWD, 'update_report.txt'), help='Path/name of the report file that will be generated')
parser.add_argument('-D', '--delete', action='store_true', help='Delete the zip file after unpacking (occurs even on failure)')
try: args = parser.parse_args()
except:         # if no arguments, print help and exit
    print('\n---\n')
    parser.print_help()
    print('\n---\n\n  You do not need to run this manually.\n'
          '\n  This is a utility script for extracting a .zip file, created for PyPlayer'
          '\n  but designed to be used as part of a general purpose auto-update utility.')
    input('\n  thisismy-github 3/19/22 | Press any key to exit... ')
    sys.exit(1)


# delete old report path if it exists
try: os.remove(args.report_path)
except: pass


# delete lock files if they exist, otherwise sleep one second
if args.lock_files:
    for lock_file in args.lock_files:
        while os.path.exists(lock_file):
            try: os.remove(lock_file)
            except PermissionError: time.sleep(0.1)
else: time.sleep(1)


# extract zip file and save outcome
try:
    with ZipFile(args.zip, 'r') as zip: zip.extractall(args.destination)
    report_text = 'SUCCESS'
except Exception as error:
    report_text = f'{type(error)} - {error}'


# write report
with open(args.report_path, 'w') as report:
    for line in args.add_to_report: report.write(f'{line}\n')
    report.write(f'{args.zip}\n')
    if report_text: report.write(report_text)


# delete zip file and run command
if args.delete: os.remove(args.zip)
if args.cmd: subprocess.Popen(args.cmd)
