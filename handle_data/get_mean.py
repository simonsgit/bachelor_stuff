__author__ = 'stamylew'

from python_functions.handle_h5.handle_h5 import read_h5
import numpy as np

measurement1 = "rand index"
measurement2 = "variation of information"
measurement3 = "precision"
measurement4 = "recall"
measurement5 = "true positives"
measurement6 = "false positives"
measurement7 = "true negatives"
measurement8 = "false negatives"

path = "/mnt/CLAWS1/stamilev/test_folder/compare_labels/100p_cube1/100p_cube1_n_3_random/n_3_l_1000.0_w_none/n_3_l_1000.0_w_none.h5"
key = "quality/" + measurement2

data = read_h5(path, key)
print np.mean(data)