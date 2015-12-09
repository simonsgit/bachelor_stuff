# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 16:50:07 2015

@author: stamylew
"""

def show():
    import numpy as np

    import sys , h5py ; from numpy import float32 , uint8
    from vigra.filters import hessianOfGaussianEigenvalues , gaussianSmoothing
    from vigra.analysis import watersheds
    from vigra.analysis import labelVolumeWithBackground, extendedLocalMinima3D
    from PyQt4.QtCore import QTimer ; from PyQt4 . QtGui import QApplication
    app = QApplication ( sys.argv )
    from volumina.api import Viewer
    v = Viewer ()
    v . title = " Volumina Demo "
    v . showMaximized ()
    print "blubb"

    print a

    data = np.random.random((50,50,50))

    v . addGrayscaleLayer ( data , name =" raw data ")

    t = QTimer ()
    t.setInterval (200)

    app.exec_ ()
    
    
