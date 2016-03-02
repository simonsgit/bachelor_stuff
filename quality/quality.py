__author__ = 'stamylew'

import os
import numpy as np
import vigra.graphs as vg
import vigra.filters as vf
from python_functions.handle_h5.handle_h5 import read_h5, save_h5
import matplotlib.pyplot as plt
import skneuro.learning._learning as skl
from src.watershed.wsdt import wsDtSegmentation
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

    assert np.size(np.shape(predict)) == 5
    squeezed_data = predict[0,:,:,:,0]

    adjusted_predict = unswap(squeezed_data)

    return adjusted_predict


def save_images(predict, gt, outpath = "/home/stamylew/tests", slices = (0)):
    """ save 2D slice images of the gt and predicition data for visual comparison
    :param gt:      groundtruth data
    :param predict: prediction data
    :param outpath: path where to save the slice images
    :param slice:   which slice in x axis direction is picked
    """

    for slice in slices:
        plt.imsave(outpath + "/gt_slice_" + str(slice) + ".png", gt[slice])
        plt.imsave(outpath + "/predict_" + str(slice) + ".png", predict[slice])


def exclude_ignore_label(predict, gt, ignore_label = 0):
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
    return relevant_predict, relevant_gt


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
def accuracy_precision_recall(predict, gt, pos_label = 1):
    """ calculate accuracy, precision and recall
    :param gt:          groundtruth with ignore label excluded
    :param predict:     prediction data adjusted, binarized and with ignore label excluded
    :param pos_label:   label belonging to the positive class
    :return:    accuracy, precision, recall
    """

    bin_predict = binarize_predict(predict)

    #sklearn quality
    sklearn_acc = accuracy_score(gt, bin_predict)
    sklearn_prec = precision_score(gt, bin_predict)
    sklearn_rec = recall_score(gt, bin_predict)

    return sklearn_acc, sklearn_prec, sklearn_rec


def adjust_labels(data):
    """
    :param data: Trimap groundtruth
    :return: Membrane groundtruth
    """
    right_label = data == 1
    adjusted_label = right_label * 1
    return adjusted_label


def calculate_roc_auc_score(predict, gt):
    """ Get the roc curve and the auc score
    """
    adjusted_gt = adjust_labels(gt)

    auc_score = roc_auc_score(adjusted_gt, predict)
    return auc_score


def get_segmentation(predict, cleanCloseSeeds=True, returnSeedsOnly=False):
    """ Get segmentation through watershed and agglomerative clustering
    :param predict: prediction map
    :return: segmentation map
    """

    #use watershed and save superpixels map
    super_pixels = wsDtSegmentation(predict, 0.5, 4000, 10000, 2, 1, cleanCloseSeeds, returnSeedsOnly)
    print "#superpixels", len(np.unique(super_pixels))
    save_h5(super_pixels, "/home/stamylew/delme/super_pixels.h5", "data", None)

    #smooth prediction map
    probs = vf.gaussianSmoothing(predict, 0.1)

    save_h5(probs, "/home/stamylew/delme/probs.h5", "data", None)

    #make grid graph
    grid_graph = vg.gridGraph(super_pixels.shape, False)
    grid_graph_edge_indicator = vg.edgeFeaturesFromImage(grid_graph, probs)

    #make region adjacency graph
    rag = vg.regionAdjacencyGraph(grid_graph, super_pixels)

    #accumulate edge features from grid graph node map
    edge_weights = rag.accumulateEdgeFeatures(grid_graph_edge_indicator)

    #do agglomerative clustering
    labels = vg.agglomerativeClustering(rag, edge_weights, edgeLengths=None,nodeFeatures=None,nodeSizes=None,
            nodeLabels=None,nodeNumStop=None,beta=0,metric='l1',wardness=0.2,out=None)

    #project labels back to data
    segmentation = rag.projectLabelsToBaseGraph(labels)
    print "#nodes in segmentation", len(np.unique(segmentation))
    save_h5(segmentation, "/home/stamylew/delme/segmap.h5", "data", None)

    return segmentation


def get_data_size(predict, gt):
    """
    """
    relevant_data = predict.size
    assert relevant_data == gt.size
    return relevant_data


def true_and_false_pos(predict, gt, pos_label=1):
    """
    """
    bin_predict = binarize_predict(predict)
    predicted_pos = bin_predict == pos_label
    only_pos_predicted = bin_predict[predicted_pos]
    only_pos_predicted_gt = gt[predicted_pos]

    true_pos = only_pos_predicted == only_pos_predicted_gt
    false_pos = only_pos_predicted != only_pos_predicted_gt

    no_of_true_pos = float(np.sum(true_pos))
    no_of_false_pos = float(np.sum(false_pos))

    return no_of_true_pos, no_of_false_pos


