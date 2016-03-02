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
    data3 = "/home/stamylew/volumes/groundtruth/dense_groundtruth/100p_cube2_dense_gt.h5"
    data4 = "/home/stamylew/volumes/groundtruth/dense_groundtruth/100p_cube3_dense_gt.h5"
    data5 = "/home/stamylew/volumes/groundtruth/trimaps/100p_cube3_trimap_15.h5"
    data6 = "/home/stamylew/volumes/groundtruth/memb/100p_cube3_memb.h5"
    data7 = "/home/stamylew/delme/segmentation_gt.h5"
    data8 = "/home/stamylew/delme/gt_seg_seeds.h5"
    inpaths = (data0, data1, data2, data3, data5, data6)
    view_HDF5(inpaths)