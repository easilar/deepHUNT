# from jeniffer
import numpy as np
from keras import backend as K
from sklearn import metrics as sk_metrics

class evaluate:
    def __init__(self, y_true, y_pred):

        self.y_true = y_true
        self.y_pred = y_pred

        y_pred_pos = K.round(K.clip(y_pred, 0, 1))
        y_pred_neg = 1 - y_pred_pos
        y_pos = K.round(K.clip(y_true, 0, 1))
        y_neg = 1 - y_pos

        self.tp = K.sum(y_pos * y_pred_pos)
        self.tn = K.sum(y_neg * y_pred_neg)
        self.fp = K.sum(y_neg * y_pred_pos)
        self.fn = K.sum(y_pos * y_pred_neg)

        self.precision = self.tp / (self.tp + self.fp)
        self.sensitivity = self.tp / (self.tp + self.fn)
        self.specificity = self.tn / (self.tn + self.fp)

def precision(y_true, y_pred):
    calc_obj = evaluate(y_true, y_pred)
    return calc_obj.precision

def accuracy(y_true, y_pred):
    calc_obj = evaluate(y_true, y_pred)
    return (calc_obj.tp + calc_obj.tn) / (calc_obj.tp + calc_obj.fp + calc_obj.fn + calc_obj.tn) 

def sensitivity(y_true, y_pred):
    calc_obj = evaluate(y_true, y_pred)
    return calc_obj.sensitivity

def specificity(y_true, y_pred):
    calc_obj = evaluate(y_true, y_pred)
    return calc_obj.specificity

def bal_acc(y_true, y_pred):
    calc_obj = evaluate(y_true, y_pred)
    return (calc_obj.sensitivity + calc_obj.specificity) / 2

def fpr(y_true, y_pred):
    calc_obj = evaluate(y_true, y_pred)
    return calc_obj.fp / (calc_obj.fp + calc_obj.tn)

def fnr(y_true, y_pred):
    calc_obj = evaluate(y_true, y_pred)
    return calc_obj.fn / (calc_obj.tp + calc_obj.fn)

def fmeasure(y_true, y_pred):
    calc_obj = evaluate(y_true, y_pred)
    return (2 * calc_obj.precision * calc_obj.sensitivity) / (calc_obj.precision + calc_obj.sensitivity)

def mse(y_true, y_pred):
    calc_obj = evaluate(y_true, y_pred)
    return None

def mcc(y_true, y_pred):
    calc_obj = evaluate(y_true, y_pred)
    mcc_numerator = (calc_obj.tp * calc_obj.tn - calc_obj.fp * calc_obj.fn)
    mcc_denominator = K.sqrt((calc_obj.tp + calc_obj.fp) * (calc_obj.tp + calc_obj.fn) * (calc_obj.tn + calc_obj.fp) * (calc_obj.tn + calc_obj.fn))
    return mcc_numerator / (mcc_denominator + K.epsilon()) 

def youden(y_true, y_pred):
    calc_obj = evaluate(y_true, y_pred)
    return calc_obj.sensitivity + calc_obj.specificity -1

def AUC(y_true, y_pred):
    #calc_obj = evaluate(y_true, y_pred)
    return sk_metrics.roc_auc_score(K.eval(y_true), K.eval(y_pred))

def hamming(y_true, y_pred):
    calc_obj = evaluate(y_true, y_pred)
    return None

def kappa(y_true, y_pred):
    calc_obj = evaluate(y_true, y_pred)
    return None

def gmean(y_true, y_pred):
    calc_obj = evaluate(y_true, y_pred)
    return K.sqrt(calc_obj.sensitivity * calc_obj.specificity)

