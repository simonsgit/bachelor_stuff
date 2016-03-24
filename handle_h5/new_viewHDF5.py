__author__ = 'stamylew'

import vigra
import numpy as np
from volumina.api import Viewer
import sys
from PyQt4.QtGui import QApplication
from python_functions.handle_h5.handle_h5 import read_h5
from python_functions.quality.quality import adjust_predict, binarize_predict

def view_HDF5(inpaths):

    app = QApplication(sys.argv)
    v = Viewer()

    for inpath in inpaths:
        if "n_1_" in inpath:
            prefix = "n_1_"
        elif "n_2_" in inpath:
            prefix = "n_2_"
        else:
            prefix = ""
        if "h5" in inpath:
            #data = vigra.readHDF5(inpath, "data")
            print
            print "inpath", inpath
            data = read_h5(inpath)
            file = inpath.split("/")[-1]
            name = prefix + file.split(".")[0]
            if "prob_files" in inpath or "seeds" in inpath or "trimap" in inpath:
                data = binarize_predict(data)
                file = inpath.split("/")[-2] + "_" + inpath.split("/")[-1]
                name = prefix + file.split(".")[0]
            print "type", type(data)
            if "test_data" in inpath or "prob_files" in inpath or "seeds" in inpath or "trimap" in inpath:
                v.addGrayscaleLayer(data, name=name)
            # if "trimaps" in inpath or "dense" in inpath or "sup_maps" in inpath or "seg_maps" in inpath:
            #     v.addRandomColorsLayer(255*data, name=name+"_color")
            else:
                v.addRandomColorsLayer(255*data, name=name+"_color")

        if "png" in inpath:
            img = vigra.impex.readImage(inpath)
            img = np.asarray(img)
            file = inpath.split("/")[-1]
            name = file.split(".")[0]
            print "type",type(img)
            v.addGrayscaleLayer(img, name=name)

            #v.addRandomColorsLayer(255*img, name=name+"color")
    v.showMaximized()
    app.exec_()

if __name__ == '__main__':
    #raw data
    raw_cube1 = "/mnt/CLAWS1/stamilev/volumes/test_data/100p_cube1.h5"
    raw_cube2 = "/mnt/CLAWS1/stamilev/volumes/test_data/100p_cube2.h5"

    #dense gt
    dgt_cube1 = "/mnt/CLAWS1/stamilev/volumes/groundtruth/dense_groundtruth/100p_cube1_dense_gt.h5"
    dgt_cube2 = "/mnt/CLAWS1/stamilev/volumes/groundtruth/dense_groundtruth/100p_cube2_dense_gt.h5"

    #trimaps
    tri_cube1 = "/mnt/CLAWS1/stamilev/volumes/groundtruth/trimaps/100p_cube1_trimap_t_10.h5"
    tri_cube2 = "/mnt/CLAWS1/stamilev/volumes/groundtruth/trimaps/100p_cube2_trimap_t_05.h5"

    #probability maps for loop comparison
    central_cube1_path = "/mnt/CLAWS1/stamilev/test_folder/q_data/100p_cube1/"
    central_cube2_path = "/mnt/CLAWS1/stamilev/test_folder/q_data/100p_cube2/"
    prob_n_1_cube1 = central_cube1_path + "n_2_l_10000_w_none/prob_files/prob_1.h5"
    prob_n_5_cube1 = central_cube1_path + "n_5_l_10000_w_none/prob_files/prob_4.h5"
    prob_n_9_cube1 = central_cube1_path + "n_9_l_10000_w_none/prob_files/prob_8.h5"
    prob_n_10_cube1 = central_cube1_path + "n_10_l_10000_w_none/prob_files/prob_9.h5"
    prob_n_1_cube2 = central_cube2_path + "n_1_l_10000_w_none/prob_files/prob_1.h5"
    prob_n_2_cube2 = central_cube2_path + "n_2_l_10000_w_none/prob_files/prob_2.h5"

    #seed maps
    # seeds_n_1_cube2 = central_cube2_path + "n_1_l_10000_w_none/seeds/prob_6.h5"
    # seeds_n_2_cube2 = central_cube2_path + "n_2_l_10000_w_none/seeds/prob_6.h5"

    #segmentations map
    seg_n_1_cube1 = central_cube1_path + "n_2_l_10000_w_none/seg_maps/prob_1.h5"
    seg_n_5_cube1 = central_cube1_path + "n_5_l_10000_w_none/seg_maps/prob_4.h5"
    seg_n_9_cube1 = central_cube1_path + "n_9_l_10000_w_none/seg_maps/prob_8.h5"
    seg_n_10_cube1 = central_cube1_path + "n_10_l_10000_w_none/seg_maps/prob_9.h5"

    seg_n_1_cube2 = central_cube2_path + "n_1_l_10000_w_none/seg_maps/prob_1.h5"
    seg_n_2_cube2 = central_cube2_path + "n_2_l_10000_w_none/seg_maps/prob_2.h5"

    #super pixels
    sup_n_1_cube1 = central_cube1_path + "n_2_l_10000_w_none/sup_maps/prob_1.h5"
    sup_n_2_cube1 = central_cube1_path + "n_2_l_10000_w_none/sup_maps/prob_2.h5"
    sup_n_1_cube2 = central_cube2_path + "n_1_l_10000_w_none/sup_maps/prob_1.h5"
    sup_n_2_cube2 = central_cube2_path + "n_2_l_10000_w_none/sup_maps/prob_2.h5"

    # raw_usable_data = "/home/stamylew/volumes/test_data/usable_data.h5"
    # dgt_usable_data = "/home/stamylew/volumes/groundtruth/dense_groundtruth/usable_data_dense_gt.h5"
    # big_cube2 = "/mnt/CLAWS1/stamilev/volumes/test_data/500p_cube2.h5"
    # big_dgt2  = "/mnt/CLAWS1/stamilev/volumes/groundtruth/dense_groundtruth/500p_cube2_dense_gt.h5"
    raw_cubes = (raw_cube1, raw_cube2)
    # dgt_cubes = (dgt_cube1, dgt_cube2)
    # tri_cubes = (tri_cube1, tri_cube2)

    cube1 = (dgt_cube1, seg_n_10_cube1, seg_n_9_cube1, seg_n_5_cube1, seg_n_1_cube1, prob_n_10_cube1, prob_n_9_cube1, prob_n_5_cube1,
             prob_n_1_cube1)
    cube2 = (raw_cube2, dgt_cube2, tri_cube2, seg_n_2_cube2, sup_n_2_cube2, prob_n_2_cube2, seg_n_1_cube2, sup_n_1_cube2,
             prob_n_1_cube2)

    view_HDF5(raw_cubes)
    # view_HDF5((raw_usable_data, dgt_usable_data))
    # view_HDF5((big_cube2, big_dgt2))

    # from sklearn.metrics import roc_auc_score, roc_curve, accuracy_score, precision_score, recall_score
    # import skneuro.learning._learning as skl
    # a= np.array([1,1,1,0,0,1,0,1,0,0], dtype=np.uint32)
    # b= np.array([1,1,1,0,0,1,0,0,1,0], dtype=np.uint32)
    # print precision_score(a,b), skl.variationOfInformation(a,b)