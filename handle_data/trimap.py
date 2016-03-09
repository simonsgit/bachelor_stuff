# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 18:42:39 2015

@author: stamylew
"""
from python_functions.handle_h5.handle_h5 import read_h5, save_h5
import numpy as np
import vigra
import matplotlib.pyplot as plt

#TODO: "create ignore through distant transformation"

def prepare_data(data):

    if 1 in np.unique(data):
        print
        print "label 1 is in data"
        labeled_one = data == 1
        modified = labeled_one * 1111 + data
        assert 1112 not in np.unique((data))
        return modified
    else:
        return data


def create_membrane(data):
    for i in range(data.shape[0]-1):
        print "x layer %d out of %d" % (i+1, data.shape[0]-1)
        for j in range(data.shape[1]-1):
            for k in range(data.shape[2]-1):
                #x direction
                if data[i,j,k] != data[i+1,j,k] and data[i,j,k] != 1:
                    data[i,j,k] = data[i+1,j,k] = 1
                if data[i,data.shape[1]-1,k] != data[i,data.shape[1]-2,k] and data[i, data.shape[1]-1,k] !=1:
                    data[i,data.shape[1]-1,k] = 1
                if data[i,j,data.shape[1]-1] != data[i,j,data.shape[1]-2] and data[i,j,data.shape[1]-1] !=1:
                    data[i,j,data.shape[1]-1] = 1
                #y direction
                if data[i,j,k] != data[i,j+1,k] and data[i,j,k] != 1:
                    data[i,j,k] = data[i,j+1,k] = 1
                if data[data.shape[1]-1,j,k] != data[data.shape[1]-2,j,k] and data[data.shape[1]-1,j,k] !=1:
                    data[i,data.shape[1]-1,k] = 1
                if data[i,j,data.shape[1]-1] != data[i,j,data.shape[1]-2] and data[i,j,data.shape[1]-1] !=1:
                    data[i,j,data.shape[1]-1] = 1
                #z direction
                if data[i,j,k] != data[i,j,k+1] and data[i,j,k] != 1:
                    data[i,j,k] = data[i,j,k+1] = 1
                if data[i,data.shape[1]-1,k] != data[i,data.shape[1]-2,k] and data[i, data.shape[1]-1,k] !=1:
                    data[i,data.shape[1]-1,k] = 1
                if data[data.shape[1]-1,j,k] != data[data.shape[1]-2,j,k] and data[data.shape[1]-1,j,k] !=1:
                    data[data.shape[1]-1,j,k] = 1
    return data


def label_neurons(data, neuron_label):
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            for k in range(data.shape[2]):
                if data[i,j,k] != 1 and data[i,j,k] != 0:
                    data[i,j,k] = neuron_label
    return data


def filter_membrane(dense_gt_data):
    prepared_data = prepare_data(dense_gt_data)
    memb = create_membrane(prepared_data)
    memb_data = label_neurons(memb, 0)
    return memb_data, dense_gt_data


def create_trimap(dense_gt_path, thickness):
    """
    :param: raw_data_path   : path to raw data
    :param: dense_gt_path   : path to dense groundtruth
    :param: thickness       : sigma of the gaussian smoothing
    :return trimap
    """

    # Read input data
    gt_data = read_h5(dense_gt_path)
    memb_data, gt_data = filter_membrane(gt_data)
    gt_data = read_h5(dense_gt_path)
    #print "memb_data", memb_data[0:5]

    #create ignore layer by gaussian smoothing
    gs = vigra.gaussianSmoothing(memb_data.astype(np.float32), thickness)
    mask = gs > 0
    #plt.show(mask[0,:,:])
    ignore_and_membrane_layer = mask + memb_data
    ignore_and_membrane_mask = ignore_and_membrane_layer < 1
    neuron_layer = np.multiply(gt_data, ignore_and_membrane_mask)
    #print "neurons", neuron_layer[0:5]
    neuron_mask = neuron_layer > 0
    normed_neurons = neuron_mask * 2
    trimap = memb_data + normed_neurons

    # Create outpath and save membrane and trimap
    filename_with_ending = dense_gt_path.split("/")[-1]
    filename = filename_with_ending.split("_")[0] + "_" + filename_with_ending.split("_")[1]
    thickness_string = str(thickness)
    memb_outpath = "/home/stamylew/volumes/groundtruth/memb/" + filename + "_memb.h5"
    save_h5(memb_data, memb_outpath, "data")
    thickness_tag = thickness_string.split(".")[0] + thickness_string.split(".")[1]
    trimap_outpath = "/home/stamylew/volumes/groundtruth/trimaps/" + filename + "_trimap_t_" + thickness_tag +".h5"
    save_h5(trimap, trimap_outpath, "data")

    return trimap


#def dilation(data, thickness):
#    output = vigra.filters.discDilation(data.astype(np.uint8), thickness)
#    return output
    
if __name__ == '__main__':
    
    raw_data_path = "/home/stamylew/volumes/test_data/200p_cube4.h5"
    dense_gt_path = "/home/stamylew/volumes/groundtruth/dense_groundtruth/200p_cube3_dense_gt.h5"
    dgt = read_h5(dense_gt_path)
    print "dgt", np.unique(dgt)
    trimap = create_trimap(dense_gt_path, 1.0)
    #print "trimap", trimap[0:5]

    print "done"