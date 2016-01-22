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
    """Creates a bool array where entries with the given label number  as value are True and everything else False
    :param data:            data array
    :param label_number:    label number
    :return: Bool array
    """

    #create bool array
    selected_label = data == label_number

    return selected_label

def filter_label(data, percentage):
    """Filters the data so that the given percentage of all entries remains non-zero
    :param data:        data array
    :param percentage:  percentage of entries that remains non-zero
    :return: Filtered data array
    """

    #create random array    
    random = np.random.random(data.shape) 

    #randomization of labels
    rol = data * random

    #determine amount of labeled pixels
    nolp = np.sum(data)
    #print "nolp", nolp

    #determine amount of all pixels
    total = data.size

    #calculate percentage of labeled pixels
    q = (total - round(percentage * nolp, 0)) / total * 100

    #calculate percentile value
    limit = np.percentile(rol, q)

    #filter all entries <= percentile value
    sol = rol > limit

    #convert bool to int
    sol = sol.astype(np.uint8)

    return sol
        
    
def filter_all_labels(data, percentage):
    """Filters over all labels
    :param data: data array
    :param percentage: percentage of entries that remains non-zero
    :return: Filtered data array
    """

    #create list to contain label data
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
    """Returns the amount of non-zero entries
    :param data: data array
    :return: Amount of labeled pixels in data
    """

    #filter all labeled pixels
    labeled_pixels = data != 0

    #count all labeled pixels
    number_of_labels = np.sum(labeled_pixels)

    return number_of_labels
    
    
def limit_label(data, limit, nolp=""):
    """Limits amount of labeled pixels in data array to given limit
    :param data:    data array
    :param limit:   limit
    :param nolb:    number of labeled pixels
    :return: Data array with reduced amount of labeled pixels
    """

    #get number of labeled pixels
    if nolp == "":
        nol = get_number_of_labels(data)
        #make nol float typ
        nol = nol.astype(np.float128)
    else:
        nol = nolp

    #reduces number labeled pixels if limit < nol
    if limit < nol:
        percentage = limit / nol

        limited_data = filter_all_labels(data, percentage)

        return limited_data
    else:
        print
        print "Limit exceeds amount of labeled pixels"
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
