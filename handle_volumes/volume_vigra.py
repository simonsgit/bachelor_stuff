# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 15:27:41 2015

@author: stamylew
"""

import vigra as vg
from python_functions.handle_h5.handle_h5 import read_h5
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def make_slice_image(data, slice=0, outpath = "/home/stamylew/delme/delme.jpg"):
    image = data[:,:,slice]
    plt.imsave(outpath, image,  cmap = cm.Greys_r)

if __name__ == '__main__':
    data = read_h5("/home/stamylew/volumes/training_data/100p_cube1.h5")
    make_slice_image(data, 75, "/home/stamylew/Documents/Projektpraktikum/comparison_raw.png")
    print "done"