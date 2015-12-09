# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 12:03:53 2015

@author: stamylew
"""

import vigra as vg
import numpy as np
import h5py as h
from make_smallvol import cut_block

n = "/home/stamylew/volumes/training_sample2.hdf5"
cut_block(n, 40, 140, 40, 140, 40, 140)