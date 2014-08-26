# -*- coding: utf-8 -*-

# This file is part of music-autotagging-msordo.
#
# music-autotagging-msordo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# music-autotagging-msordo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with music-autotagging-msordo.  If not, see <http://www.gnu.org/licenses/>.

# Written by Mohamed Sordo (@neomoha)
# Email: mohamed ^dot^ sordo ^at^ gmail ^dot^ com
# Website: http://msordo.weebly.com

import os
import numpy as np

def load_metadata(metadata_filename):
    metadata = dict()
    with open(metadata_filename) as f:
        for line in f:
            trackid, trackpath, tag, weight = line.strip().split("\t")
            metadata.setdefault(trackid, []).append((tag, float(weight)))
    return metadata

def load_output(output_filename):
    output = dict()
    with open(output_filename) as f:
        for line in f:
            trackid, featurespath, tag, weight = line.strip().split("\t")
            output.setdefault(trackid, []).append((tag, float(weight)))
    return output

def get_TP_FP_FN(ground_truth, prediction):
    '''
    Returns number of True Positives (TP), False Positives (FP) and False Negatives (FN) given two lists of strings
    '''
    TP = len(set(ground_truth).intersection(set(prediction)))
    FP = len(set(prediction).difference(set(ground_truth)))
    FN = len(set(ground_truth).difference(set(prediction)))
    return TP, FP, FN

def get_TP_FP_TN_FN(ground_truth, prediction, vocab):
    '''
    Returns number of True Positives (TP), False Positives (FP), True Negatives (TN) and False Negatives (FN) given two lists of strings
    '''
    TP = len(set(ground_truth).intersection(set(prediction)))
    FP = len(set(prediction).difference(set(ground_truth)))
    FN = len(set(ground_truth).difference(set(prediction)))
    aux1 = set(vocab).difference(set(ground_truth))
    aux2 = set(vocab).difference(set(prediction))
    TN = len(aux1.intersection(aux2))
    return TP, FP, TN, FN

def precision(TP, FP):
    if (TP+FP) == 0:
        return 0.0
    return float(TP) / (TP+FP)

def recall(TP, FN):
    if (TP+FN) == 0:
        return 0.0
    return float(TP) / (TP+FN)

def true_positive_rate(TP, FN):
    return recall(TP, FN)

def false_positive_rate(FP, TN):
    if (FP+TN) == 0:
        return 0.0
    return float(FP)/(FP+TN)

def fscore(P, R, beta=1):
    denom = (beta**2*P+R)
    if denom == 0:
        return 0.0
    return (1+beta**2)*(float(P*R)/denom)

def precision_at_N(ground_truth, prediction, N):
    '''
    Returns Precision-at-N given two lists of strings
    '''
    TP = len(set(ground_truth).intersection(prediction[:N]))
    return float(TP)/N

def AUC(xdata, ydata):
	"""Given a list of x coordinates and a list of y coordinates, returns
	the area under the curve they define."""
	x = (np.roll(xdata, -1) - xdata)[:-1]
	y = (np.roll(ydata, -1) + ydata)[:-1]/2
	return sum(map(lambda x, y: x*y, x, y))

def per_track_binary_relevance_measures(metadata, output):
    '''
    Calculates the average per-track Precision, Recall and F-measure given a Ground Truth (metadata) and a Prediction (output)
    '''
    avg_P, avg_R, avg_F = [], [], []
    for trackid, tags in metadata.iteritems():
        gt = [t for t,w in tags]
        pred = [t for t,w in output[trackid]]
        TP, FP, FN = get_TP_FP_FN(gt, pred)
        avg_P.append(precision(TP, FP))
        avg_R.append(recall(TP, FN))
        avg_F.append(fscore(avg_P[-1], avg_R[-1]))
        #print avg_P[-1], avg_R[-1], avg_F[-1]
        #print "########################"
    avg_P, avg_R, avg_F = np.array(avg_P), np.array(avg_R), np.array(avg_F)
    print "------------------Per-Track Binary Relevance------------------------"
    print "Precision: (mean=%.3f), (std=%.3f), (median=%.3f)" % (np.mean(avg_P), np.std(avg_P), np.median(avg_P))
    print "Recall: (mean=%.3f), (std=%.3f), (median=%.3f)" % (np.mean(avg_R), np.std(avg_R), np.median(avg_R))
    print "F-score: (mean=%.3f), (std=%.3f), (median=%.3f)" % (np.mean(avg_F), np.std(avg_F), np.median(avg_F))
    
