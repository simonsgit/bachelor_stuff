__author__ = 'stamylew'

import socket
from python_functions.other.single_test import test
from python_functions.other.host_config import assign_path

def multi_loops(nol, ilp, files, gt, labels="", weights="", repeats=1, outpath= "",
         t_cache = "", p_cache = ""):
    hostname = socket.gethostname()
    test_folder_path = assign_path(hostname)[4]
    if t_cache == "":
        t_cache = test_folder_path + "/t_cache"

    if p_cache == "":
        p_cache = test_folder_path + "/p_cache"

    if outpath == "":
        output = test_folder_path + "/q_data"

    for n in range(1,nol+1):
        test(ilp, files, gt, labels, n, weights, repeats, output, t_cache, p_cache)



def multi_labels(label_values,ilp, files, gt, loops=3, weights="", repeats=1, outpath= "",
         t_cache = "", p_cache = ""):
    hostname = socket.gethostname()
    test_folder_path = assign_path(hostname)[4]
    if t_cache == "":
        t_cache = test_folder_path + "/t_cache"

    if p_cache == "":
        p_cache = test_folder_path + "/p_cache"

    if outpath == "":
        output = test_folder_path + "/q_data"

    for n in label_values:
        test(ilp, files, gt, n, loops, weights, repeats, output, t_cache, p_cache)

if __name__ == '__main__':
    hostname = socket.gethostname()
    print
    print "hostname:", hostname

    ilp_folder = assign_path(hostname)[0]
    volumes_folder = assign_path(hostname)[1]
    ilp_file = ilp_folder + "500p_cube1.ilp"
    files = volumes_folder + "test_data/500p_cube2.h5/data"
    gt = volumes_folder + "groundtruth/trimaps/500p_cube2_trimap_t_05.h5"
    multi_loops(1, ilp_file, files, gt, 2000, "", 4)
    #multi_labels([100, 500, 1000, 5000, 10000, 20000],ilp_file, files, gt, 3, "", 10)