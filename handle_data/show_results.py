# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 14:52:56 2015

@author: stamylew
"""

import matplotlib.pyplot as plt

from python_functions.handle_h5.handle_h5 import read_h5
from python_functions.handle_h5.handle_h5 import read_h5
import numpy as np
import os
from os.path import isfile, join, isdir


def sort_qdata(path, fixed_param):
    if "n_" in fixed_param:
        x_dim = "labels"
        fixed = 'n = ' + fixed_param.split("_")[-2]
    else:
        x_dim = "loops"
        fixed = 'l = ' + fixed_param.split("_")[-2]

    qdata_folders = [f for f in os.listdir(path) if (isdir(path)) and (fixed_param in f)]
    qtuple_list = []
    for qdata_folder in qdata_folders:
        print
        print qdata_folder
        inpath = join(path, qdata_folder)
        qdata = [g for g in os.listdir(inpath) if (isfile(join(inpath, g))) and "h5" in g]
        datapath = join(inpath, qdata[0])
        #print datapath
        xvar = read_h5(datapath, x_dim)
        xvar = xvar[0]
        print xvar
        apr = read_h5(datapath, "a_p_r_auc")
        acc= apr[:,0]
        pre= apr[:,1]
        rec= apr[:,2]
        auc= apr[:,3]
        qtuple = (xvar,np.mean(acc),np.std(acc),np.mean(pre),np.std(pre),np.mean(rec),np.std(rec),np.mean(auc),np.std(auc))
        qtuple_list.append(qtuple)

    sorted_qtuple = sorted(qtuple_list, key=lambda  tup: tup[0])
    return x_dim, sorted_qtuple, fixed

def create_plot(input, outpath = "/home/stamylew/test_folder/q_data/100p_cube2/diagrams/"):
    xlabel = input[0]
    qtuple = input[1]

    n = len(qtuple)
    title = 'Quality for ' + input[2]

    xpoints = []
    apoints = []
    aerr = []
    ppoints = []
    perr = []
    rpoints = []
    rerr = []
    aucpoints = []
    aucerr = []
    for i in range(n):
        xpoints.append(qtuple[i][0])
        apoints.append(qtuple[i][1])
        aerr.append(qtuple[i][2])
        ppoints.append(qtuple[i][3])
        perr.append(qtuple[i][4])
        rpoints.append(qtuple[i][5])
        rerr.append(qtuple[i][6])
        aucpoints.append(qtuple[i][7])
        aucerr.append(qtuple[i][8])

    if "loops" == xlabel:
        xrange = [min(xpoints)-0.5, max(xpoints)+0.5]
    elif "labels" == xlabel:
        xrange = [min(xpoints)-1000, max(xpoints)+1000]

    diag_name = outpath + input[2].split(" ")[0] + "_" + input[2].split(" ")[-1] + ".png"

    plt.figure()
    plt.plot(xpoints, apoints, '-ro', label = 'accuracy')
    plt.errorbar(xpoints,apoints, aerr, None, 'r-', 'r')
    plt.plot(xpoints, ppoints, '-go', label = 'precision')
    plt.errorbar(xpoints,ppoints, perr, None, 'g-', 'g')
    plt.plot(xpoints, rpoints, '-bo', label = 'recall')
    plt.errorbar(xpoints,rpoints, rerr, None, 'b-', 'b')
    plt.plot(xpoints, aucpoints, '-yo', label = 'auc_score')
    plt.errorbar(xpoints, aucpoints, aucerr, None, 'y-', 'y')
    plt.legend(loc = 'best')
    plt.xlabel(xlabel, fontsize=14, color='black')
    plt.ylabel('score', fontsize=14, color='black')
    plt.title(title)
    plt.xlim(xrange)
    plt.savefig(diag_name)
    plt.show()


    return xpoints, apoints, ppoints, rpoints

if __name__ == '__main__':
    path = "/home/stamylew/delme"
    #print sort_qdata(path, "l_1000_")
    q = sort_qdata(path, "l_1000_")
    create_plot(q,)
    #create_plot(r)