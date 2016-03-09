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
        fixed_value = 'n = ' + fixed_param.split("_")[-2]
    else:
        x_dim = "loops"
        fixed_value = 'l = ' + fixed_param.split("_")[-2]

    # Sort data folders
    sorting_list = []
    for data_folder in data_folders:
        inpath = join(path, data_folder)
        h5file = [g for g in os.listdir(inpath) if (isfile(join(inpath, g))) and fixed_param in g and "h5" in g]
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
            h5file = [g for g in os.listdir(inpath) if (isfile(join(inpath, g))) and fixed_param in g and "h5" in g]
            h5file_path = join(inpath, h5file[0])
            #print datapath
            x_param = read_h5(h5file_path, x_dim)
            x_param = x_param[0]
            x_values.append(x_param)
            measurement_data = read_h5(h5file_path, "quality/"+str(measurement))
            mean.append(np.mean(measurement_data))
            std.append(np.std(measurement_data))
        data.append((str(measurement), x_values, mean, std))

    return x_dim, data, fixed_value


def create_plot(input_path, fixed_param, measurements, outpath = "/home/stamylew/test_folder/q_data/100p_cube2/diagrams/"):
    """
    :param input:
    :param outpath:
    :return:
    """

    x_dim, data_list, fixed_value = sort_and_extract_quality_data(input_path, fixed_param, measurements)

    # Amount of plots
    n = len(data_list)
    title = 'Quality for ' + fixed_value

    plt.figure()
    x_min = []
    x_max = []
    for data in data_list:
        position = data_list.index(data)
        x_min.append(min(data[1]))
        x_max.append(max(data[1]))
        plt.errorbar(data[1], data[2], data[3], None, label=data[0])

    if "loops" == x_dim:
        xrange = [min(x_min)-0.5, max(x_max)+0.5]
    elif "labels" == x_dim:
        xrange = [min(x_min)-1000, max(x_max)+1000]

    diag_name = outpath + fixed_value.split(" ")[0] + "_" + fixed_value.split(" ")[-1] + ".png"

    plt.legend(loc = 'best')
    plt.title(title)
    plt.xlim(xrange)
    plt.xlabel(x_dim, fontsize=14, color='black')
    plt.ylabel('score', fontsize=14, color='black')
    plt.show()


def compare_plots(inpaths, fixed_params, measurements):
    """
    :param measurement:
    :param plot_data_sets:
    :return:
    """

    plot_data_sets = []
    for inpath in inpaths:
        data_set_name = inpath.split("/")[-1]
        for fixed_param in fixed_params:
            x_dim, data_list, fixed = sort_and_extract_quality_data(inpath, fixed_param, measurements)
            plot_data_sets.append((data_set_name, fixed_param, x_dim, data_list, fixed))

    x_min = []
    x_max = []
    plt.figure()
    for plot_data in plot_data_sets:
        print plot_data
        data_set_name, fixed_param, x_dim, data_list, fixed = plot_data

        # Plot the plots
        for data in data_list:

            #name label and title
            if len(inpaths) > 1:
                label = data[0] + " " + data_set_name
                title = "Comparison between blocks"
            elif len(fixed_params) > 1:
                label = data[0] + " " + fixed_param.split("_")[0] + "=" + fixed_param.split("_")[1]
                title = "Comparison between fixed parameters"
            else:
                label = data[0]
                title = "Comparison between measurements "
            x_min.append(min(data[1]))
            x_max.append(max(data[1]))
            plt.errorbar(data[1], data[2], data[3], None, label= label)

        if "loops" == x_dim:
            xrange = [min(x_min)-0.5, max(x_max)+0.5]
        elif "labels" == x_dim:
            xrange = [min(x_min)-1000, max(x_max)+1000]

    plt.xlabel(x_dim, fontsize=14, color='black')
    plt.ylabel('score', fontsize=14, color='black')
    plt.title(title)
    plt.legend(loc = 'best')
    plt.xlim(xrange)
    plt.show()


if __name__ == '__main__':
    path1 = "/home/stamylew/test_folder/q_data/200p_cube3_t05"
    path2 = "/home/stamylew/test_folder/q_data/200p_cube3"
    path3 = "/home/stamylew/test_folder/q_data/200p_cube3"
    # print sort_and_extract_qdata(path, "l_1000_")

    fixed_param1 = "l_10000_"
    fixed_param2 = "n_3_"

    measurement1 = "rand index"
    measurement2 = "variation of information"
    measurement3 = "precision"
    measurement4 = "recall"
    #create_plot(path1, "n_3_")
    #x_dim, data, fixed = sort_and_extract_quality_data(path1, "l_20000_", ["precision", "recall"])

    # create_plot(path1, "l_10000_", ["precision", "recall", "rand index"])
    # create_plot(path1, "l_10000_", ["variation of information"])

    compare_plots([path1, path2], [fixed_param2], [measurement1])
    # print data



    # s = sort_and_extract_qdata(path1, "n_3_")
    # t = sort_and_extract_qdata(path1, "n_4_")
    # u = sort_and_extract_qdata(path1, "n_5_")
    # v = sort_and_extract_qdata(path1, "n_6_")
    # w = sort_and_extract_qdata(path1, "n_7_")
    # x = sort_and_extract_qdata(path1, "n_8_")
    # y = sort_and_extract_qdata(path1, "n_9_")
    # z = sort_and_extract_qdata(path1, "n_10")


    #compare_plots("pre", (q,r))

