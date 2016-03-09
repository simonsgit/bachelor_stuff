__author__ = 'stamylew'
import matplotlib.pyplot as plt
import numpy as np
from python_functions.handle_h5.handle_h5 import read_h5, save_h5

# plt.plot([2,4,6,8], label='a')
# plt.plot([1,2,3,4], label='b')
# plt.legend()
# plt.show()

def get_nodes_data(dense_gt_path):

    filename1 = dense_gt_path.split("/")[-1]
    filename2 = filename1.split("_")[0] + "_" + filename1.split("_")[1]
    outpath = "/home/stamylew/volumes/groundtruth/dense_gt_data/"+ filename2 + ".h5"
    dgt = read_h5(dense_gt_path)
    dgt= dgt[25:725, 0:700, 0:700]
    unique = np.unique(dgt)
    unique_elements = []
    unique_tuples = []
    print "no of unique elements", len(unique)

    for i in unique:
        mask = dgt == i
        noe = np.sum(mask)
        print i, noe
        unique_elements.append(noe)
        unique_tuples.append((i, noe))

    assert len(unique)==len(unique_elements)
    l = len(unique_elements)
    data = np.zeros((l,2), dtype=np.uint)
    for n in range(l):
        data[n,0] = unique_tuples[n][0]
        data[n,1] = unique_tuples[n][1]
    outpath = "/home/stamylew/volumes/groundtruth/dense_gt_data/entire_usable_data.h5"
    save_h5(data,outpath,"data", None)

if __name__ == '__main__':
    dgt_path = "/mnt/CLAWS1/stamilev/data/ids_i_c_manualbigignore.h5"
    #dgt_path = "/home/stamylew/volumes/groundtruth/dense_groundtruth/200p_cube3_dense_gt.h5"
    get_nodes_data(dgt_path)