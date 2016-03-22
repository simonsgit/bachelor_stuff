__author__ = 'stamylew'

import os
import socket
from python_functions.other.single_test import test
from python_functions.other.host_config import assign_path
from python_functions.handle_data.new_modify_labels import reduce_labels_in_ilp

def multi_loops(nol, ilp, files, gt, dense_gt, labels="", weights="", repeats=1, outpath= "",
         t_cache = "", p_cache = ""):
    hostname = socket.gethostname()
    if labels != "":
        print
        print "reducing labels to " + str(labels)
        ilp = reduce_labels_in_ilp(ilp, labels)
    test_folder_path = assign_path(hostname)[5]
    if t_cache == "":
        t_cache = test_folder_path + "/t_cache"

    if p_cache == "":
        filesplit = files.split(".")[-2]
        filename = filesplit.split("/")[-1]
        p_cache = test_folder_path + "/p_cache/" + filename
        if not os.path.exists(p_cache):
            os.mkdir(p_cache)

    if outpath == "":
        outpath = test_folder_path + "/q_data"

    for n in range(1,nol+1):
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
        p_cache = test_folder_path + "/p_cache/" + filename
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
        p_cache = test_folder_path + "/p_cache/" + filename
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
    ilp_file1 = ilp_folder + "100p_cube1_t_05.ilp"
    ilp_file2 = ilp_folder + "100p_cube1_manual_less_feat.ilp"
    ilp_file3 = ilp_folder + "100p_cube2_t_05.ilp"
    ilp_file4 = ilp_folder + "100p_cube2_manual_less_feat.ilp"
    files1 = volumes_folder + "test_data/100p_cube2.h5/data"
    gt1 = volumes_folder + "groundtruth/trimaps/100p_cube2_trimap_t_05.h5"
    dense_gt1 = volumes_folder + "groundtruth/dense_groundtruth/100p_cube2_dense_gt.h5"
    files2 = volumes_folder + "test_data/100p_cube1.h5/data"
    gt2 = volumes_folder + "groundtruth/trimaps/100p_cube1_trimap_t_05.h5"
    dense_gt2 = volumes_folder + "groundtruth/dense_groundtruth/100p_cube1_dense_gt.h5"
    # multi_labels([60000, 70000],ilp_file2, files, gt, dense_gt, 3, "", 10)

    multi_loops(10, ilp_file1, files1, gt1, dense_gt1, 10000, "", 1)
    # multi_loops(10, ilp_file2, files1, gt1, dense_gt1, "", "", 10)
    # multi_loops(10, ilp_file3, files2, gt2, dense_gt2, 10000, "", 10)
    # multi_loops(10, ilp_file4, files2, gt2, dense_gt2, "", "", 10)
    # multi_loops(10, ilp_file1, files, gt, dense_gt, 20000, "", 10)
    # multi_loops(10, ilp_file2, files, gt, dense_gt, 10000, "", 10)
    # multi_labels([100, 500, 1000, 5000, 20000, 30000, 40000, 50000, 60000, 70000],ilp_file1, files, gt, dense_gt, 3, "", 10)
    # multi_weights(([1,1,1,1],[2,1,1,1], [3,2,1,1], [4,3,2,1],[1,1,1,2],[1,1,2,3],[1,2,3,4],[1,2,2,1],[1,2,3,1],[1,3,2,1]),
    #               ilp_file1, files1, gt1, dense_gt1, 4, "", 10)
    # multi_weights(([1,1,1,1],[2,1,1,1], [3,2,1,1], [4,3,2,1],[1,1,1,2],[1,1,2,3],[1,2,3,4],[1,2,2,1],[1,2,3,1],[1,3,2,1]),
    #               ilp_file2, files1, gt1, dense_gt1, 4, "", 10)
    # multi_weights(([1,1,1,1],[2,1,1,1], [3,2,1,1], [4,3,2,1],[1,1,1,2],[1,1,2,3],[1,2,3,4],[1,2,2,1],[1,2,3,1],[1,3,2,1]),
    #               ilp_file3, files2, gt2, dense_gt2, 4, "", 10)
    # multi_weights(([1,1,1,1],[2,1,1,1], [3,2,1,1], [4,3,2,1],[1,1,1,2],[1,1,2,3],[1,2,3,4],[1,2,2,1],[1,2,3,1],[1,3,2,1]),
    #               ilp_file4, files2, gt2, dense_gt2, 4, "", 10)