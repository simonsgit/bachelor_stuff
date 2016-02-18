# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 14:52:56 2015

@author: stamylew
"""

import matplotlib.pyplot as plt

from python_functions.handle_h5.handle_h5 import read_h5
import numpy as np
import os
from os.path import isfile, join, isdir


def sort_and_extract_qdata(path, fixed_param):
    """
    :param path:
    :param fixed_param:
    :return:
    """

    # Create labels for plot
    if "n_" in fixed_param:
        x_dim = "labels"
        fixed = 'n = ' + fixed_param.split("_")[-2]
    else:
        x_dim = "loops"
        fixed = 'l = ' + fixed_param.split("_")[-2]

    qdata_folders = [f for f in os.listdir(path) if (isdir(path)) and (fixed_param in f)]
    qtuple_list = []
    for qdata_folder in qdata_folders:
        inpath = join(path, qdata_folder)
        qdata = [g for g in os.listdir(inpath) if (isfile(join(inpath, g))) and "h5" in g]
        datapath = join(inpath, qdata[0])
        #print datapath
        xvar = read_h5(datapath, x_dim)
        xvar = xvar[0]
        qv = read_h5(datapath, "quality_values")
        acc= qv[:,0]
        pre= qv[:,1]
        rec= qv[:,2]
        auc= qv[:,3]
        ri = qv[:,4]
        voi= qv[:,5]
        ds = qv[:,6]
        tp = qv[:,7]
        fp = qv[:,8]
        tn = qv[:,9]
        fn = qv[:,10]

        qdata_tuple = (xvar,np.mean(acc),np.std(acc),np.mean(pre),np.std(pre),np.mean(rec),np.std(rec),np.mean(auc),np.std(auc),
                       np.mean(ri), np.std(ri), np.mean(voi), np.std(voi), np.mean(ds), np.std(ds), np.mean(tp), np.std(tp),
                       np.mean(fp), np.std(fp), np.mean(tn), np.std(tn), np.mean(fn), np.mean(fn))
        qtuple_list.append(qdata_tuple)

    sorted_qtuple = sorted(qtuple_list, key=lambda  tup: tup[0])
    return x_dim, sorted_qtuple, fixed

def create_plot(input, outpath = "/home/stamylew/test_folder/q_data/100p_cube2/diagrams/"):
    """
    :param input:
    :param outpath:
    :return:
    """

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
    plt.subplot(211)
    plt.plot(xpoints, apoints, '-ro', label = 'accuracy')
    plt.errorbar(xpoints,apoints, aerr, None, 'r-', 'r')
    plt.plot(xpoints, ppoints, '-go', label = 'precision')
    plt.errorbar(xpoints,ppoints, perr, None, 'g-', 'g')
    plt.plot(xpoints, aucpoints, '-yo', label = 'auc_score')
    plt.errorbar(xpoints, aucpoints, aucerr, None, 'y-', 'y')
    plt.title(title)
    plt.legend(loc = 'best', prop={'size':12})
    plt.xlabel(xlabel, fontsize=14, color='black')
    plt.ylabel('score', fontsize=14, color='black')
    plt.xlim(xrange)
    plt.subplot(212)
    plt.plot(xpoints, rpoints, '-bo', label = 'recall')
    plt.errorbar(xpoints,rpoints, rerr, None, 'b-', 'b')
    plt.legend(loc = 'best')
    plt.xlabel(xlabel, fontsize=14, color='black')
    plt.ylabel('score', fontsize=14, color='black')
    plt.xlim(xrange)
    plt.savefig(diag_name)
    plt.show()

    return xpoints, apoints, ppoints, rpoints


def compare_plots(measurement, plot_data_sets):
    """
    :param measurement:
    :param plot_data_sets:
    :return:
    """

    # determine which measurement is plotted
    if measurement == "acc":
        m = 1
        score = "accuracy score"
    elif measurement == "pre":
        m = 3
        score = "precision score"
    elif measurement == "rec":
        m = 5
        score = "recall score"
    elif measurement == "auc":
        m = 7
        score = "auc score"
    else:
        raise Exception("No valid measurement input given. Either acc, pre, rec or auc allowed.")

    title = "Comparison of " + score

    for plot_data in plot_data_sets:
        x_label = plot_data[0]

        x_points = []
        y_points = []
        y_error = []
        y_data = plot_data[1]
        colors = ['-r', '-b']
        for i in range(len(y_data)):
            x_points.append(y_data[i][0])
            y_points.append(y_data[i][m])
            y_error.append(y_data[i][m+1])
        if "loops" == x_label:
            x_range = [min(x_points)-0.5, max(x_points)+0.5]
        elif "labels" == x_label:
            x_range = [min(x_points)-1000, max(x_points)+1000]
        plt.plot(x_points, y_points, '-', label = plot_data[2])
        plt.errorbar(x_points, y_points, y_error, None)
        plt.legend()
    plt.xlabel(x_label, fontsize=14, color='black')
    plt.ylabel('score', fontsize=14, color='black')
    plt.title(title)

    plt.xlim(x_range)
    plt.show()

if __name__ == '__main__':
    path1 = "/home/stamylew/test_folder/q_data/100p_cube2"
    path2 = "/home/stamylew/test_folder/q_data/100p_cube2_t09"
    path3 = "/home/stamylew/test_folder/q_data/100p_cube2_t15"
    # print sort_and_extract_qdata(path, "l_1000_")
    q = sort_and_extract_qdata(path1, "n_3_")
    create_plot(q)

    r = sort_and_extract_qdata(path2, "l_10000_")

    s = sort_and_extract_qdata(path3, "l_10000_")

    # s = sort_and_extract_qdata(path1, "n_3_")
    # t = sort_and_extract_qdata(path1, "n_4_")
    # u = sort_and_extract_qdata(path1, "n_5_")
    # v = sort_and_extract_qdata(path1, "n_6_")
    # w = sort_and_extract_qdata(path1, "n_7_")
    # x = sort_and_extract_qdata(path1, "n_8_")
    # y = sort_and_extract_qdata(path1, "n_9_")
    # z = sort_and_extract_qdata(path1, "n_10")


    #compare_plots("pre", (q,r))

