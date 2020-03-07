#!/usr/bin/python
import csv
import logging
import os
import sys

import log

DATA = 'data'
HELPER = 'predicates.txt'
OUTFILE = 'evidence.db'

EVAL = 'eval'
LEARN = 'learn'

FALSE = 'false'
TRUE = 'true'

H_PRED = 0
H_SIZE = 1
H_OPEN = 2
H_FILE = 3
H_PRIOR = 4
H_TRUTH = 5

def write_data(data, path):
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, OUTFILE), 'w') as out_file:
        out_file.write('\n'.join(data))

def load_split(predicate, split):
    size = int(predicate[H_SIZE])
    pred = predicate[H_PRED]
    filename = predicate[H_FILE]
    prior = predicate[H_PRIOR]
    truth = predicate[H_TRUTH]

    # TODO(connor) handle truth files
    if truth == TRUE:
        return []

    if not os.path.isfile(os.path.join(split, filename)):
        logging.error("No file named %s in %s" % (filename, split))
        return

    tuffy_data = []
    with open(os.path.join(split, filename), 'r') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')

        for line in reader:
            value = 1.0

            if prior != FALSE:
                value = float(prior)
            elif len(line) < size:
                value = float(line[-1])

            if value == 1.0:
                tuffy_data.append(pred + '(' + ', '.join(line[0:size]) + ')')
            else:
                tuffy_data.append(str(value) + ' ' + pred + '(' + ', '.join(line[0:size]) + ')')

    return tuffy_data

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

    helper = load_helper(os.path.join(tuffy_experiment, HELPER))

    if experiment not in os.listdir(os.path.join(psl_experiment, DATA)):
        logging.error("No data directory named %s in %s" % (experiment, os.path.join(psl_experiment, DATA)))
        return

    for split_dir in os.listdir(os.path.join(psl_experiment, DATA, experiment)):
        if not os.path.isdir(os.path.join(psl_experiment, DATA, experiment, split_dir)):
            continue

        for phase in [EVAL, LEARN]:
            p_split = os.path.join(psl_experiment, DATA, experiment, split_dir, phase)
            t_split = os.path.join(tuffy_experiment, DATA, experiment, split_dir, phase)
            data = []
            if not os.path.isdir(p_split):
                logging.error("No eval/learn in %s" % (os.path.join(psl_experiment, DATA, experiment, p_split_dir)))
                continue

            for predicate in helper:
                data = data + load_split(predicate, p_split)
            write_data(data, t_split)

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
