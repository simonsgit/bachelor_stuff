# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 15:09:56 2015

@author: stamylew
"""


from os import listdir
from os.path import isfile, join
import vigra as vg
import numpy as np


def make_vol(x):
    onlyfiles = [f for f in listdir(x) if (isfile(join(x,f))) and (".png" in f)] #holt die .png files aus dem Zielordner
    onlyfiles.sort() #sortiert die files
    f = x + onlyfiles[0] #wählt das erste Bild
    print f
    firstpic = vg.impex.readImage(f) #liest das erste Bild
    vol = np.zeros((firstpic.shape[0], firstpic.shape[1], len(onlyfiles)), dtype=np.uint8) #kreiert das Volumengerüst
    for i in range(len(onlyfiles)):                         #ordnet jeder z-Ebene ein Bild zu
        pic = x + onlyfiles[i]
        vol[:, :, i] = np.squeeze(vg.impex.readImage(pic))
        print i, "/", len(onlyfiles),
    adress = "volumes/" + x.split("/")[-3] +".hdf5"
    vg.impex.writeHDF5(vol, adress, "data", compression="lzf") #speichert das Volumen als HDF5 file
    print "done"
    
if __name__ == '__main__':
    n = "data/neuroproof_examples/validation_sample/grayscale_maps/"
    make_vol(n)
#    test = np.ones((10, 10, 10), dtype=np.uint8)
#    vg.impex.writeHDF5(test, "volumes/test.hdf5", "data", compression="lzf")