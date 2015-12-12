# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 11:21:48 2015

@author: stamylew
"""

import vigra as vg
import h5py as h

def read_h5(path, key=""):
    inpath_isstring = isinstance(path, basestring)
    assert inpath_isstring, "inpath should be string"
    f = h.File(path)
    
    if key=="":
        key = f.keys()[0]
    else:
	assert key in f.keys(), "the given key "+key+" is not in the file "+ path
    data = f[key][...]
    f.close()
    return data
    
    
def save_h5(data, outpath, key="", comp=""):
    if key =="":
        key = "data"
    if comp=="":
        comp = "lzf"
    vg.impex.writeHDF5(data, outpath, key, compression = comp)

if __name__ == '__main__':
    print "start"
    print "done"
