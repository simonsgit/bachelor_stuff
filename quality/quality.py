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


def get_segmentation(predict, pmin=0.5, minMemb=10, minSeg=10, sigMin=6, sigWeights=1, sigSmooth=0.1, cleanCloseSeeds=True,
                     returnSeedsOnly=False, edgeLengths=None,nodeFeatures=None, nodeSizes=None, nodeLabels=None, nodeNumStop=None,
                     beta=0, metric='l1', wardness=0.2, out=None):
    """ Get segmentation through watershed and agglomerative clustering
    :param predict: prediction map
    :return: segmentation map
    """
    #use watershed and save superpixels map
    super_pixels = wsDtSegmentation(predict, pmin, minMemb, minSeg, sigMin, sigWeights, cleanCloseSeeds, returnSeedsOnly)
    # seeds = wsDtSegmentation(predict, pmin, minMemb, minSeg, sigMin, sigWeights, cleanCloseSeeds, True)
    # save_h5(seeds, "/home/stamylew/delme/seeds.h5", "data")
    print
    print "#Nodes in superpixels", len(np.unique(super_pixels))
    # save_h5(super_pixels, "/home/stamylew/delme/super_pixels.h5", "data")

    #smooth prediction map
    probs = vf.gaussianSmoothing(predict, sigSmooth)
     # save_h5(probs, "/home/stamylew/delme/probs.h5", "data")

    #make grid graph
    grid_graph = vg.gridGraph(super_pixels.shape, False)

    grid_graph_edge_indicator = vg.edgeFeaturesFromImage(grid_graph, probs)

    #make region adjacency graph
    rag = vg.regionAdjacencyGraph(grid_graph, super_pixels)

    #accumulate edge features from grid graph node map
    edge_weights = rag.accumulateEdgeFeatures(grid_graph_edge_indicator)
    edge_weights_tag = "mean of the probabilities"

    #do agglomerative clustering

    labels = vg.agglomerativeClustering(rag, edge_weights, edgeLengths, nodeFeatures, nodeSizes,
            nodeLabels, nodeNumStop, beta, metric, wardness, out)

    #segmentation data
    wsDt_data = np.zeros((8,1))
    wsDt_data[:,0] = (pmin, minMemb, minSeg, sigMin, sigWeights, sigSmooth, cleanCloseSeeds, returnSeedsOnly)
    agglCl_data = edge_weights_tag, str(edgeLengths), str(nodeFeatures), str(nodeSizes), str(nodeLabels), str(nodeNumStop), str(beta), metric, str(wardness), str(out)

    #project labels back to data
    segmentation = rag.projectLabelsToBaseGraph(labels)
    print "#nodes in segmentation", len(np.unique(segmentation))
    # save_h5(segmentation, "/home/stamylew/delme/segmap.h5", "data", None)

    return segmentation, super_pixels, wsDt_data, agglCl_data


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

def rand_index_variation_of_information(segmentation, dense_gt):
    ri =  skl.randIndex(segmentation.flatten().astype(np.uint32), dense_gt.flatten().astype(np.uint32), True)
    voi = skl.variationOfInformation(segmentation.flatten().astype(np.uint32), dense_gt.flatten().astype(np.uint32), True)
    return ri, voi