def per_tag_binary_relevance_measures(metadata, output):
    '''
    Calculates the average per-tag Precision, Recall and F-measure given a Ground Truth (metadata) and a Prediction (output)
    '''
    avg_P, avg_R, avg_F = [], [], []
    gt_tags = dict()
    for trackid, tags in metadata.iteritems():
        for tag, weight in tags:
            gt_tags.setdefault(tag, []).append(trackid)
    pred_tags = dict()
    for trackid, tags in output.iteritems():
        for tag, weight in tags:
            pred_tags.setdefault(tag, []).append(trackid)
    for tag in gt_tags.iterkeys():
        gt = gt_tags[tag]
        if tag in pred_tags:
            pred = pred_tags[tag]
        else:
            pred = []
        TP, FP, FN = get_TP_FP_FN(gt, pred)
        avg_P.append(precision(TP, FP))
        avg_R.append(recall(TP, FN))
        avg_F.append(fscore(avg_P[-1], avg_R[-1]))
        #print avg_P[-1], avg_R[-1], avg_F[-1]
        #print "########################"
    avg_P, avg_R, avg_F = np.array(avg_P), np.array(avg_R), np.array(avg_F)
    print "------------------Per-Tag Binary Relevance------------------------"
    print "Precision: (mean=%.3f), (std=%.3f), (median=%.3f)" % (np.mean(avg_P), np.std(avg_P), np.median(avg_P))
    print "Recall: (mean=%.3f), (std=%.3f), (median=%.3f)" % (np.mean(avg_R), np.std(avg_R), np.median(avg_R))
    print "F-score: (mean=%.3f), (std=%.3f), (median=%.3f)" % (np.mean(avg_F), np.std(avg_F), np.median(avg_F))

def per_track_affinity_measures(metadata, output):
    '''
    Calculates the average per-track Precision-at-N and Area under the ROC curve given a Ground Truth (metadata) and a Prediction (output)
    '''
    avg_prec_at_N = dict()
    avg_auc_roc = []
    vocab = dict([(t, 1) for trid, tags in metadata.iteritems() for t,w in tags]).keys()
    for trackid, tags in metadata.iteritems():
        gt = [t for t,w in tags]
        sorted_output = sorted(output[trackid], key=lambda x: x[1], reverse=True)
        pred = [t for t,w in sorted_output]
        for N in range(3,16,3):
            avg_prec_at_N.setdefault(N, []).append(precision_at_N(gt, pred, N))
        FPR, TPR = [], []
        for i in xrange(1, len(pred)+1):
            TP, FP, TN, FN = get_TP_FP_TN_FN(gt, pred[:i], vocab)
            FPR.append(false_positive_rate(FP, TN))
            TPR.append(true_positive_rate(TP, FN))
        avg_auc_roc.append(AUC(np.array(FPR), np.array(TPR)))
    print "------------------Per-Track Affinity------------------------"
    for N, avg_P in sorted(avg_prec_at_N.iteritems()):
        avg_P = np.array(avg_P)
        print "Precision-at-%d: (mean=%.3f), (std=%.3f), (median=%.3f)" % (N, np.mean(avg_P), np.std(avg_P), np.median(avg_P))
    avg_auc_roc = np.array(avg_auc_roc)
    print "AUC-ROC: (mean=%.3f), (std=%.3f), (median=%.3f)" % (np.mean(avg_auc_roc), np.std(avg_auc_roc), np.median(avg_auc_roc))

def per_tag_affinity_measures(metadata, output):
    '''
    Calculates the average per-tag Area under the ROC curve given a Ground Truth (metadata) and a Prediction (output)
    '''
    vocab = metadata.keys()
    avg_auc_roc = []
    gt_tags = dict()
    for trackid, tags in metadata.iteritems():
        for tag, weight in tags:
            gt_tags.setdefault(tag, []).append(trackid)
    pred_tags = dict()
    for trackid, tags in output.iteritems():
        for tag, weight in tags:
            pred_tags.setdefault(tag, []).append((trackid, weight))
    print "------------------Per-Tag Affinity------------------------"
    for tag in sorted(gt_tags.iterkeys()):
        gt = gt_tags[tag]
        if tag in pred_tags:
            sorted_output = sorted(pred_tags[tag], key=lambda x: x[1], reverse=True)
            pred = [t for t,w in sorted_output]
        else:
            pred = []
        FPR, TPR = [], []
        for i in xrange(1, len(pred)+1):
            TP, FP, TN, FN = get_TP_FP_TN_FN(gt, pred[:i], vocab)
            FPR.append(false_positive_rate(FP, TN))
            TPR.append(true_positive_rate(TP, FN))
        avg_auc_roc.append(AUC(np.array(FPR), np.array(TPR)))
        print "%s\t%.6f" % (tag, avg_auc_roc[-1])
    avg_auc_roc = np.array(avg_auc_roc)
    print "AUC-ROC: (mean=%.3f), (std=%.3f), (median=%.3f)" % (np.mean(avg_auc_roc), np.std(avg_auc_roc), np.median(avg_auc_roc))
    
def binary_relevance_measures(metadata_filename, output_filename):
    metadata = load_metadata(metadata_filename)
    output = load_output(output_filename)
    per_track_binary_relevance_measures(metadata, output)
    per_tag_binary_relevance_measures(metadata, output)

def affinity_measures(metadata_filename, output_filename):
    metadata = load_metadata(metadata_filename)
    output = load_output(output_filename)
    per_track_affinity_measures(metadata, output)
    per_tag_affinity_measures(metadata, output)

if __name__ == '__main__':
    metadata_filename = "test/majorminer_metadata__fold3.tsv"
    output_filename = "test/majorminer_output_binary__fold3.tsv"
    binary_relevance_measures(metadata_filename, output_filename)
    
    output = "test/majorminer_output_affinity__fold3.tsv"
    affinity_measures(metadata_filename, output_filename)
    