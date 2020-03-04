#!/usr/bin/python
import sys

def main(tuffy_dir, psl_dir):
    print(tuffy_dir, psl_dir)

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
