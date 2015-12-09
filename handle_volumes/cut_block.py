# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 17:52:45 2015

@author: stamylew
"""

def cut_block(data, x1=0, x2=50, y1=0, y2=50, z1=0, z2=50):
    #create block
    block = data[x1:x2, y1:y2, z1:z2]
    return block
    