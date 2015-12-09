# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 11:53:51 2015

@author: stamylew
"""
import numpy as np
import vigra as vg
from handle_h5 import save_h5
from handle_h5 import read_h5
from cut_block.py import cut_block
#number = re.findall('\d+[,.]\d+|\d+', x)
#y = number[-1]
#print int(y)


def make_volume(x):
    #read first image
    sample = vg.impex.readImage(x)
    #create volume in cubic shape based on first image
    vol = np.zeros((sample.shape[0], sample.shape[1], sample.shape[0]), dtype= np.uint8)
    #get common name of image files
    common_name = x.split(".")[0]
    #find offset of image number
    offset = x.split(".")[-2]
    #find length of image file number
    str_length = len(offset)
    #get filetype of image files
    filetype = x.split(".")[-1]
    #insert images in volume
    for i in range(sample.shape[0]):
        number = int(offset) + i
        sample = common_name + "." + str(number).zfill(str_length) + "." + str(filetype)
        vol[:, :, i] = np.squeeze(vg.impex.readImage(sample))
    return vol

    
if __name__ == '__main__':
#    x = "iso.03490.png"
#    vol = make_volume(x)
#    save_h5(vol, "volumes/volume.hdf5")
    
    f = "/mnt/CLAWS1/stamilev/data/ids_i_c_manualbigignore.h5"
    g = read_h5(f, "data")
    save_h5(g, "/home/stamylew/volumes/ids_i_c_manualbigignore.h5", "raw", None)
    #j = cut_block(g, 316, 492, 464, 640, 1, 177)
    m = cut_block(g, 25, 725, 0, 700, 0, 700)
    save_h5(m, "/home/stamylew/volumes/ids_i_c_manualbigignore.h5", "useful", None)
    print "done"