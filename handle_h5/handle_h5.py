# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 11:21:48 2015

@author: stamylew
"""


import h5py as h
import numpy as np
from h5py import Group
import vigra as vg

def read_h5(path, key=""):
    inpath_isstring = isinstance(path, basestring)
    assert inpath_isstring, "inpath should be string"
    f = h.File(path, "r")

    if key=="":
        key = f.keys()[0]
    else:
        assert key in f.keys(), "the given key "+ key +" is not in the file "+ path
    data = f[key][...]
    f.close()
    return data
    
    
def save_h5(data, outpath, key="", comp=""):
    if key =="":
        key = "data"
    if comp=="":
        comp = "lzf"
    vg.impex.writeHDF5(data, outpath, key, compression = comp)

def save_h5_wo_vigra(data, outpath, key="", comp=""):
    #TODO: doesn't work IOError Unable to create file (Unable to truncate a file which is already open)
    if key =="":
        key = "data"
    if comp=="":
        comp = "lzf"
    g = h.File(outpath, "w")
    g.create_dataset(key, data= data, compression= comp)

if __name__ == '__main__':

    #vg.impex.readHDF5("file:///mnt/data/simon/volumes/groundtruth/dense_groundtruth/50cube1_dense_gt.h5")
    dset = read_h5("/home/stamylew/volumes/test_data/500p_cube2.h5")
    save_h5(dset, "/home/stamylew/delme/test.h5")
    print "done"
