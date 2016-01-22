# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 18:42:39 2015

@author: stamylew
"""
from python_functions.handle_h5.handle_h5 import save_h5
import numpy as np
import vigra
import matplotlib.pyplot as plt

def create_trimap(memb_data, gt_data, thickness):

    #create ignore layer by gaussian smoothing
    gs = vigra.gaussianSmoothing(memb_data.astype(np.float32), thickness)

    #
    layer = gs > 0


    trimap = layer + memb_data
    trimap_filter = trimap < 1
    neurons = np.multiply(gt_data, trimap_filter)
    neuron_filter = neurons > 0
    normed_neurons = neuron_filter * 2
    labeled_data = memb_data + normed_neurons
    
    
    return labeled_data


    
#def dilation(data, thickness):
#    di = vigra.filters.discDilation(data.astype(np.uint8), thickness)
#    output = di
#    return output
    
if __name__ == '__main__':
    
    d = vigra.readHDF5("/home/stamylew/volumes/groundtruth/memb/100p_cube2_memb.h5", "data")
    gt = vigra.readHDF5("/home/stamylew/volumes/groundtruth/dense_groundtruth/100p_cube2_dense_gt.h5", "data")
    # plt.figure()
    # plt.imshow(d[0])
    #
    # plt.figure()
    # plt.imshow(gt[0])

    ld = create_trimap(d, gt, 0.9)
    save_h5(ld, "/home/stamylew/volumes/groundtruth/trimaps/100p_cube2_trimap_t_09.h5", "data", "lzf")
    #
    # plt.figure()
    # plt.imshow(d[10])
    # #plt.imsave("/home/stamylew/tests/a", d[0])
    #
    # plt.figure()
    # plt.imshow(ld[10])
    # #plt.savefig("/home/stamylew/tests/b")
    #
    #plt.show()
    print "done"