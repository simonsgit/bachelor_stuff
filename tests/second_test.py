# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 17:28:17 2015

@author: stamylew
"""

from python_functions.handle_volumes.cut_block import cut_block
from python_functions.handle_data.create_membrane import filter_membrane, label_neurons
from python_functions.handle_data.trimap import create_trimap
import numpy as np
from python_functions.handle_data.random_labels import get_number_of_labels, limit_label
from python_functions.quality.quality import accuracy, precision, recall
import matplotlib.pyplot as plt
from python_functions.handle_h5.handle_h5 import read_h5, save_h5
from python_functions.handle_data.binarize_labels import threshold

#create raw test block

#a = read_h5("/mnt/CLAWS1/stamilev/data/d.h5")
#b = cut_block(a, 25, 725, 0, 700, 0, 700)
#save_h5(b, "/home/stamylew/volumes/test_data.h5", "useful")
#    
#c = read_h5("/home/stamylew/volumes/test_data.h5", "useful")
#d = cut_block(c, 430, 580, 280, 430, 0, 150)

#save_h5(d, "/home/stamylew/volumes/test_cube2.h5", "150cube_raw")


#create gt and membrane test block

#e = read_h5("/mnt/CLAWS1/stamilev/data/ids_i_c_manualbigignore.h5")
#f = cut_block(e, 25, 725, 0, 700, 0, 700)
#save_h5(f, "/home/stamylew/volumes/test_gt.h5", "useful")

#g = read_h5("/home/stamylew/volumes/test_data/test_gt.h5", "useful")
#h = cut_block(g, 430, 580, 280, 430, 0, 150)
#save_h5(h, "/home/stamylew/volumes/test_cube2.h5", "150cube_gt")

#j = read_h5("/home/stamylew/volumes/test_data/test_cube2.h5", "150cube_gt")
#save_h5(j, "/home/stamylew/volumes/test_data/test_cube2.h5", "delme", None)
#i = filter_membrane(j)
#save_h5(i, "/home/stamylew/volumes/test_data/test_cube2_labeled.h5", "150cube_labeled2", None)

#create trimap

#i = read_h5("/home/stamylew/volumes/test_data/150cube.h5", "memb")
#h = read_h5("/home/stamylew/volumes/test_data/test_cube2.h5", "150cube_gt")
#j = create_trimap(i, h, 1)
#save_h5(j, "/home/stamylew/volumes/test_data/150cube.h5", "tri", None)

#binarize trained data
#
#j = read_h5("/home/stamylew/src/autocontext/training/cache/0000_test_cube2_probs.h5")
#k = np.squeeze(j)
#l = k[:,:,:,0]
#m = threshold(l, 0.2, 0.8)
#save_h5(m, "/home/stamylew/volumes/test_data/150cube_loops.h5", "n4")

#label number

#labels = read_h5("/home/stamylew/75cube_Labels.h5", "exported_data")
#nol = get_number_of_labels(labels)
#print nol
#limited = limit_label(labels, 499)
#save_h5(limited, "/home/stamylew/75cube_Labels_rand_500.h5", "", None)

#compare gt to predict

##for different number of loops

gt = read_h5("/home/stamylew/volumes/test_data/150cube.h5", "tri")
#n = read_h5("/home/stamylew/volumes/test_cube2.h5", "150cube_memb")
#o = read_h5("/home/stamylew/volumes/test_cube2_loops.h5", "n0")
#o = np.squeeze(o)
#o = o[:,:,:,0]
#p = read_h5("/home/stamylew/volumes/test_cube2_loops.h5", "n1")
#q = read_h5("/home/stamylew/volumes/test_cube2_loops.h5", "n2")
#r = read_h5("/home/stamylew/volumes/test_cube2_loops.h5", "n3")
s = read_h5("/home/stamylew/volumes/test_data/150cube_loops.h5", "n4")
#t = read_h5("/home/stamylew/volumes/test_cube2_loops.h5", "n5")
#u = read_h5("/home/stamylew/volumes/test_cube2_loops.h5", "n6")
#v = read_h5("/home/stamylew/volumes/test_cube2_loops.h5", "n7")
#w = read_h5("/home/stamylew/volumes/test_cube2_loops.h5", "n8")
#x = read_h5("/home/stamylew/volumes/test_cube2_loops.h5", "n9")
#y = read_h5("/home/stamylew/volumes/test_cube2_loops.h5", "n10")
#z = read_h5("/home/stamylew/volumes/test_cube2_loops.h5", "n11")

##for different label limits

#n = read_h5("/home/stamylew/volumes/test_cube2.h5", "75cube_memb")
#o = read_h5("/home/stamylew/volumes/test_cube2_labels.h5", "rand500_n4")

#plot results

a = accuracy 
b = precision
c = recall
print a(gt, s)
print 
print b(gt, s)
print 
print c(gt, s)

#plt.plot([0,1,2,3,4,5,6,7,8,9,10,11],[a(n,x),a(n,w),a(n,v),a(n,o),a(n,p),a(n,q),a(n,r),a(n,s),a(n,t),a(n,u),a(n,y),a(n,z)],'r-',
#         [0,1,2,3,4,5,6,7,8,9,10,11],[b(n,x),b(n,w),b(n,v),b(n,o),b(n,p),b(n,q),b(n,r),b(n,s),b(n,t),b(n,u),b(n,y),b(n,z)],'b-',
#         [0,1,2,3,4,5,6,7,8,9,10,11],[c(n,x),c(n,w),c(n,v),c(n,o),c(n,p),c(n,q),c(n,r),c(n,s),c(n,t),c(n,u),c(n,y),c(n,z)],'g-')
#plt.axis([-1,12,0,1])
#plt.show()

#plt.plot([0,1],[a(n,o),a(n,p)],'ro', [0,1],[b(n,o),b(n,p)],'bo', [0,1], [c(n,o),c(n,p)], 'go')
#plt.axis([-1,2, 0,1])
#plt.show()
print "done"