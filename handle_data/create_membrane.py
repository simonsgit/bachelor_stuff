# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 15:00:45 2015

@author: stamylew
"""

from python_functions.handle_h5.handle_h5 import read_h5, save_h5
import numpy as np
import vigra

def prepare_data(data):
    if 1 in np.unique(data):
        print
        print "label 1 in data"
        labeled_one = data == 1
        modified = labeled_one * 11 + data
        assert 12 not in np.unique((data))
        return modified
    else:
        return data


def create_membrane(data):
    for i in range(data.shape[0]-1):
        print i
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

def create_membrane2(data, r):
    for i in range(data.shape[0]-r):
        for j in range(data.shape[1]-r):
            for k in range(data.shape[2]-r):
                #x direction
                if data[i,j,k] != data[i+r,j,k] and data[i,j,k] != 1:
                    data[i,j,k] = data[i+r,j,k] = 1
#                if data[i,data.shape[1]-1,k] != data[i,data.shape[1]-2,k] and data[i, data.shape[1]-1,k] !=1:
#                    data[i,data.shape[1]-1,k] = 1
#                if data[i,j,data.shape[1]-1] != data[i,j,data.shape[1]-2] and data[i,j,data.shape[1]-1] !=1:
#                    data[i,j,data.shape[1]-1] = 1
#                #y direction
                if data[i,j,k] != data[i,j+r,k] and data[i,j,k] != 1:
                    data[i,j,k] = data[i,j+r,k] = 1
#                if data[data.shape[1]-1,j,k] != data[data.shape[1]-2,j,k] and data[data.shape[1]-1,j,k] !=1:
#                    data[i,data.shape[1]-1,k] = 1
#                if data[i,j,data.shape[1]-1] != data[i,j,data.shape[1]-2] and data[i,j,data.shape[1]-1] !=1:
#                    data[i,j,data.shape[1]-1] = 1
#                #z direction
                if data[i,j,k] != data[i,j,k+r] and data[i,j,k] != 1:
                    data[i,j,k] = data[i,j,k+r] = 1
#                if data[i,data.shape[1]-1,k] != data[i,data.shape[1]-2,k] and data[i, data.shape[1]-1,k] !=1:
#                    data[i,data.shape[1]-1,k] = 1
#                if data[data.shape[1]-1,j,k] != data[data.shape[1]-2,j,k] and data[data.shape[1]-1,j,k] !=1:
#                    data[data.shape[1]-1,j,k] = 1
    return data

#def create_thicker_membrane(data, thickness):
#    t = thickness
#    for i in range(data.shape[0]-t):
#        for j in range(data.shape[1]-t):
#            for k in range(data.shape[2]-t):
#                if data[i,j,k] == 0 and data[i+t,j,k] == 1:
#                    for l in range(t-1):
#                        data[i+l,j,k] = 1
#                if data[i,j,k] == 1 and data[i+t,j,k] == 0:
#                    for l in range(t):
#                        data[i+l,j,k] = 1
#    return data

def label_neurons(data, neuron_label):
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            for k in range(data.shape[2]):
                if data[i,j,k] != 1 and data[i,j,k] != 0:
                    data[i,j,k] = neuron_label
    return data

def filter_membrane(data):
    prepared_data = prepare_data(data)
    memb = create_membrane(prepared_data)
    memb_data = label_neurons(memb, 0)
    return memb_data

if __name__ == '__main__':
    data = read_h5("/home/stamylew/volumes/groundtruth/dense_groundtruth/100p_cube1_dense_gt.h5", "data")

    memb = filter_membrane(data)
    save_h5(memb, "/home/stamylew/volumes/groundtruth/memb/100p_cube1_memb.h5", "data", "lzf")
    
    print "done"