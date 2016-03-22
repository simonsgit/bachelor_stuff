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
    outpath = "/mnt/CLAWS1/stamilev/volumes/groundtruth/dense_gt_data/" + filename2 + ".h5"
    dgt = read_h5(dense_gt_path)
    #dgt= dgt[25:725, 0:700, 0:700]
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
    nodes_data = np.zeros((l,2), dtype=np.uint)
    for n in range(l):
        nodes_data[n,0] = unique_tuples[n][0]
        nodes_data[n,1] = unique_tuples[n][1]
    #outpath = "/home/stamylew/volumes/groundtruth/dense_gt_data/entire_usable_data.h5"
    save_h5(nodes_data, outpath, "nodes and occurrence", None)

def get_trimap_data(trimap_path):
    filename1 = trimap_path.split("/")[-1]
    filename2 = filename1.split("_")[0] + "_" + filename1.split("_")[1]
    outpath = "/mnt/CLAWS1/stamilev/volumes/groundtruth/dense_gt_data/" + filename2 + ".h5"
    print outpath
    trimap = read_h5(trimap_path)
    #dgt= dgt[25:725, 0:700, 0:700]
    unique = np.unique(trimap)
    unique_elements = []
    unique_tuples = []
    print "no of unique elements", len(unique)

    for i in unique:
        mask = trimap == i
        noe = np.sum(mask)
        print i, noe
        unique_elements.append(noe)
        unique_tuples.append((i, noe))

    assert len(unique)==len(unique_elements)
    l = len(unique_elements)
    nodes_data = np.zeros((l,2), dtype=np.uint)
    for n in range(l):
        nodes_data[n,0] = unique_tuples[n][0]
        nodes_data[n,1] = unique_tuples[n][1]
    #outpath = "/home/stamylew/volumes/groundtruth/dense_gt_data/entire_usable_data.h5"
    save_h5(nodes_data, outpath, "labels and occurrence", None)

if __name__ == '__main__':
    # dgt_path = "/mnt/CLAWS1/stamilev/data/ids_i_c_manualbigignore.h5"
    dgt_path = "/home/stamylew/volumes/groundtruth/dense_groundtruth/100p_cube2_dense_gt.h5"
    trimap_path = "/mnt/CLAWS1/stamilev/volumes/groundtruth/trimaps/100p_cube2_trimap_t_10.h5"
    get_nodes_data(dgt_path)
    get_trimap_data(trimap_path)