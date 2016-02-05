__author__ = 'stamylew'

import numpy as np
from python_functions.handle_h5.handle_h5 import read_h5
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score, roc_curve, accuracy_score, precision_score, recall_score

#prepare data for quality assesment

def unswap(data, ax1 = 0, ax2 = 2):
    """ unswap prediction data axises that probably have been swapped during the batch prediction
    :param data: prediction data
    :param ax1: first axis to be swapped
    :param ax2: second axis to be swapped
    :return:
    """

    copy = np.copy(data)
    assert np.size(np.shape(data)) == 3
    swapped_data = np.swapaxes(copy, ax1, ax2)
    return swapped_data


def adjust_predict(predict):
    """ extract data cube, swap dimensions
    :param predict: prediction unswapped if necessary
    """

    print np.size(np.shape(predict))
    assert np.size(np.shape(predict)) == 5
    squeezed_data = predict[0,:,:,:,0]
    # plt.imshow(squeezed_data[0])
    # plt.show()
    adjusted_predict = unswap(squeezed_data)
    # plt.imshow(adjusted_predict[0])
    # plt.show()
    return adjusted_predict


def save_images(gt, predict, outpath = "/home/stamylew/tests", slice = 0):
    """ save 2D slice images of the gt and predicition data for visual comparison
    :param gt:      groundtruth data
    :param predict: prediction data
    :param outpath: path where to save the slice images
    :param slice:   which slice in x axis direction is picked
    """

    plt.imsave(outpath + "/gt.png", gt[slice])
    plt.imsave(outpath + "/predict.png", predict[slice])


def exclude_ignore_label(gt, predict, ignore_label = 0):
    """ exclude the ignore label given in the ground truth from the ground truth and the prediction
    :param gt:      ground truth
    :param predict: prediction
    :return:    relevant_gt is the groundtruth without the pixels that have been labeled with the ignore label,
                same for the predicition data
    """
    #check
    plt.imshow(predict[0])
    plt.imshow(gt[0])

    relevant_data = gt != ignore_label
    relevant_gt = gt[relevant_data]
    relevant_predict = predict[relevant_data]
    return relevant_gt, relevant_predict


def binarize_predict(predict, threshold = 0.5, neg_label = 2, pos_label = 1):
    """
    :param predict:     prediction in probabilities
    :param threshold:   threshold value for probabilities
    :return:    binarized prediction data
    """

    neg_class = predict <= threshold
    neg_class_map = neg_class * neg_label

    pos_class = predict > threshold
    pos_class_map = pos_class * pos_label

    binarized_predict = neg_class_map + pos_class_map
    return binarized_predict


# calculate quality values
def apr(gt, predict, pos_label = 1):
    """ calculate accuracy, precision and recall
    :param gt:          groundtruth with ignore label excluded
    :param predict:     prediction data adjusted, binarized and with ignore label excluded
    :param pos_label:   label belonging to the positive class
    :return:    accuracy, precision, recall
    """
    # TODO: Find optimal threshold from roc curve
    predict = binarize_predict(predict)


    #sklearn quality
    sklearn_acc = accuracy_score(gt, predict)
    sklearn_prec = precision_score(gt, predict)
    sklearn_rec = recall_score(gt, predict)

    #auc_score
    auc_score = roc_auc(gt, predict)


    # #myquality
    # #accuray
    # comparison = gt == predict
    # accuracy = float(np.sum(comparison)) / gt.size
    # sod = gt.size
    # print
    # print "my accuracy:", accuracy
    #
    #
    # #precision
    # retrieved_pos = predict == pos_label
    # pos_predict = predict[retrieved_pos]
    # pos_gt = gt[retrieved_pos]
    # true_pos = pos_predict == pos_gt
    # norp = float(np.sum(retrieved_pos))
    # false_pos = pos_predict != pos_gt
    # notp = float(np.sum(true_pos))
    # nofp = float(np.sum(false_pos))
    # precision = notp / (notp + nofp)
    #
    # print
    # print "my precision:", precision
    # print
    #
    # #recall
    # retrieved_neg = predict != 1
    # neg_predict = predict[retrieved_neg]
    # neg_gt = gt[retrieved_neg]
    # false_neg = neg_predict != neg_gt
    # nofn = float(np.sum(false_neg))
    #
    # recall = notp / (notp + nofn)
    #
    # print
    # print "my recall:", recall
    # print

    return sklearn_acc, sklearn_prec, sklearn_rec, auc_score

def get_quality_values(gt, predict):
    adjusted_predict = adjust_predict(predict)
    ignore_label_excluded = exclude_ignore_label(gt, adjusted_predict)
    quality_values = apr(ignore_label_excluded[0], ignore_label_excluded[1])
    return quality_values

def adjust_labels(data):
    right_label = data == 1
    adjusted_label = right_label * 1
    return adjusted_label

def roc_auc(gt, predict):
    """ get the roc curve and the auc score
    """

    agt = adjust_labels(gt)
    auc_score = roc_auc_score(agt,predict)
    return auc_score

def draw_roc_curve(gt, predict):
    agt = adjust_labels(gt)
    fpr, tpr, thresholds = roc_curve(agt, predict)
    return fpr, tpr, thresholds



if __name__ == '__main__':
    predict = read_h5("/home/stamylew/test_folder/p_cache/100p_cube2_probs.h5", "exported_data")
    gt = read_h5("/home/stamylew/volumes/groundtruth/trimaps/100p_cube2_trimap_t_05.h5", "data")
    print get_quality_values(gt, predict)
    # adjusted_predict = adjust_predict(predict)
    # print
    # print np.unique(adjusted_predict)
    # relevant_data = exclude_ignore_label(gt, adjusted_predict)
    #
    # roc_predict = unswap(predict[0,:,:,:,0])
    # roc_relevant_data = exclude_ignore_label(gt, roc_predict)
    # print "auc_score:", roc_auc(roc_relevant_data[0], roc_relevant_data[1])
    #
    #
    # acc, prec, rec, = apr(relevant_data[0], relevant_data[1])
    # print
    # print "apr:", acc, prec, rec
    print "done"