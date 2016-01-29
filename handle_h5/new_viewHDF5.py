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

    v.showMaximized()
    app.exec_()

if __name__ == '__main__':
    data1 = "/home/stamylew/volumes/groundtruth/trimaps/100p_cube2_trimap_t_05.h5"
    data2 = "/home/stamylew/volumes/groundtruth/trimaps/100p_cube2_trimap_t_09.h5"
    data3 = "/home/stamylew/volumes/groundtruth/trimaps/100p_cube2_trimap_t_15.h5"
    inpaths = (data1, data2, data3)
    view_HDF5(inpaths)