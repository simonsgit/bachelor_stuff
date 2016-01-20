__author__ = 'stamylew'
from python_functions.handle_h5.handle_h5 import read_h5, save_h5
import numpy as np

def delete_row(data_path, row_number):
    data = read_h5(data_path)
    print "data: ", data
    new_data = np.delete(data, row_number, axis=0)
    print "new data: ", new_data
    #save_h5(new_data, data_path)


if __name__ == '__main__':
    data_path = "/home/stamylew/test_folder/q_data/500p_cube2/n_1_l_1000_w_none/n_1_l_1000_w_none.h5"
    delete_row(data_path, (3))