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


if len(sys.argv) == 1: sys.exit(1)


IS_COMPILED = getattr(sys, 'frozen', False)
SCRIPT_PATH = sys.executable if IS_COMPILED else os.path.realpath(__file__)
CWD = os.path.dirname(SCRIPT_PATH)


parser = argparse.ArgumentParser()
parser.add_argument('--zip', help='The zip file to unpack')
parser.add_argument('--destination', default=CWD, help='The destination to unpack the zip file')
parser.add_argument('--cmd', help='The command to run after unpacking')
parser.add_argument('--lock-files', nargs='*', default=None, help='File(s) that must be deleted before unpacking, typically PID files')
parser.add_argument('--add-to-report', nargs='*', default=None, help='Data to always include at the top of the report file')
parser.add_argument('--report-path', default=os.path.join(CWD, 'update_report.txt'), help='Path/name of the report file that will be generated')
parser.add_argument('--delete', action=argparse.BooleanOptionalAction, default=False, help='Delete the zip file after successfully unpacking')
args = parser.parse_args()


try: os.remove(args.report_path)
except: pass


if args.lock_files:
    for lock_file in args.lock_files:
        while os.path.exists(lock_file):
            try: os.remove(lock_file)
            except PermissionError: time.sleep(0.1)
else: time.sleep(1)


try:
    with ZipFile(args.zip, 'r') as zip: zip.extractall(args.destination)
    report_text = 'SUCCESS'
except Exception as error:
    report_text = f'{type(error)} - {error}'


with open(args.report_path, 'w') as report:
    for line in args.add_to_report: report.write(f'{line}\n')
    report.write(f'{args.zip}\n')
    if report_text: report.write(report_text)


if args.delete: os.remove(args.zip)
if args.cmd: subprocess.Popen(args.cmd)
