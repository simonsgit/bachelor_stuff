__author__ = 'stamylew'

import vigra
import numpy as np
from volumina.api import Viewer
import sys
from PyQt4.QtGui import QApplication
from python_functions.handle_h5.handle_h5 import read_h5
from python_functions.quality.quality import adjust_predict

def view_HDF5(inpaths):

    app = QApplication(sys.argv)
    v = Viewer()

    for inpath in inpaths:
        if "h5" in inpath:
            #data = vigra.readHDF5(inpath, "data")
            data = read_h5(inpath)
            file = inpath.split("/")[-1]
            name = file.split(".")[0]
            if "probs" in inpath:
                data = adjust_predict(data)
                file = inpath.split("/")[-2] + inpath.split("/")[-1]
                name = file.split(".")[0]
            print "type", type(data)
            v.addGrayscaleLayer(data, name=name)
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
    data0 = "/home/stamylew/test_folder/q_data/100p_cube3_random/n_1_l_20000_w_none_segmentation.h5"
    data1 = "/home/stamylew/test_folder/q_data/100p_cube3_random/n_1_l_20000_w_none_super_pixels.h5"
    data2 = "/home/stamylew/test_folder/q_data/100p_cube3_random/n_2_l_20000_w_none_segmentation.h5"
    data3 = "/home/stamylew/test_folder/q_data/100p_cube3_random/n_2_l_20000_w_none_super_pixels.h5"
    data4 = "/home/stamylew/volumes/groundtruth/dense_groundtruth/100p_cube3_dense_gt.h5"

    data5 = "/home/stamylew/volumes/groundtruth/trimaps/200p_cube1_trimap_t_05.h5"
    data6 = "/home/stamylew/volumes/groundtruth/trimaps/200p_cube1_trimap_t_10.h5"
    data7 = "/home/stamylew/volumes/groundtruth/trimaps/200p_cube1_trimap_t_15.h5"
    data8 = "/home/stamylew/volumes/test_data/200p_cube1.h5"
    data9 = "/home/stamylew/volumes/groundtruth/dense_groundtruth/200p_cube1_dense_gt.h5"

    data10 = "/home/stamylew/test_folder/q_data/100p_cube3_random/n_2_l_20000_w_none/100p_cube3_probs.h5"
    data11 = "/home/stamylew/test_folder/q_data/100p_cube3_random/n_4_l_20000_w_none/100p_cube3_probs.h5"
    data12 = "/home/stamylew/test_folder/q_data/100p_cube3_random/n_6_l_20000_w_none/100p_cube3_probs.h5"
    data13 = "/home/stamylew/volumes/groundtruth/dense_groundtruth/100p_cube3_dense_gt.h5"
    data14 = "/home/stamylew/volumes/groundtruth/trimaps/100p_cube3_trimap_t_10.h5"


    dense_gt = "/mnt/CLAWS1/stamilev/data/ids_i_c_manualbigignore.h5"
    raw = "/mnt/CLAWS1/stamilev/data/d.h5"
    entire_data = (raw, dense_gt)
    inpaths1 = (data0, data1, data2, data3, data4)
    inpaths2 = (data5, data6, data7, data8, data9)
    inpaths3 = (data14, data13, data10, data11, data12)
    view_HDF5(inpaths1)