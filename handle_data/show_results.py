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


def sort_and_extract_quality_data(path, fixed_param, measurements):
    """
    :param path:
    :param fixed_param:
    :param measurements:
    :return:
    """
    # Find all relevant data folders
    data_folders = [f for f in os.listdir(path) if (isdir(path)) and (fixed_param in f)]

    # Create labels for plot
    if "n_" in fixed_param:
        x_dim = "labels"
        fixed = 'n = ' + fixed_param.split("_")[-2]
    else:
        x_dim = "loops"
        fixed = 'l = ' + fixed_param.split("_")[-2]

    # Sort data folders
    sorting_list = []
    for data_folder in data_folders:
        inpath = join(path, data_folder)
        h5file = [g for g in os.listdir(inpath) if (isfile(join(inpath, g))) and "h5" in g]
        h5file_path = join(inpath, h5file[0])
        x_value = read_h5(h5file_path, x_dim)
        sorting_list.append((x_value, data_folder))
    sorted_list = sorted(sorting_list, key=lambda tup: tup[0])
    sorted_data_folders = []
    for tuple in sorted_list:
        sorted_data_folders.append(tuple[1])

    # Extract quality data
    data = []
    for measurement in measurements:
        assert str(measurement) in ["accuracy", "precision", "recall", "auc_score", "rand index",
                                    "variation of information", "true positives", "false positives", "true negatives",
                                    "false negatives"], "Given Quality measurement %d not valid" % measurement
        x_values = []
        mean = []
        std = []
        for data_folder in sorted_data_folders:
            inpath = join(path, data_folder)
            h5file = [g for g in os.listdir(inpath) if (isfile(join(inpath, g))) and "h5" in g]
            h5file_path = join(inpath, h5file[0])
            #print datapath
            x_param = read_h5(h5file_path, x_dim)
            x_param = x_param[0]
            x_values.append(x_param)
            measurement_data = read_h5(h5file_path, "quality/"+str(measurement))
            mean.append(np.mean(measurement_data))
            std.append(np.std(measurement_data))
        data.append((str(measurement), x_values, mean, std))

    return x_dim, data, fixed


def create_plot(input_path, fixed_param, measurements, outpath = "/home/stamylew/test_folder/q_data/100p_cube2/diagrams/"):
    """
    :param input:
    :param outpath:
    :return:
    """

    x_dim, data_list, fixed = sort_and_extract_quality_data(input_path, fixed_param, measurements)

    # Amount of plots
    n = len(data_list)
    title = 'Quality for ' + fixed

    plt.figure()
    x_min = []
    x_max = []
    for data in data_list:
        x_min.append(min(data[1]))
        x_max.append(max(data[1]))
        plt.plot(data[1], data[2], label=data[0])
        plt.errorbar(data[1], data[2], data[3], None)

    if "loops" == x_dim:
        xrange = [min(x_min)-0.5, max(x_max)+0.5]
    elif "labels" == x_dim:
        xrange = [min(x_min)-1000, max(x_max)+1000]

    diag_name = outpath + fixed.split(" ")[0] + "_" + fixed.split(" ")[-1] + ".png"
    plt.legend(loc = 'best')
    plt.title(title)
    plt.xlim(xrange)
    plt.xlabel(x_dim, fontsize=14, color='black')
    plt.ylabel('score', fontsize=14, color='black')
    plt.show()
    #
    # plt.figure()
    # plt.subplot(211)
    # plt.plot(xpoints, apoints, '-ro', label = 'accuracy')
    # plt.errorbar(xpoints,apoints, aerr, None, 'r-', 'r')
    # plt.plot(xpoints, ppoints, '-go', label = 'precision')
    # plt.errorbar(xpoints,ppoints, perr, None, 'g-', 'g')
    # plt.plot(xpoints, aucpoints, '-yo', label = 'auc_score')
    # plt.errorbar(xpoints, aucpoints, aucerr, None, 'y-', 'y')
    # plt.title(title)
    # plt.legend(loc = 'best', prop={'size':12})
    # plt.xlabel(x_dim, fontsize=14, color='black')
    # plt.ylabel('score', fontsize=14, color='black')
    # plt.xlim(xrange)
    # plt.subplot(212)
    # plt.plot(xpoints, rpoints, '-bo', label = 'recall')
    # plt.errorbar(xpoints,rpoints, rerr, None, 'b-', 'b')

    # plt.xlim(xrange)
    # plt.savefig(diag_name)
    # plt.show()
    #
    # return xpoints, apoints, ppoints, rpoints


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

    #create_plot(path1, "n_3_")
    x_dim, data, fixed = sort_and_extract_quality_data(path1, "l_20000_", ["precision", "recall"])
    create_plot(path1, "l_20000_", ["precision", "recall", "rand index"])
    #print data



    # s = sort_and_extract_qdata(path1, "n_3_")
    # t = sort_and_extract_qdata(path1, "n_4_")
    # u = sort_and_extract_qdata(path1, "n_5_")
    # v = sort_and_extract_qdata(path1, "n_6_")
    # w = sort_and_extract_qdata(path1, "n_7_")
    # x = sort_and_extract_qdata(path1, "n_8_")
    # y = sort_and_extract_qdata(path1, "n_9_")
    # z = sort_and_extract_qdata(path1, "n_10")


    #compare_plots("pre", (q,r))

