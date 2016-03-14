__author__ = 'stamylew'

import os
import socket
from python_functions.other.single_test import test
from python_functions.other.host_config import assign_path

def multi_loops(nol, ilp, files, gt, dense_gt, labels="", weights="", repeats=1, outpath= "",
         t_cache = "", p_cache = ""):
    hostname = socket.gethostname()
    test_folder_path = assign_path(hostname)[5]
    if t_cache == "":
        t_cache = test_folder_path + "/t_cache"

    if p_cache == "":
        filesplit = files.split(".")[-2]
        filename = filesplit.split("/")[-1]
        p_cache = test_folder_path + "/p_cache" + filename
        if not os.path.exists(p_cache):
            os.mkdir(p_cache)

    if outpath == "":
        outpath = test_folder_path + "/q_data"

    for n in range(11,nol+1):
        test(ilp, files, gt, dense_gt, labels, n, weights, repeats, outpath, t_cache, p_cache)


def multi_labels(label_values,ilp, files, gt, dense_gt, loops=3, weights="", repeats=1, outpath= "",
         t_cache = "", p_cache = ""):
    hostname = socket.gethostname()
    test_folder_path = assign_path(hostname)[5]
    if t_cache == "":
        t_cache = test_folder_path + "/t_cache"

    if p_cache == "":
        filesplit = files.split(".")[-2]
        filename = filesplit.split("/")[-1]
        p_cache = test_folder_path + "/p_cache" + filename
        if not os.path.exists(p_cache):
            os.mkdir(p_cache)

    if outpath == "":
        outpath = test_folder_path + "/q_data"

    for n in label_values:
        test(ilp, files, gt, dense_gt, n, loops, weights, repeats, outpath, t_cache, p_cache)


def multi_weights(weightings, ilp, files, gt, dense_gt, loops, labels, repeats=1, outpath ="",
                  t_cache= "", p_cache= ""):
    hostname = socket.gethostname()
    test_folder_path = assign_path(hostname)[5]
    if t_cache == "":
        t_cache = test_folder_path + "/t_cache"

    if p_cache == "":
        filesplit = files.split(".")[-2]
        filename = filesplit.split("/")[-1]
        p_cache = test_folder_path + "/p_cache" + filename
        if not os.path.exists(p_cache):
            os.mkdir(p_cache)

    if outpath == "":
        outpath = test_folder_path + "/q_data"

    for weights in weightings:
        test(ilp, files, gt, dense_gt, labels, loops, weights, repeats, outpath, t_cache, p_cache)


if __name__ == '__main__':
    hostname = socket.gethostname()
    print
    print "hostname:", hostname

    ilp_folder = assign_path(hostname)[1]
    volumes_folder = assign_path(hostname)[2]
    ilp_file = ilp_folder + "100p_cube1.ilp"
    files = volumes_folder + "test_data/100p_cube3.h5/data"
    gt = volumes_folder + "groundtruth/trimaps/100p_cube3_trimap_t_10.h5"
    dense_gt = volumes_folder + "groundtruth/dense_groundtruth/100p_cube3_dense_gt.h5"
    multi_loops(12, ilp_file, files, gt, dense_gt, 20000, "", 10)
    #multi_labels([100, 500, 1000, 5000, 20000, 30000, 40000, 50000, 600000],ilp_file, files, gt, dense_gt, 3, "", 10)
    # multi_weights(([1,1,1,1],[2,1,1,1], [3,2,1,1], [4,3,2,1]), ilp_file, files, gt, dense_gt, 4, 10000, 10)