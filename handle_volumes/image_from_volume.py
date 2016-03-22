# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 15:27:41 2015

@author: stamylew
"""

import vigra as vg
import numpy as np
from python_functions.handle_h5.handle_h5 import read_h5
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as cl


def make_slice_image(data, slice=40, outpath = "/mnt/CLAWS1/stamilev/delme/delme.jpg", grey= True):
    image = data[:,:,slice]
    if grey:
        plt.imsave(outpath, image,  cmap = cm.Greys_r)
    else:
        plt.imsave(outpath, image,  cmap = cl.ListedColormap ( np.random.rand ( 256,3)))


if __name__ == '__main__':
    data = read_h5("/mnt/CLAWS1/stamilev/volumes/groundtruth/dense_groundtruth/100p_cube2_dense_gt.h5")
    make_slice_image(data, 40, "/mnt/CLAWS1/stamilev/delme/100p_cube2_merge_dgt.png", False)
    print "done"