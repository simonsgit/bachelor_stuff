# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 16:28:31 2015

@author: stamylew
"""

import numpy as np
from python_functions.handle_h5.handle_h5 import read_h5, save_h5
from autocontext.core.ilp import ILP
import matplotlib.pyplot as plt

def select_label(data, label_number):
    selected_label = data == label_number
    return selected_label

def filter_label(data, percentage):
    """
    :param data:
    :param percentage:
    :return:
    """

    #create random array    
    random = np.random.random(data.shape) 

    #randomization of labels
    rol = data * random

    #determine amount of labeled pixels
    nolp = np.sum(data)
    #print "nolp", nolp

    #determine amount of all pixels
    assert data.size == data.shape[0] * data.shape[1] * data.shape[2]
    total = data.size

    #calculate percentage of labeled pixels
    q = (total - round(percentage * nolp)) / total * 100

    #calculate percentile value
    limit = np.percentile(rol, q)

    #filter all entries <= percentile value
    sol = rol > limit

    #convert bool to int
    sol = sol.astype(np.uint8)
    #print "number of labels", get_number_of_labels(sol)
    return sol
        
    
def filter_all_labels(data, percentage):
    #list to contain label data
    lol = []
    #get individual label data
    for i in np.unique(data):
        #print "label", i
        g = select_label(data, i)
        j = filter_label(g, percentage)*i
        lol.append(j)
    #combine individual label data
    al = lol[0]
    for i in range(1, len(lol)):
        al += lol[i]
    return al

def get_number_of_labels(data):
    #filter all labeled pixels
    labeled_pixels = data > 0
    #count all labeled pixels
    number_of_labels = np.sum(labeled_pixels)
    return number_of_labels 
    
    
def limit_label(data, limit):
    print
    print "limit:", limit
    #get number of labeled pixels
    nol = get_number_of_labels(data)
    print
    print "nol of pixels in raw:", nol
    #make nol float typ
    nol = nol.astype(np.float128)
    #reduces number labeled pixels if limit < nol
    if limit < nol:
        percentage = limit / nol
        print "percentage"
        print percentage        
        limited_data = filter_all_labels(data, percentage)
        print
#        assert(limit >= get_number_of_labels(limited_data))
        return limited_data
    else:
        return data


if __name__ == '__main__':
    a = "/home/stamylew/volumes/groundtruth/trimaps/500p_cube1_trimap_t_05.h5"
    b = read_h5(a)
    print get_number_of_labels(b)
    #print "working file:", np.unique(b)
    # c = filter_all_labels(b, 0.5)
    # print get_number_of_labels(c)
    d = limit_label(b, 10000)
    print get_number_of_labels(d)
    
#    print "real number" 
#    print get_number_of_labels(g)
#    j = select_label(g,1)
#    k = filter_label(g, 0.5)
#    
#    save_h5(k, "/home/stamylew/test.h5")
#
#    l = filter_all_labels(g, 0.5)
#    save_h5(l, "/home/stamylew/random_labels/test4.h5")
#    
#    m = limit_label(g, 1000)
#    print "nol in result"
#    print get_number_of_labels(m)
#    save_h5(m, "/home/stamylew/volumes/trimaps/50cube1_tri_1500.h5","1500labels")
#     print "not working file:"
#     f = "/home/stamylew/ilastik_projects/smallcubes_copy.ilp"
#     g = ILP(f, "/home/stamylew/delme")
#     print g.get_labels(0)
#     h, t = g.get_labels(0)
#     i = h[0]
#     print i.shape
#     j = filter_all_labels(i, 0.5)
#     print j.shape
#
#     plt.figure()
#     plt.imshow(b[0,:,:])
#
#     plt.figure()
#     plt.imshow(c[0,:,:])
#
#     plt.figure()
#     plt.imshow(i[0,:,:,0])
#
#     plt.figure()
#     plt.imshow(j[0,:,:,0])
#
#     plt.show()
#    Label_number = np.unique(data)[i]
#    #lol=[]
#    
#    all_filtered_labels = np.zeros(data.shape)
#    
#    for i in range(1, nol):
#        sol = filter_label(inpath, percentage, i, outpath="/home/stamylew/temp/")
#        all_filtered_labels[sol] = i        
        #lol.append(sol)
    print "done"




####old function:

#nol = np.amax(data) #number of labels
#print nol
#
#tol = np.unique(data) #number of labels
#print tol
#
#check = len(tol) - 1
#
#assert(check == nol)
#
#label = [] #list of labels
#rol = []
#
#for i in range(1, len(tol)): #creates list of label data
#    label.append(data == i)
#    random = np.random.random(data.shape) #create array with random values between 0 and 1
#    rol.append(random * label[i])
#
#
#rol1 = label[0] * random #randomization_of_label1
#
#s = sum(label[0]) #number of pixels labeled by label1
#
#total = data.shape[0] * data.shape[1] * data.shape[2] #total number of pixels of data
#
#
#p = 0.3 #wanted percentage of labeled pixels
#
#q = (total - p*s) / total * 100 #percentile
#print q
#
#subset = np.percentile(rol1, q) #qth percentile
#
#sol1 = rol1 > subset #selection of label1 dtype=bool
#print subset
#print sol1[35:37, 66:68, 66:68]
#print sum(sol1)


#r = np.random.random(100)
#
#p = np.percentile(r, 90)
#
#print r
#print p
#
#print r>p
#print r<p
#
#print np.sum(r>p)
#print np.sum(r<p)

#quit()
#
#
#
#
#
#print "datatype of data:"
#print data.dtype
#
#label1 = data == 1 #filter label 1
#label2 = data == 2 #filter label 2
#all_labels = data >= 1 #all labels
#
#random = np.random.random(data.shape) #create array with random values between 0 and 1
#
#randomization_label1 = np.multiply(random, label1) #multiply label1 array with random array elementwise
#
#
#
#b = randomization_label1 > 0.5
#
#b = b.astype(np.int32)
#b = b.astype(np.bool)
#b = b.astype(np.float)
#
#print randomization_label1[b] 
#
#
#
#random_label1 = threshold(randomization_label1, 0.5) 
#print "shape"
#print random_label1.shape
#random_label1[random_label1 > 0]= int(1) #reset label array
#
#print "datatype of random_label1:"
#print random_label1.dtype
#print random_label1[35:37, 66:68, 66:68]

