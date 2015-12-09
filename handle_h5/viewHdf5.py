# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 14:21:27 2015

@author: stamylew
"""

import vigra
import h5py
import numpy as np
import matplotlib.pyplot as plt



def view_sampleimage_fromHDF5_withkey(path, key):
    d = vigra.impex.readHDF5(path, key)
    d = np.squeeze(d)
    assert np.size(np.shape(d)) in [3, 4]    
    
    c = 1
    
    if np.size(np.shape(d)) == 4:
        c = np.shape(d)[-1]
    else:
        d = d[:,:,:,np.newaxis]
        
    
    for i in range(c):
                
        plt.figure()
        plt.title(key + " - " + str(i))
        plt.gray()
        plt.imshow(d[:,:,0,i], interpolation="nearest")
    


def view_sampleimage_fromHDF5(path):
    f = h5py.File(path, "r")
    keys = f.keys()
    f.close()
    
    for k in keys:
        print k
        view_sampleimage_fromHDF5_withkey(path, k)
    

if __name__ == "__main__":
    #test_path = "/home/stamylew/src/autocontext/training/cache/0000_test_cube2_probs.h5"    
    #view_sampleimage_fromHDF5(test_path)
        
    
    #comparison = "/home/stamylew/volumes/trimaps/50cube2_tri.h5"
    #comparison = "/home/stamylew/volumes/training_data/smallcubes.h5"

    raw = vigra.readHDF5("/home/stamylew/volumes/test_data/500p_cube2_raw.h5", "data")

    predict = vigra.readHDF5("/home/stamylew/volumes/test_data/500p_cube2_memb.h5", "memb")
    print predict.shape

    tm = vigra.readHDF5("/home/stamylew/volumes/groundtruth/trimaps/500p_cube2_trimap_t_05.h5", "data")

    gt = vigra.readHDF5("/home/stamylew/volumes/groundtruth/dense_groundtruth/100p_cube1_dense_gt.h5", "data")

    from volumina.api import Viewer
    from volumina.pixelpipeline.datasources import LazyflowSource
    import sys
    from lazyflow.graph import Graph
    from lazyflow.operators.ioOperators.opStreamingHdf5Reader import OpStreamingHdf5Reader
    from lazyflow.operators import OpCompressedCache
    
    from PyQt4.QtGui import QApplication
    
    
    
    app = QApplication(sys.argv)
    v = Viewer()

    #raw layer
    v.addGrayscaleLayer(raw, name="raw")

    #predict layer
    #predict = np.array(predict[:,:,:,0,0]) * 255
    #v.addColorTableLayer(predict.astype(np.float32), name="prediction")
    v.addGrayscaleLayer(predict.astype(np.float32), name="prediction")

    #trimap layer
    tm = np.array(tm)*255
    print np.unique(tm)
    v.addColorTableLayer(tm.astype(np.float32), name="trimap")
    #v.addGrayscaleLayer(tm.astype(np.float32), name="tm")


    #gt layer
    v.addGrayscaleLayer(gt.astype(np.float32), name="groundtruth")

    v.showMaximized()
    app.exec_()    
    
    
#    plt.figure()
#    plt.gray()    
#    plt.imshow(raw[:,:,0], interpolation= "nearest")    
#    
#    plt.figure()
#    
#    masked = np.copy(raw)
#    
#    masked = masked[:,:,:,np.newaxis]
#    masked = np.tile(masked, (1, 1, 1, 3))
#    
#    masked[:,:,:,0][tm == 0] = 0
#    
#    
#    
#
#    
#    #masked[tm != 2] -= 100  
#    #np.clip(masked, 0, 255)
#    
#    plt.imshow(masked[:,:,0], interpolation= "nearest")
#    
#    plt.show()

    
    
    
        
    
    #view_sampleimage_fromHDF5(comparison)
    
    