def true_and_false_neg(predict, gt, pos_label=1):
    bin_predict = binarize_predict(predict)
    predicted_neg = bin_predict != pos_label
    only_neg_predicted = bin_predict[predicted_neg]
    only_neg_predicted_gt = gt[predicted_neg]

    true_neg = only_neg_predicted == only_neg_predicted_gt
    false_neg = only_neg_predicted != only_neg_predicted_gt

    no_of_neg_pos = float(np.sum(true_neg))
    no_of_false_neg = float(np.sum(false_neg))

    return no_of_neg_pos, no_of_false_neg


def get_quality_values(predict, gt, dense_gt):
    """
    """
    adjusted_predict = adjust_predict(predict)
    save_h5(adjusted_predict, "/home/stamylew/delme/prob.h5", "data")
    relevant_predict, relevant_gt = exclude_ignore_label(adjusted_predict, gt)
    acc, pre, rec = accuracy_precision_recall(relevant_predict, relevant_gt)
    auc_score = calculate_roc_auc_score(relevant_predict, relevant_gt)
    data_size = get_data_size(relevant_predict, relevant_gt)
    no_of_true_pos, no_of_false_pos = true_and_false_pos(relevant_predict, relevant_gt)
    no_of_true_neg, no_of_false_neg = true_and_false_neg(relevant_predict, relevant_gt)

    print "#nodes in dense gt", len(np.unique(dense_gt))
    segmentation = get_segmentation(adjusted_predict)
    save_h5(segmentation, "/home/stamylew/delme/segmap.h5", "data", None)
    ri_data = skl.randIndex(segmentation.flatten().astype(np.uint32), dense_gt.flatten().astype(np.uint32), True)
    voi_data = skl.variationOfInformation(segmentation.flatten().astype(np.uint32), dense_gt.flatten().astype(np.uint32), True)


    return acc, pre, rec, auc_score, ri_data, voi_data, no_of_true_pos, no_of_false_pos, no_of_true_neg, no_of_false_neg


def draw_roc_curve(predict, gt):
    """
    """

    adjusted_predict = adjust_predict(predict)
    relevant_predict, relevant_gt = exclude_ignore_label(adjusted_predict, gt)
    agt = adjust_labels(relevant_gt)
    fpr, tpr, thresholds = roc_curve(agt, relevant_predict)
    return fpr, tpr, thresholds


def save_quality_values(predict_path, gt_path, dense_gt_path, outpath, slices):
    """
    """

    #read predict and groundtruth data
    predict_data = read_h5(predict_path, "exported_data")
    gt_data = read_h5(gt_path)
    dense_gt_data = read_h5(dense_gt_path)
    #all_quality_data = get_quality_values(predict_data, gt_data, dense_gt_data)


    #get quality values
    acc, prec, rec, auc_score, ri, voi, tp, fp, tn, fn = get_quality_values(predict_data, gt_data, dense_gt_data)
    measurements = {"accuracy":acc, "precision":prec, "recall":rec, "auc score":auc_score, "rand index":ri,
                    "variation of information":voi, "true positives":tp, "false positives":fp, "true negatives":tn,
                    "false negatives":fn}

    if not os.path.exists(outpath):
        print "Output h5 file did not exist."
        for measurement in measurements.iterkeys():
            key = "quality/" + measurement
            data = np.zeros((1,))
            data[0] = measurements[str(measurement)]
            save_h5(data, outpath, key, None)
    else:
        for measurement in measurements.iterkeys():
            key = "quality/" + measurement
            data = read_h5(outpath, key)
            new_data = np.vstack((data, measurements[measurement]))
            save_h5(new_data, outpath, key, None)

    for slice in slices:
        im_outpath = outpath.split(".")[-2]
        predict_im_outpath = im_outpath + "_slice_" + str(slice) + ".png"
        gt_im_outpath = im_outpath + "_slice_" + str(slice) + "_gt.png"
        plt.imsave(predict_im_outpath, adjust_predict(predict_data)[slice])
        plt.imsave(gt_im_outpath, gt_data[slice])

    fpr, tpr, threshold = draw_roc_curve(predict_data, gt_data)
    plt.figure()
    plt.plot(fpr, tpr)
    plt.savefig(im_outpath + "roc_curve_test.png")

if __name__ == '__main__':
    predict_path = "/home/stamylew/test_folder/p_cache/100p_cube2_probs.h5"
    predict = read_h5(predict_path)
    gt_path = "/home/stamylew/volumes/groundtruth/trimaps/100p_cube2_trimap_t_05.h5"
    gt = read_h5(gt_path)
    dense_gt_path = "/home/stamylew/volumes/groundtruth/dense_groundtruth/100p_cube2_dense_gt.h5"
    dense_gt = read_h5(dense_gt_path)
    outpath = "/home/stamylew/delme/n_1_l_10000_w_none/n_1_l_10000_w_none.h5"
    print get_quality_values(predict, gt, dense_gt)[4:6]
    #save_quality_values(predict_path, gt_path, dense_gt_path, outpath)

    print "done"
