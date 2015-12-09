# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 17:06:00 2015

@author: stamylew
"""

def get_filename_from_abs_path(abs_path):
    filename = abs_path.split(".")[-2]
    filename = filename.split("/")[-1]
    return filename
