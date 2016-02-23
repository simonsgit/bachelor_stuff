# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 18:42:39 2015

@author: stamylew
"""
from python_functions.handle_h5.handle_h5 import read_h5, save_h5
from python_functions.handle_data.create_membrane import filter_membrane
import numpy as np
import vigra
import matplotlib.pyplot as plt

#TODO: "create ignore through distant transformation"

def create_trimap(raw_data_path, dense_gt_path, thickness):
    """
    :param: raw_data_path   : path to raw data
    :param: gt_path         : path to dense groundtruth
    :param: thickness       : sigma of the gaussian smoothing
    :return trimap
    """

    # Read input data
    gt_data = read_h5(dense_gt_path)
    print "gt unique", np.unique(gt_data)
    memb_data, gt_data = filter_membrane(gt_data)
    print "gt", np.unique(gt_data)
    #print "memb_data", memb_data[0:5]

    #create ignore layer by gaussian smoothing
    gs = vigra.gaussianSmoothing(memb_data.astype(np.float32), thickness)
    mask = gs > 0
    ignore_and_membrane_layer = mask + memb_data
    ignore_and_membrane_mask = ignore_and_membrane_layer < 1
    neuron_layer = np.multiply(gt_data, ignore_and_membrane_mask)
    #print "neurons", neuron_layer[0:5]
    neuron_mask = neuron_layer > 0
    normed_neurons = neuron_mask * 2
    trimap = memb_data + normed_neurons

    # Create outpath and save trimap
    filename_with_ending = raw_data_path.split("/")[-1]
    filename = filename_with_ending.split(".")[0]
    thickness_string = str(thickness)
    thickness_tag = thickness_string.split(".")[0] + thickness_string.split(".")[1]
    outpath = "/home/stamylew/volumes/groundtruth/trimaps/" + filename + "_trimap_" + thickness_tag +".h5"
    save_h5(trimap, outpath, "data")

    return trimap


    
#def dilation(data, thickness):
#    di = vigra.filters.discDilation(data.astype(np.uint8), thickness)
#    output = di
#    return output
    
if __name__ == '__main__':
    
    raw_data_path = "/home/stamylew/volumes/test_data/100p_cube3.h5"
    dense_gt_path = "/home/stamylew/volumes/groundtruth/dense_groundtruth/100p_cube3_dense_gt.h5"
    dgt = read_h5(dense_gt_path)
    print "dgt", np.unique(dgt)
    trimap = create_trimap(raw_data_path, dense_gt_path, 0.9)
    #print "trimap", trimap[0:5]

    print "done"