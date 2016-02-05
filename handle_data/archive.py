# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 14:54:50 2015

@author: stamylew
"""

import os
from os.path import isfile, join
from python_functions.handle_h5.handle_h5 import read_h5, save_h5
from python_functions.handle_data.predict_class import predict_class
from python_functions.quality.quality import get_quality_values
import numpy as np
import matplotlib.pyplot as plt

def archive_qdata(p_cache, gt, qdata, repeat, outpath, slices):
    """ archive quality data
    :param p_cache:     folder in which the batch prediction results are stored
    :param gt:          groundtruth
    :param outpath:     folder in which quality data is stored
    :param threshold:   threshold used on the prediction data
    :param slice:       which 2D slice in x direction of the data is saved as image
    """

    #get predicition file
    prob_file = [x for x in os.listdir(p_cache) if ("probs" in x)]
    predict_data = read_h5(p_cache + "/" + prob_file[0], "exported_data")

    #save quality data
    gt_data = read_h5(gt)
    #q_data = np.zeros((repeats, 4), dtype = np.float64)

    predict = predict_class(gt_data, predict_data)
    apr = get_quality_values(gt_data, predict_data)
    qdata[repeat] = predict.quality
    print
    print "quality:"
    print "accuracy:", predict.quality[0]
    print "precision:", predict.quality[1]
    print "recall:", predict.quality[2]
    print "roc auc score:", predict.quality[3]
    #save_h5(q_data, outpath, "a_p_r_auc", None)

    #show and save prediction and gt images
    for slice in slices:
        im_outpath = outpath.split(".")[-2]
        predict_im_outpath = im_outpath + "_slice_" + str(slice) + ".png"
        gt_im_outpath = im_outpath + "_slice_" + str(slice) + "_gt.png"
        plt.imsave(predict_im_outpath, predict.adjusted_predict[slice])
        plt.imsave(gt_im_outpath, gt_data[slice])

    #save roc curve
    fpr, tpr, threshold = predict.roc_curve
    plt.figure()
    plt.plot(fpr, tpr)
    plt.savefig(im_outpath + "roc_curve_test" + str(repeat) + ".png")


if __name__ == '__main__':
    x = "/home/stamylew/test_folder/p_cache"
    gt = "/home/stamylew/volumes/trimaps/50cube2_trimap_t_05.h5"
    outpath = "/home/stamylew/test_folder/output_t_05/delme/test.h5"
    archive_qdata(x, gt, outpath)
    print "done"








# def archive_quality_data(p_cache, gt, outpath, threshold):
#     """archive the quality data of each batch prediction iteration
#     """
#
#     #get and sort probability files
#     x = p_cache
#     only_probs = [f for f in os.listdir(x) if (isfile(join(x,f))) and ("probs" in f)]
#     only_probs.sort()
#
#     #create array for quality data
#     quality_data = np.zeros((len(only_probs),3), dtype = np.float64)
#     g = read_h5(gt)
#
#     for i in range(1, len(only_probs)):
#         r = read_h5(x + only_probs[i], "exported_data")
#         r = adjust_predict(r, threshold)
#
#         #save prediction image
#
#         plt.imsave(outpath.split(".")[-2] + "_" + str(i) + ".png", r[0])
#
#         #save quality values
#         c = predict_class(g, r)
#         quality_data[i-1,:] = c.return_quality()
#
#     r = read_h5(x + only_probs[0], "exported_data")
#     r = adjust_predict(r, threshold)
#
#     #save last loop image
#     plt.imsave(outpath.split(".")[-2] + "_" + str(len(only_probs)) + ".png", r[0])
#
#     #save last loop quality data
#     c = predict_class(g, r)
#     quality_data[len(only_probs)-1, :] = c.return_quality()
#
#     print quality_data
#     save_h5(quality_data, outpath, "test")
