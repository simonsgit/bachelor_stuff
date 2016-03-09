__author__ = 'stamylew'

import vigra
from volumina.api import Viewer
import sys
from PyQt4.QtGui import QApplication
from python_functions.handle_h5.handle_h5 import read_h5

def view_HDF5(inpaths):

    app = QApplication(sys.argv)
    v = Viewer()

    for inpath in inpaths:
        #data = vigra.readHDF5(inpath, "data")
        data = read_h5(inpath)
        file = inpath.split("/")[-1]
        name = file.split(".")[0]
        v.addGrayscaleLayer(data, name=name)
        v.addRandomColorsLayer(255*data, name=name+"color")

    v.showMaximized()
    app.exec_()

if __name__ == '__main__':
    data0 = "/home/stamylew/delme/prob.h5"
    data1 = "/home/stamylew/delme/super_pixels.h5"
    data2 = "/home/stamylew/delme/segmap.h5"
    data3 = "/home/stamylew/volumes/groundtruth/dense_groundtruth/200p_cube3_dense_gt.h5"
    data4 = "/home/stamylew/delme/seeds.h5"

    data5 = "/home/stamylew/volumes/groundtruth/trimaps/200p_cube1_trimap_t_05.h5"
    data6 = "/home/stamylew/volumes/groundtruth/trimaps/200p_cube1_trimap_t_10.h5"
    data7 = "/home/stamylew/volumes/groundtruth/trimaps/200p_cube1_trimap_t_15.h5"
    data8 = "/home/stamylew/volumes/test_data/200p_cube1.h5"
    data9 = "/home/stamylew/volumes/groundtruth/dense_groundtruth/200p_cube1_dense_gt.h5"
    dense_gt = "/mnt/CLAWS1/stamilev/data/ids_i_c_manualbigignore.h5"
    raw = "/mnt/CLAWS1/stamilev/data/d.h5"
    entire_data = (raw, dense_gt)
    inpaths1 = (data0, data1, data2, data3, data4)
    inpaths2 = (data5, data6, data7, data8, data9)
    view_HDF5(inpaths2)