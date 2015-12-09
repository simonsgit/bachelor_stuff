# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 14:45:41 2015

@author: stamylew
"""

from handle_h5 import read_h5
from handle_h5 import save_h5
from quality import precision

def compare(data1, data2):
    comparison = data1 == data2
    return comparison

if __name__ == '__main__':
    f = read_h5("/home/stamylew/volumes/test_cube1.h5", "75cube_memb")
    g = read_h5("/home/stamylew/volumes/test_cube1.h5", "bin_n5")
    print precision(f, g)