def get_quality_values(predict, gt, dense_gt):
    """
    """
    adjusted_predict = adjust_predict(predict)
    # save_h5(adjusted_predict, "/home/stamylew/delme/prob.h5", "data")
    relevant_predict, relevant_gt = exclude_ignore_label(adjusted_predict, gt)
    acc, pre, rec = accuracy_precision_recall(relevant_predict, relevant_gt)
    auc_score = calculate_roc_auc_score(relevant_predict, relevant_gt)
    no_of_true_pos, no_of_false_pos = true_and_false_pos(relevant_predict, relevant_gt)
    no_of_true_neg, no_of_false_neg = true_and_false_neg(relevant_predict, relevant_gt)

    print "#nodes in dense gt", len(np.unique(dense_gt))
    segmentation, super_pixels, wsDt_data, agglCl_data = get_segmentation(adjusted_predict)
    save_h5(segmentation, "/home/stamylew/delme/segmap.h5", "data", None)
    ri_data = skl.randIndex(segmentation.flatten().astype(np.uint32), dense_gt.flatten().astype(np.uint32), True)
    voi_data = skl.variationOfInformation(segmentation.flatten().astype(np.uint32), dense_gt.flatten().astype(np.uint32), True)
    sp_ri = skl.randIndex(super_pixels.flatten().astype(np.uint32), dense_gt.flatten().astype(np.uint32), True)
    sp_voi = skl.variationOfInformation(super_pixels.flatten().astype(np.uint32), dense_gt.flatten().astype(np.uint32), True)
    print
    print "super pixels values", (sp_ri, sp_voi)
    print
    print "segmentation values", (ri_data, voi_data)
    return acc, pre, rec, auc_score, ri_data, voi_data, no_of_true_pos, no_of_false_pos, no_of_true_neg, no_of_false_neg, \
           wsDt_data, agglCl_data
    # return acc, pre, rec, auc_score, no_of_true_pos, no_of_false_pos, no_of_true_neg, no_of_false_neg, \
    #        wsDt_data, agglCl_data


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
    acc, prec, rec, auc_score, ri, voi, tp, fp, tn, fn, wsDt_data, agglCl_data = get_quality_values(predict_data, gt_data, dense_gt_data)
    measurements = {"accuracy":acc, "precision":prec, "recall":rec, "auc score":auc_score, "rand index":ri,
                    "variation of information":voi, "true positives":tp, "false positives":fp, "true negatives":tn,
                    "false negatives":fn}

    # acc, prec, rec, auc_score, tp, fp, tn, fn, wsDt_data, agglCl_data = get_quality_values(predict_data, gt_data, dense_gt_data)
    # measurements = {"accuracy":acc, "precision":prec, "recall":rec, "auc score":auc_score,
    #                  "true positives":tp, "false positives":fp, "true negatives":tn,
    #                 "false negatives":fn}

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


    save_h5(wsDt_data, outpath, "segmentation/wsDt data", None)
    save_h5([agglCl_data], outpath, "segmentation/agglCl data", None)
    fpr, tpr, threshold = draw_roc_curve(predict_data, gt_data)
    plt.figure()
    plt.plot(fpr, tpr)
    plt.savefig(im_outpath + "roc_curve_test.png")

def test_wsDt_agglCl_configs(predict_path, dense_gt_path, pmin=0.5, minMemb=10, minSeg=10, sigMin=2, sigWeights=2, sigSmooth=0.1):
    """
    :param predict_path:
    :param dense_gt_path:
    :param pmin:
    :param minMemb:
    :param minSeg:
    :param sigMin:
    :param sigWeights:
    :param sigSmooth:
    :return:
    """

    #get rand index and variation of information
    predict_data = read_h5(predict_path)
    adjusted_predict_data = adjust_predict(predict_data)
    dense_gt_data = read_h5(dense_gt_path)
    seg, sup = get_segmentation(adjusted_predict_data,pmin,minMemb,minSeg,sigMin,sigWeights,sigSmooth)
    ri, voi = rand_index_variation_of_information(seg, dense_gt_data)
    print "ri, voi", ri, voi

    config = predict_path.split("/")[-2]
    filename = config + "_" + predict_path.split("/")[-1]
    outpath_folder = "/home/stamylew/test_folder/q_data/wsDt_agglCl_tests/"
    outpath = outpath_folder + filename

    key = "sigMin_" + str(sigMin) + "_sigWeights_" + str(sigWeights) + "_sigSmooth_" + str(sigSmooth)

    if not os.path.exists(outpath):
        print "Output h5 file did not exist."
        data = np.zeros((1,2))
        data[0,0] = ri
        data[0,1] = voi
        save_h5(data, outpath, key, None)
    else:
        old_data = read_h5(outpath, key)
        data = np.zeros((1,2))
        data[0,0] = ri
        data[0,1] = voi
        new_data = np.vstack((old_data, data))
        save_h5(new_data, outpath, key, None)


