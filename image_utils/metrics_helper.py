# from jeniffer

def evaluate(y, pred):
    """Evaluates  the performance of a model

    Args:
    y: true values
    y_pred: predicted values of the model

    Returns:
    dictionary: dictionary with all calculated values
    """
    y = np.asarray(y.to_frame())
    classes = np.greater(pred, 0.5).astype(int)
    tp = np.count_nonzero(classes * y)
    tn = np.count_nonzero((classes - 1) * (y - 1))
    fp = np.count_nonzero(classes * (y - 1))
    fn = np.count_nonzero((classes - 1) * y)

    # Calculate accuracy, precision, recall and F1 score.
    accuracy = (tp + tn) / (tp + fp + fn + tn)
    precision = tp / (tp + fp)
    sensitivity = tp / (tp + fn)
    specificity = tn / (tn + fp)
    bal_acc = (sensitivity + specificity) / 2
    fpr = fp / (fp + tn)
    fnr = fn / (tp + fn)
    fmeasure = (2 * precision * sensitivity) / (precision + sensitivity)
    mse = mean_squared_error(classes, y)
    mcc = matthews_corrcoef(y, classes)
    youden = sensitivity + specificity - 1
    AUC = roc_auc_score(y, pred)
    hamming = hamming_loss(y, classes)
    kappa = cohen_kappa_score(y, classes)
    gmean = sqrt(sensitivity * specificity)

    ret = {'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn,
           'acc': accuracy, 'bal_acc': bal_acc, 'sens': sensitivity, 'spec': specificity, 'fnr': fnr, 'fpr': fpr,
           'fmeas': fmeasure, 'mse': mse, 'youden': youden, 'mcc': mcc, 'auc': AUC,
           'hamming': hamming, 'cohen_kappa': kappa, 'gmean': gmean}

    return ret
