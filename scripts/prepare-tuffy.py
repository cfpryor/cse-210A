#!/usr/bin/python
import csv
import os
import sys

CLI = 'cli'
HELPER = 'predicates.txt'
#HasCat   2  open  hasCat_truth.txt  false

def load_helper(helper_file):
    with open(helper_file, 'r') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            print(row)

def main(tuffy_dir, psl_dir):
    print(tuffy_dir, psl_dir)
    load_helper(os.path.join(tuffy_dir, CLI, HELPER))

def _load_args(args):
    executable = args.pop(0)
    if (len(args) != 2 or ({'h', 'help'} & {arg.lower().strip().replace('-', '') for arg in args})):
        print("USAGE: python3 %s <tuffy_dir> <psl_dir>" % (executable), file = sys.stderr)
        sys.exit(1)

    tuffy_dir = args.pop(0)
    psl_dir = args.pop(0)

    return tuffy_dir, psl_dir

if (__name__ == '__main__'):
    tuffy_dir, psl_dir = _load_args(sys.argv)
    main(tuffy_dir, psl_dir)
