# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 16:12:22 2015

@author: stamylew
"""
import numpy as np
import vigra as vg
import h5py as h


def create_random_block(source, outpath, x_size, y_size, z_size):
    """
    :param source:
    :param x_size:
    :param y_size:
    :param z_size:
    :return:
    """

    x_anchor = np.random.randint(0,x_size)
    y_anchor = np.random.randint(0,y_size)
    z_anchor = np.random.randint(0,z_size)

    cut_block(source, outpath, x_anchor, y_anchor, z_anchor)

def create_random_cube(source, outpath, length):
    x_size = length
    y_size = length
    z_size = length

    create_random_block(source, outpath, x_size, y_size, z_size)

def cut_block(inpath, outpath, x1=225, x2=725, y1=200, y2=700, z1=200, z2=700):
    """
    :param inpath
    :param outpath
    """

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

    return outpath
    
    

    
if __name__ == '__main__':
    #inpath = "/mnt/CLAWS1/stamilev/data/ids_i_c_manualbigignore.h5"
    inpath = "/mnt/CLAWS1/stamilev/data/d.h5"
    #outpath = "/home/stamylew/volumes/groundtruth/dense_groundtruth/100p_cube3_dense_gt.h5"
    outpath = "/home/stamylew/volumes/test_data/100p_cube3.h5"
    print outpath
    cut_block(inpath, outpath, 246, 346, 753, 853, 50, 150)
    print "done"