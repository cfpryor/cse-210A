#!/usr/bin/python
import csv
import logging
import os
import sys

from sklearn.metrics import confusion_matrix
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import classification_report

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

def evaluate_mse(predictions, labels):
    return [mean_squared_error(labels, predictions)]

def evaluate_catigorical(predictions, labels):
    return [accuracy_score(labels, predictions), precision_score(labels, predictions)]

def evaluate_f1(predictions, labels, negative = False):
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

    if negative:
        for index in range(len(b_predictions)):
            if b_predictions[index] == 0:
                b_predictions[index] = 1
            else:
                b_predictions[index] = 0
            if b_labels[index] == 0:
                b_labels[index] = 1
            else:
                b_labels[index] = 0

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

def align_data(predictions, labels, closed):
    truth = []
    pred = []
    label_dict = {}
    pred_dict = {}
    obs_dict = {}

    for label in labels:
        label_dict[(label[0], label[1])] = label[2]

    for prediction in predictions:
        pred_dict[(prediction[0], prediction[1])] = prediction[2]

    if closed:
        for label in label_dict:
            if label not in pred_dict:
                continue
            truth.append(float(label_dict[label]))
            pred.append(float(pred_dict[label]))
    else:
        for label in label_dict:
            truth.append(float(label_dict[label]))
            if label in pred_dict:
                pred.append(float(pred_dict[label]))
            else:
                pred.append(0.0)

    return truth, pred


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
    return_list = []
    for result in results:
        if current != result[0]:
            current = result[0]
            return_list.append([result[0], result[1], '1'])
        else:
            return_list.append([result[0], result[1], '0'])

    return return_list

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

def gather_system_info(path):
    return_list = []
    time = 'Elapsed (wall clock) time (h:mm:ss or m:ss):'
    memory = 'Maximum resident set size (kbytes):'
    with open(path, 'r') as file:
        for line in file:
            if time in line:
                return_list.append(line.split(time)[-1].strip())
            if memory in line:
                return_list.append(line.split(memory)[-1].strip())

    return return_list

def main(experiment, evaluation, psl_dir, tuffy_dir):
    results = []

    header = ['PPL', 'experiment','split']
    if evaluation in ['f1', 'accuracy', 'precision', 'recall']:
        header = header + ['accuracy', 'precision', 'recall', 'f1', 'n_accuracy', 'n_precision', 'n_recall', 'n_f1']
    else:
        header.append(evaluation)

    results.append("\t".join(header))

    for split in os.listdir(os.path.join(psl_dir, experiment, 'data', experiment)):
        if split == 'tmp' or not os.path.isdir(os.path.join(psl_dir, experiment, 'data', experiment, split)):
            continue
        truth_split_dir = os.path.join(psl_dir, experiment, 'data', experiment, split, 'eval')
        ground_truth = load_truth(experiment, truth_split_dir)

        psl_split_dir = os.path.join(psl_dir, experiment, 'data', experiment, split, 'eval')
        psl_data = load_psl(psl_split_dir, experiment)

        tuffy_split_dir = os.path.join(tuffy_dir, experiment, 'data', experiment, split, 'eval')
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

            psl_results = psl_results + evaluate_f1(psl_data, psl_truth, negative = True)
            tuffy_results = tuffy_results + evaluate_f1(tuffy_data, tuffy_truth, negative = True)

        if evaluation in ['mse']:
            psl_results = evaluate_mse(psl_data, psl_truth)
            tuffy_results = evaluate_mse(tuffy_data, tuffy_truth)

        if evaluation in ['cat', 'catigorical']:
            psl_results = evaluate_catigorical(psl_data, psl_truth)
            tuffy_results = evaluate_catigorical(tuffy_data, tuffy_truth)

        tuffy_results = tuffy_results + gather_system_info(os.path.join(tuffy_split_dir, 'out.err'))
        psl_results = psl_results + gather_system_info(os.path.join(psl_split_dir, 'out.err'))

        psl_results = ['PSL', experiment, split] + psl_results
        tuffy_results = ['Tuffy', experiment, split] + tuffy_results
        results.append("\t".join([str(i) for i in psl_results]))
        results.append("\t".join([str(i) for i in tuffy_results]))

    with open('results.csv', 'w') as out_file:
        out_file.write("\n".join(results))

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
