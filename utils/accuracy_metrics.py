import pandas as pd
from scipy.stats import spearmanr
import numpy as np

'''
A Accuracy Metrics that evaluates the accuracy of a prediction based on spearman correlation, f1 scores, and r-sqaured

Arguments:

    predictions:                a list of predictions with values of real numbers (Must have the same length as gold_labels)
    gold_labels:                a list of gold labels with values of -1, 0, or 1 
    neutral_lower(optional):    a lower bound for neutral sentiment, below which a prediction is classified as negative
    neutral_upper(optional):    an upper bound for neutral sentiment, above which a prediction is classified as positive

Attributes:

    correlation:                spearman rho correlation
    p_val:                      spearman p value
    negative_f1:                f1 score for the negative class
    neutral_f1:                 f1 score for the neutral class
    positive_f1:                f1 score for the positive class
    r_squared:                  r-squared for the predictions

Methods:

    result_dict:                Returns a dictionary of class attributes mapped to their values

Example:

    a = [-0.98, -0.4, -0.3, 0.2, 0.45, 0.88]
    b = [-1, -1, -1, 0, 0, 1]   
    metrics = AccuracyMetrics(a, b)
    print(metrics.positive_f1)

    acc_dict = metrics.result_dict()
    print(acc_dict['r_squared'])


'''

class AccuracyMetrics():

    

    def __init__(self, predictions, gold_labels, neutral_lower=-0.33, neutral_upper=0.33):

        if len(predictions) != len(gold_labels):
            raise InputListsDiffLengthsError

        self.predictions = np.array(predictions)
        self.gold_labels = np.array(gold_labels)
        self.neutral_lower = neutral_lower
        self.neutral_upper = neutral_upper

        self.map_predictions(self.predictions)
        self.correlation, self.pval = spearmanr(self.predictions, self.gold_labels)

        self.negative_f1 = self.compute_f1(-1)
        self.neutral_f1 = self.compute_f1(0)
        self.positive_f1 = self.compute_f1(1)

        self.r_squared = self.compute_r_squared()

    def result_dict(self):

        accuracy_metrics = {
            "spearman_correlation": self.correlation,
            "spearman_pval": self.pval,
            "negative_f1": self.negative_f1,
            "neutral_f1": self.neutral_f1,
            "positive_f1": self.positive_f1,
            "r_squared": self.r_squared
        }
        return accuracy_metrics

    def map_predictions(self, predictions):
        for itr in range(len(predictions)):
            if predictions[itr] <= self.neutral_lower:
                predictions[itr] = -1
            elif predictions[itr] <= self.neutral_upper:
                predictions[itr] = 0
            else:
                predictions[itr] = 1


    def compute_spearman(self):
        observation_length = len(self.predictions)
        diff_sqr_sum = 0
        for i in range(observation_length):
            diff_sqr_sum += (self.predictions[i] - self.gold_labels[i]) ** 2
            # print("d2 is ", (predictions[i] - gold_labels[i]) ** 2)

        spearman_corr = 1 - ((6.0 * diff_sqr_sum) / (observation_length * (observation_length**2 - 1)))
        return spearman_corr

    def compute_precision(self, p_class):
        tp = 0.0
        fp = 0
        for i in range(len(self.predictions)):
            if self.predictions[i] == p_class and self.gold_labels[i] == p_class:
                tp += 1
            elif self.predictions[i] == p_class and self.gold_labels[i] != p_class:
                fp += 1
        return tp/(tp+fp)

    def compute_recall(self, r_class):
        tp = 0.0
        fn = 0
        for i in range(len(self.predictions)):
            if self.predictions[i] == r_class and self.gold_labels[i] == r_class:
                tp += 1
            elif self.predictions[i] != r_class and self.gold_labels[i] == r_class:
                fn += 1
        return tp/(tp+fn)

    def compute_f1(self, f_class):
        precision = self.compute_precision(f_class)
        recall = self.compute_recall(f_class)

        return (2 * precision * recall) / (precision + recall)

    def compute_r_squared(self):
        correlation_matrix = np.corrcoef(self.predictions, self.gold_labels)
        correlation = correlation_matrix[0,1]
        r_squared = correlation**2
        return r_squared

class InputListsDiffLengthsError(Exception):
        def __init__(self):
            self.message = "The Predictions and Gold Labels have different lengths!"
            super(Exception, self).__init__(self.message)
    