def redo_segmentation(block_path, dense_gt_path, minMemb, minSeg, sigMin, sigWeights, sigSmooth, edgeLengths=None,
                      nodeFeatures=None, nodeSizes=None, nodeLabels=None, nodeNumStop=None, beta=0, metric='l1',
                      wardness=0.2, out=None):
    folder_list = [f for f in os.listdir(block_path) if not os.path.isfile(os.path.join(block_path,f)) and ("figure" not in f)]
    print "folder_list", folder_list

    for f in folder_list:
        folder_path = os.path.join(block_path, f)
        prob_file = [h for h in os.listdir(folder_path) if "probs" in h]
        prob_file_path = os.path.join(folder_path,prob_file[0])
        print
        print
        print prob_file_path
        predict_data = read_h5(prob_file_path)
        adjusted_predict_data = adjust_predict(predict_data)
        dense_gt_data = read_h5(dense_gt_path)
        nodes_in_dgt = len(np.unique(dense_gt_data))
        print "#nodes in dense gt", nodes_in_dgt
        pmin = 0.5
        seg, sup, wsDt_data, agglCl_data = get_segmentation(adjusted_predict_data, pmin, minMemb, minSeg, sigMin, sigWeights,
                                                            sigSmooth,True,False, edgeLengths,nodeFeatures, nodeSizes,
                                                            nodeLabels, nodeNumStop,beta, metric, wardness, out)
        nodes_in_seg = len(np.unique(seg))
        nodes_in_sup = len(np.unique(sup))
        ri, voi = rand_index_variation_of_information(seg, dense_gt_data)

        outpath = folder_path + "_redone_segmentation.h5"
        key = "pmin_"+ str(pmin) + "_minMemb_" + str(minMemb)+ "_minSeg_"+ str(minSeg) +"_sigMin_" + str(sigMin) + "_sigWeights_" + str(sigWeights) \
              + "_sigSmooth_" + str(sigSmooth) + "_nodeNumStop_" + str(nodeNumStop)
        save_h5(seg, folder_path + "_segmentation.h5", key)
        save_h5(sup, folder_path + "_super_pixels.h5", key)
        seg_data = np.zeros((2,3))
        seg_data[0,0] = ri
        seg_data[0,1] = voi
        seg_data[1,0] = nodes_in_dgt
        seg_data[1,1] = nodes_in_sup
        seg_data[1,2] = nodes_in_seg
        save_h5(seg_data, outpath, key, None)

if __name__ == '__main__':
    # predict_path1 = "/home/stamylew/test_folder/q_data/100p_cube1_t05/n_1_l_10000_w_none/100p_cube1_probs.h5"
    # predict1 = read_h5(predict_path1)
    #
    # predict_path2 = "/home/stamylew/test_folder/q_data/200p_cube3/n_5_l_10000_w_none/200p_cube3_probs.h5"
    # predict2 = read_h5(predict_path2)
    #
    # gt_path1 = "/home/stamylew/volumes/groundtruth/trimaps/100p_cube1_trimap_t_10.h5"
    # gt1 = read_h5(gt_path1)
    #
    # gt_path2 = "/home/stamylew/volumes/groundtruth/trimaps/200p_cube3_trimap_t_15.h5"
    # gt2 = read_h5(gt_path2)
    #
    # dense_gt_path1 = "/home/stamylew/volumes/groundtruth/dense_groundtruth/100p_cube1_dense_gt.h5"
    # dense_gt1 = read_h5(dense_gt_path1)
    #
    # dense_gt_path2 = "/home/stamylew/volumes/groundtruth/dense_groundtruth/200p_cube3_dense_gt.h5"
    # dense_gt2 = read_h5(dense_gt_path2)
    #
    # outpath = "/home/stamylew/delme/n_1_l_10000_w_none/seg_data_test.h5"
    #
    # save_quality_values(predict_path1, gt_path1, dense_gt_path1, outpath, (0,49,99))
    # print
    # seg, sup = get_segmentation(adjust_predict(predict1))
    # ri, voi = rand_index_variation_of_information(seg, dense_gt1)
    # print ri, voi


    block_path = "/home/stamylew/test_folder/q_data/100p_cube3_random"
    gt_path = "/home/stamylew/volumes/groundtruth/trimaps/100p_cube3_trimap_t_10.h5"
    dense_gt_path = "/home/stamylew/volumes/groundtruth/dense_groundtruth/100p_cube3_dense_gt.h5"
    slices = (0, 49, 99)
    redo_segmentation(block_path, dense_gt_path, minMemb=10, minSeg=10, sigMin=2, sigWeights=2, sigSmooth=0.1,edgeLengths=None,
                      nodeFeatures=None, nodeSizes=None, nodeLabels=None, nodeNumStop=None, beta=0, metric='l1', wardness=0.2,
                      out=None)
    print "done"
