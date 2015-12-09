# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 16:12:22 2015

@author: stamylew
"""
import vigra as vg
import h5py as h



def cut_block(inpath, outpath, x1=225, x2=725, y1=200, y2=700, z1=200, z2=700):
    inpath_isstring = isinstance(inpath, basestring)
    assert inpath_isstring, "inpath should be string"
    n = inpath
    k = h.File(str(n), "r").keys()
    data = h.File(str(n), "r")[k[0]][...]
    h.File(str(n), "r").close()
    block = data[x1:x2, y1:y2, z1:z2]
    print block
    print n.split("/")[-1]
    adress = "volumes/block_of_" + n.split("/")[-1]

    nickname = "data"
    print adress
    print nickname
    vg.impex.writeHDF5(block, outpath, nickname, compression = "lzf")
    
    

    
if __name__ == '__main__':
    inpath = "/mnt/CLAWS1/stamilev/data/ids_i_c_manualbigignore.h5"
    outpath = "/home/stamylew/volumes/groundtruth/dense_groundtruth/100p_cube1_dense_gt.h5"
    print outpath
    cut_block(inpath, outpath, 25, 125, 0, 100, 0, 100)
    print "done"