# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 18:02:05 2015

@author: stamylew
"""

from cut_block import cut_block
from handle_h5 import read_h5
from handle_h5 import save_h5
from create_membrane import filter_membrane
import numpy as np
from binarize_labels import binarize_dense_labels
from random_labels import get_number_of_labels, limit_label
from quality import accuracy, precision, recall
import matplotlib.pyplot as plt

#create raw test block

#a = read_h5("/mnt/CLAWS1/stamilev/data/d.h5")
#b = cut_block(a, 25, 725, 0, 700, 0, 700)
#save_h5(b, "/home/stamylew/volumes/test_data.h5", "useful", None)
    
#c = read_h5("/home/stamylew/volumes/test_data.h5", "useful")
#d = cut_block(c, 300, 375, 465, 540, 0, 75)
#print d.shape

#save_h5(d, "/home/stamylew/volumes/test_cube1.h5", "75cube_raw", None)


#create gt and membrane test block

#e = read_h5("/mnt/CLAWS1/stamilev/data/ids_i_c_manualbigignore.h5")
#f = cut_block(e, 25, 725, 0, 700, 0, 700)
#save_h5(f, "/home/stamylew/volumes/test_gt.h5", "useful", None)

#g = read_h5("/home/stamylew/volumes/test_gt.h5", "useful")
#h = cut_block(g, 300, 375, 465, 540, 0, 75)
##save_h5(h, "/home/stamylew/volumes/test_cube1.h5", "75cube_gt", None)
#
#i = filter_membrane(h)
#save_h5(i, "/home/stamylew/volumes/test_cube1.h5", "75cube_memb", None)

#binarize trained data
#
#j = read_h5("/home/stamylew/src/autocontext/training/cache/0000_test_cube1_probs.h5")
#k = np.squeeze(j)
#l = k[:,:,:,0]
#m = binarize_dense_labels(l, 0.2, 0.8)
#save_h5(m, "/home/stamylew/volumes/test_cube1a.h5", "rand500_n4", None)

#label number

#labels = read_h5("/home/stamylew/75cube_Labels.h5", "exported_data")
#nol = get_number_of_labels(labels)
#print nol
#limited = limit_label(labels, 499)
#save_h5(limited, "/home/stamylew/75cube_Labels_rand_500.h5", "", None)


#compare gt to predict

##for different number of loops

n = read_h5("/home/stamylew/volumes/test_cube1.h5", "75cube_memb")
o = read_h5("/home/stamylew/volumes/test_cube1a.h5", "bin_n3")
p = read_h5("/home/stamylew/volumes/test_cube1.h5", "bin_n4")
q = read_h5("/home/stamylew/volumes/test_cube1.h5", "bin_n5")
r = read_h5("/home/stamylew/volumes/test_cube1a.h5", "bin_n6")
s = read_h5("/home/stamylew/volumes/test_cube1.h5", "bin_n7")
t = read_h5("/home/stamylew/volumes/test_cube1.h5", "bin_n8")
u = read_h5("/home/stamylew/volumes/test_cube1a.h5", "bin_n9")
v = read_h5("/home/stamylew/volumes/test_cube1a.h5", "bin_n2")
w = read_h5("/home/stamylew/volumes/test_cube1a.h5", "bin_n1")
y = read_h5("/home/stamylew/volumes/test_cube1a.h5", "bin_n10")
z = read_h5("/home/stamylew/volumes/test_cube1a.h5", "bin_n11")
#x = read_h5("/home/stamylew/src/autocontext/training/cache/0000_test_cube1_probs.h5")
#x = np.squeeze(x)
#x = x[:,:,:,0]


##for different label limits

#n = read_h5("/home/stamylew/volumes/test_cube1.h5", "75cube_memb")
#o = read_h5("/home/stamylew/volumes/test_cube1a.h5", "rand500_n4")

#plotting results

a = accuracy 
b = precision
c = recall

plt.plot([1,2,3,4,5,6,7,8,9,10,11],[a(n,w),a(n,v),a(n,o),a(n,p),a(n,q),a(n,r),a(n,s),a(n,t),a(n,u),a(n,y),a(n,z)],'r-',
         [1,2,3,4,5,6,7,8,9,10,11],[b(n,w),b(n,v),b(n,o),b(n,p),b(n,q),b(n,r),b(n,s),b(n,t),b(n,u),b(n,y),b(n,z)],'b-',
         [1,2,3,4,5,6,7,8,9,10,11],[c(n,w),c(n,v),c(n,o),c(n,p),c(n,q),c(n,r),c(n,s),c(n,t),c(n,u),c(n,y),c(n,z)],'g-')
plt.axis([-1,12,0,1])
plt.show()

#plt.plot([0,1],[a(n,o),a(n,p)],'ro', [0,1],[b(n,o),b(n,p)],'bo', [0,1], [c(n,o),c(n,p)], 'go')
#plt.axis([-1,2, 0,1])
#plt.show()
print "done"