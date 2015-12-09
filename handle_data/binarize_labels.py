# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 14:31:38 2015

@author: stamylew
"""


import numpy as np
from python_functions.handle_h5.handle_h5 import read_h5, save_h5

def threshold(data, threshold_membrane, threshold_neurons):
    bin_data = np.zeros(data.shape)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            for k in range(data.shape[2]):
                if data[i,j,k] <= threshold_membrane:
                    bin_data[i,j,k] = 0
                if data[i,j,k] > threshold_membrane and data[i,j,k] <= threshold_neurons:
                    bin_data[i,j,k] = 0.5
                if data[i,j,k] > threshold_neurons:
                    bin_data[i,j,k] = 1
    return bin_data
  
  
if __name__ == '__main__':
    f = read_h5("/home/stamylew/volumes/100x100block_of_validation_sample_Probabilities.h5", "exported_data")
    data = threshold(f, 0.4, 0.6)
    save_h5(data, "/home/stamylew/volumes/100x100block_of_validation_sample_Probabilities.h5", "bin", None)

    print "done"