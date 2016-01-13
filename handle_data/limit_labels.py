__author__ = 'stamylew'

import numpy as np
from python_functions.handle_h5.handle_h5 import read_h5, save_h5


data = read_h5("/home/stamylew/volumes/groundtruth/trimaps/500p_cube1_trimap_t_05.h5")
perm = np.random.permutation(data)
survivors = perm [:3]
#save_h5(perm, "/home/stamylew/volumes/groundtruth/trimaps/test.h5")
print data
print "survivors"
print survivors