__author__ = 'stamylew'

import os
import numpy as np
import vigra.graphs as vg
import vigra.filters as vf
from python_functions.handle_h5.handle_h5 import read_h5, save_h5
from python_functions.quality.quality import adjust_predict, get_segmentation, rand_index_variation_of_information, save_quality_values
import matplotlib.pyplot as plt
import skneuro.learning._learning as skl
from src.watershed.wsdt import wsDtSegmentation
from sklearn.metrics import roc_auc_score, roc_curve, accuracy_score, precision_score, recall_score

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
def redo_quality(block_path, dense_gt_path, minMemb, minSeg, sigMin, sigWeights, sigSmooth, edgeLengths=None,
                      nodeFeatures=None, nodeSizes=None, nodeLabels=None, nodeNumStop=None, beta=0, metric='l1',
                      wardness=0.2, out=None):

    #find all relevant folders in block path
    folder_list = [f for f in os.listdir(block_path) if not os.path.isfile(os.path.join(block_path,f))
                   and ("figure" not in f) and "redone" not in f]

    #create folder for redone quality
    outpath = block_path + "/redone_quality"
    if not os.path.exists(outpath):
        os.mkdir(outpath)

    dense_gt_data = read_h5(dense_gt_path)
    nodes_in_dgt = len(np.unique(dense_gt_data))

    #use prob file in every folder to create new quality in data in corresponding new folder
    for f in folder_list:


        #find prob file paths
        folder_path = os.path.join(block_path, f)
        prob_file = [h for h in os.listdir(folder_path) if "probs" in h]
        prob_file_path = os.path.join(folder_path,prob_file[0])

        #create new folders for new quality data
        config_name = prob_file_path.split("/")[-2]
        config_path = outpath +"/"+ config_name
        if not os.path.exists(config_path):
            os.mkdir(config_path)
        quality_data_path = config_path + "/" + config_name+".h5"

        #save new quality data in new folders
        save_quality_values(prob_file_path,gt_path, dense_gt_path, quality_data_path,slices,minMemb, minSeg, sigMin,
                            sigWeights, sigSmooth, edgeLengths, nodeFeatures, nodeSizes, nodeLabels, nodeNumStop, beta,
                            metric, wardness, out)


def redo_quality2(block_path, dense_gt_path, minMemb, minSeg, sigMin, sigWeights, sigSmooth, edgeLengths=None,
                      nodeFeatures=None, nodeSizes=None, nodeLabels=None, nodeNumStop=None, beta=0, metric='l1',
                      wardness=0.2, out=None):
    folder_list = [f for f in os.listdir(block_path) if not os.path.isfile(os.path.join(block_path,f))
                   and ("figure" not in f) and "redone" not in f]
    print "folder_list", folder_list
    outpath = block_path + "/redone_quality"
    if not os.path.exists(outpath):
        os.mkdir(outpath)

    dense_gt_data = read_h5(dense_gt_path)
    nodes_in_dgt = len(np.unique(dense_gt_data))
    for f in folder_list:
        folder_path = os.path.join(block_path, f)
        prob_file = [h for h in os.listdir(folder_path) if "probs" in h]
        prob_file_path = os.path.join(folder_path,prob_file[0])
        print
        print
        print prob_file_path
        predict_data = read_h5(prob_file_path)
        adjusted_predict_data = adjust_predict(predict_data)
        print "#nodes in dense gt", nodes_in_dgt
        pmin = 0.5

        seg, sup, wsDt_data, agglCl_data = get_segmentation(adjusted_predict_data, pmin, minMemb, minSeg, sigMin, sigWeights,
                                                            sigSmooth,True,False, edgeLengths,nodeFeatures, nodeSizes,
                                                            nodeLabels, nodeNumStop,beta, metric, wardness, out)
        nodes_in_seg = len(np.unique(seg))
        nodes_in_sup = len(np.unique(sup))

        ri, voi = rand_index_variation_of_information(seg, dense_gt_data)

        new_folder_path = outpath + "/" + f
        if not os.path.exists(new_folder_path):
            os.mkdir(new_folder_path)

        key = "pmin_"+ str(pmin) + "_minMemb_" + str(minMemb)+ "_minSeg_"+ str(minSeg) +"_sigMin_" + str(sigMin) + \
              "_sigWeights_" + str(sigWeights) + "_sigSmooth_" + str(sigSmooth) + "_nodeNumStop_" + str(nodeNumStop)
        save_h5(seg, new_folder_path + "/segmentation.h5", key)
        save_h5(sup, new_folder_path + "/super_pixels.h5", key)
        seg_data = np.zeros((2,3))
        seg_data[0,0] = ri
        seg_data[0,1] = voi
        seg_data[1,0] = nodes_in_dgt
        seg_data[1,1] = nodes_in_sup
        seg_data[1,2] = nodes_in_seg
        save_h5(seg_data, new_folder_path + "/seg_data", key, None)