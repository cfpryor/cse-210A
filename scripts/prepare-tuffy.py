#!/usr/bin/python
import csv
import logging
import os
import sys

import log

CLI = 'cli'
DATA = 'data'
HELPER = 'predicates.txt'

EVAL = 'eval'
LEARN = 'learn'

H_PRED = 0
H_SIZE = 1
H_OPEN = 2
H_FILE = 3
H_PRIOR = 4

def load_split(predicate, split):
    if not os.path.isfile(os.path.join(split, predicate[H_FILE])):
        logging.error("No file named %s in %s" % (predicate[H_FILE], split))
        return

    with open(os.path.join(split, predicate[H_FILE]), 'r') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for line in reader:
            print(line)

def load_helper(helper_file):
    helper = []

    with open(helper_file, 'r') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for line in reader:
            helper.append(line)

    return helper

def main(tuffy_dir, psl_dir, experiment):
    # Initialize logging level, switch to DEBUG for more info.
    log.initLogging(logging_level = logging.INFO)

    logging.info("Working on experiment %s" % (experiment))

    tuffy_experiment = os.path.join(tuffy_dir, experiment)
    psl_experiment = os.path.join(psl_dir, experiment)

    helper = load_helper(os.path.join(tuffy_experiment, CLI, HELPER))

    if experiment not in os.listdir(os.path.join(psl_experiment, DATA)):
        logging.error("No data directory named %s in %s" % (experiment, os.path.join(psl_experiment, DATA)))
        return

    for split_dir in os.listdir(os.path.join(psl_experiment, DATA, experiment)):
        if not os.path.isdir(os.path.join(psl_experiment, DATA, experiment, split_dir)):
            continue

        for phase in [EVAL, LEARN]:
            split = os.path.join(psl_experiment, DATA, experiment, split_dir, phase)
            if not os.path.isdir(split):
                logging.error("No eval/learn in %s" % (os.path.join(psl_experiment, DATA, experiment, split_dir)))
                continue

            for predicate in helper:
                data = load_split(predicate, split)

def _load_args(args):
    executable = args.pop(0)
    if (len(args) != 3 or ({'h', 'help'} & {arg.lower().strip().replace('-', '') for arg in args})):
        print("USAGE: python3 %s <tuffy_dir> <psl_dir> <experiment>" % (executable), file = sys.stderr)
        sys.exit(1)

    tuffy_dir = args.pop(0)
    psl_dir = args.pop(0)
    experiment = args.pop(0)

    return tuffy_dir, psl_dir, experiment

if (__name__ == '__main__'):
    tuffy_dir, psl_dir, experiment = _load_args(sys.argv)
    main(tuffy_dir, psl_dir, experiment)
