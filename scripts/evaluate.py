#!/usr/bin/python
import csv
import logging
import os
import sys

from sklearn.metrics import confusion_matrix

import log

MAX_VALUE = ['cora']
THRESHOLD = 0.5

H_PRED = 0
H_SIZE = 1
H_OPEN = 2
H_FILE = 3
H_PRIOR = 4
H_TRUTH = 5
H_FORCE = 6

TRUE = 'true'
FALSE = 'false'

def align_data(predictions, labels, closed):
    truth = []
    pred = []
    label_dict = {}
    pred_dict = {}

    for label in labels:
        label_dict[(label[0], label[1])] = label[2]

    for prediction in predictions: 
        pred_dict[(prediction[0], prediction[1])] = prediction[2]

    if closed:
        for label in pred_dict:
            pred.append(float(pred_dict[label]))
            if label in label_dict:
                truth.append(float(label_dict[label]))
            else:
                truth.append(0.0)
    else:
        for label in label_dict:
            truth.append(float(label_dict[label]))
            if label in pred_dict:
                pred.append(float(pred_dict[label]))
            else:
                pred.append(0.0)

    return truth, pred

def evaluate_f1(predictions, labels):
    b_predictions = []
    b_labels = []

    for prediction in predictions:
        if prediction > THRESHOLD:
            b_predictions.append(1)
        else:
            b_predictions.append(0)
    for label in labels:
        if label > THRESHOLD:
            b_labels.append(1)
        else:
            b_labels.append(0)

    tn, fp, fn, tp = confusion_matrix(b_labels, b_predictions).ravel()

    # Accuracy
    if tp + tn + fp + fn == 0.0:
        accuracy = 0.0
    else:
        accuracy = (tp + tn) / (tp + tn + fp + fn)

    # Precision
    if tp + fp == 0.0:
        precision = 0.0
    else:
        precision = tp / (tp + fp)

    # Recall
    if tp + fn == 0.0:
        recall = 0.0
    else:
        recall = tp / (tp + fn)

    # F1
    if precision + recall == 0.0:
        f1 = 0.0
    else:
        f1 = 2 * (precision * recall) / (precision + recall)

    return [accuracy, precision, recall, f1]

def load_file(filename):
    output = []

    with open(filename, 'r') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for line in reader:
            output.append(line)

    return output

def max_results(results):
    results.sort(key=lambda k: (int(k[0]), -float(k[2])))
    current = None
    for result in results:
        if current != result[0]:
            current = result[0]
            if float(result[2]) > THRESHOLD:
                result[2] = 1
            else:
                result[2] = 0
        else:
            result[2] = 0

    return results

def load_psl(psl_dir, experiment):
    results_dir = os.path.join(psl_dir, 'inferred-predicates')

    # TODO (connor) make general, currently expects only one file in inferred-predicates
    for results_filename in os.listdir(results_dir):
        results_path = os.path.join(results_dir, results_filename)
        results = load_file(results_path)

    if experiment in MAX_VALUE:
        results = max_results(results)

    return results

def load_tuffy(tuffy_dir, experiment):
    results_path = os.path.join(tuffy_dir, 'results.txt')
    results_tmp = load_file(results_path)
    results = []

    for result in results_tmp:
        predicate = result[1][result[1].find("(")+1:result[1].find(")")].replace(' ', '').split(',')
        predicate.append(result[0])
        results.append(predicate)

    if experiment in MAX_VALUE:
        results = max_results(results)

    return results

def load_truth(experiment, split_dir):
    helper_path = os.path.join('tuffy', experiment, 'predicates.txt')
    helper = load_file(helper_path)
    truth_filename = None

    for predicate in helper:
        if predicate[H_TRUTH] == TRUE:
            truth_filename = predicate[H_FILE]

    truth = load_file(os.path.join(split_dir, truth_filename))
    return truth

def main(experiment, evaluation, psl_dir, tuffy_dir):
    truth_split_dir = os.path.join(psl_dir, experiment, 'data', experiment, '0', 'eval')
    ground_truth = load_truth(experiment, truth_split_dir)

    psl_split_dir = os.path.join(psl_dir, experiment, 'data', experiment, '0', 'eval')
    psl_data = load_psl(psl_split_dir, experiment)

    tuffy_split_dir = os.path.join(tuffy_dir, experiment, 'data', experiment, '0', 'eval')
    tuffy_data = load_tuffy(tuffy_split_dir, experiment)

    if experiment in ['cora']:
        psl_truth, psl_data = align_data(psl_data, ground_truth, True)
        tuffy_truth, tuffy_data = align_data(tuffy_data, ground_truth, True)
    else:
        psl_truth, psl_data = align_data(psl_data, ground_truth, False)
        tuffy_truth, tuffy_data = align_data(tuffy_data, ground_truth, False)

    if evaluation in ['f1', 'accuracy', 'precision', 'recall']:
        psl_results = evaluate_f1(psl_data, psl_truth)
        tuffy_results = evaluate_f1(tuffy_data, tuffy_truth)

    print(psl_results)
    print(tuffy_results)

def _load_args(args):
    executable = args.pop(0)
    if (len(args) != 4 or ({'h', 'help'} & {arg.lower().strip().replace('-', '') for arg in args})):
        print("USAGE: python3 %s <experiment> <evaluation> <psl_dir> <tuffy_dir>" % (executable), file = sys.stderr)
        sys.exit(1)

    experiment = args.pop(0)
    evaluation = args.pop(0)
    psl_dir = args.pop(0)
    tuffy_dir = args.pop(0)

    return experiment, evaluation, psl_dir, tuffy_dir

if (__name__ == '__main__'):
    experiment, evaluation, psl_dir, tuffy_dir = _load_args(sys.argv)
    main(experiment, evaluation, psl_dir, tuffy_dir)
