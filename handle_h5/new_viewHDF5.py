__author__ = 'stamylew'

import vigra
from volumina.api import Viewer
import sys
from PyQt4.QtGui import QApplication

def view_HDF5(inpaths):

    app = QApplication(sys.argv)
    v = Viewer()

    for inpath in inpaths:
        data = vigra.readHDF5(inpath, "data")
        file = inpath.split("/")[-1]
        name = file.split(".")[0]
        v.addGrayscaleLayer(data, name=name)
        v.addRandomColorsLayer(255*data, name=name+"color")

    v.showMaximized()
    app.exec_()

if __name__ == '__main__':
    data1 = "/home/stamylew/delme/super_pixels.h5"
    data2 = "/home/stamylew/delme/segmap.h5"
    data3 = "/home/stamylew/volumes/groundtruth/dense_groundtruth/100p_cube2_dense_gt.h5"
    data4 = "/home/stamylew/delme/05bin_gt_map.h5"
    data5 = "/home/stamylew/volumes/groundtruth/memb/100p_cube2_memb.h5"
    data6 = "/home/stamylew/delme/segmentation_gt.h5"
    data7 = "/home/stamylew/delme/gt_seg_map.h5"
    data8 = "/home/stamylew/delme/gt_seg_seeds.h5"
    inpaths = (data1, data2, data3)
    view_HDF5(inpaths)