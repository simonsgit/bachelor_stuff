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


def sort_and_extract_quality_data(path, fixed_param, x_dim, measurements):
    """
    :param path:
    :param fixed_param:
    :param measurements:
    :return:
    """
    # Find all relevant data folders
    data_folders = [f for f in os.listdir(path) if (isdir(path)) and (fixed_param in f) and ("h5" not in f)]
    print data_folders

    # Create labels for plot
    if "n_" in fixed_param:
        fixed_value = 'n = ' + fixed_param.split("_")[-2]
    elif "l_" in fixed_param:
        fixed_value = 'l = ' + fixed_param.split("_")[-2]
    elif "w_"in fixed_param:
        fixed_value = 'w = ' + fixed_param.split("_")[-2]
    else:
        raise Exception("Can't read fixed_parameter input")

    # Sort data folders
    sorting_list = []
    for data_folder in data_folders:
        inpath = join(path, data_folder)
        h5file = [g for g in os.listdir(inpath) if (isfile(join(inpath, g))) and fixed_param in g and "h5" in g]
        h5file_path = join(inpath, h5file[0])
        x_value = read_h5(h5file_path, "autocontext_parameters/"+x_dim)
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
                                    "false negatives"], "Given Quality measurement %s not valid" % measurement
        x_values = []
        mean = []
        std = []
        for data_folder in sorted_data_folders:
            inpath = join(path, data_folder)
            h5file = [g for g in os.listdir(inpath) if (isfile(join(inpath, g))) and fixed_param in g and "h5" in g]
            h5file_path = join(inpath, h5file[0])
            #print datapath
            x_param = read_h5(h5file_path, "autocontext_parameters/"+x_dim)
            x_param = x_param[0]
            x_values.append(x_param)
            measurement_data = read_h5(h5file_path, "quality/"+str(measurement))
            mean.append(np.mean(measurement_data))
            std.append(np.std(measurement_data))
        data.append((str(measurement), x_values, mean, std))

    return x_dim, data, fixed_value,


def create_plot(input_path, fixed_param, x_dim, measurements, save_fig = False, outpath = "/home/stamylew/test_folder/q_data/100p_cube2/diagrams/"):
    """
    :param input:
    :param outpath:
    :return:
    """

    x_dim, data_list, fixed_value = sort_and_extract_quality_data(input_path, fixed_param, x_dim, measurements)

    # Amount of plots
    n = len(data_list)
    title = 'Quality for ' + fixed_value

    plt.figure()
    x_min = []
    x_max = []
    for data in data_list:
        x_points = np.arange(len(data[1]))
        x_min.append(min(data[1]))
        x_max.append(max(data[1]))
        xticks = data[1]
        plt.errorbar(x_points, data[2], data[3], None, label=data[0])
        plt.xticks(x_points, xticks)

    if "#loops" == x_dim or "weights" == x_dim:
        xrange = [x_points[0]-0.5, x_points[-1]+0.5]
    elif "#labels" == x_dim:
        xrange = [min(x_min)-1000, max(x_max)+1000]

    folder_path = input_path + "/figures/"
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    diag_name = folder_path + measurements[0] + "_over_"+ x_dim + "_with_"+fixed_value.split(" ")[0] + "_" + fixed_value.split(" ")[-1] + ".png"

    y_dim = 'score'
    if "true" in measurements[0] or "false" in measurements[0]:
        y_dim = '#pixels'
    plt.legend(loc = 'best')
    plt.title(title)
    plt.xlim(xrange)
    plt.xlabel(x_dim, fontsize=14, color='black')
    plt.ylabel(y_dim, fontsize=14, color='black')
    if save_fig:
        plt.savefig(diag_name)
    plt.show()


def compare_plots(inpaths, fixed_params, x_dim, measurements):
    """
    :param measurement:
    :param plot_data_sets:
    :return:
    """

    plot_data_sets = []
    for inpath in inpaths:
        data_set_name = inpath.split("/")[-1]
        for fixed_param in fixed_params:
            x_dim, data_list, fixed = sort_and_extract_quality_data(inpath, fixed_param, x_dim, measurements)
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
            x_points = np.arange(len(data[1]))
            x_min.append(min(data[1]))
            x_max.append(max(data[1]))
            xticks = data[1]
            plt.errorbar(x_points, data[2], data[3], None, label= label)
            plt.xticks(x_points, xticks)

        if "#loops" == x_dim or "weights" == x_dim:
            xrange = [x_points[0]-0.5, x_points[-1]+0.5]
        elif "#labels" == x_dim:
            xrange = [min(x_min)-1000, max(x_max)+1000]

    plt.xlabel(x_dim, fontsize=14, color='black')
    plt.ylabel('score', fontsize=14, color='black')
    plt.title(title)
    plt.legend(loc = 'best')
    plt.xlim(xrange)
    plt.show()
    plt.close()


if __name__ == '__main__':
    path1 = "/home/stamylew/test_folder/q_data/100p_cube3_random"
    path2 = "/home/stamylew/test_folder/q_data/100p_cube3_hand_drawn"
    path3 = "/home/stamylew/test_folder/q_data/100p_cube3"
    # print sort_and_extract_qdata(path, "l_1000_")

    fixed_param1 = "l_10000_"
    fixed_param2 = "l_20000_"
    fixed_param3 = "n_3_"

    measurement1 = "rand index"
    measurement2 = "variation of information"
    measurement3 = "precision"
    measurement4 = "recall"
    measurement5 = "true positives"
    measurement6 = "false positives"
    measurement7 = "true negatives"
    measurement8 = "false negatives"
    #create_plot(path1, "n_3_")
    #x_dim, data, fixed = sort_and_extract_quality_data(path1, "l_20000_", ["precision", "recall"])

    # create_plot(path3, "l_10000_", "weights", ["precision", "recall"])
    # create_plot(path1, fixed_param1, "#loops", [measurement8])
    create_plot(path1, fixed_param2, "#loops", [measurement4], False)

    # compare_plots([path1, path2], [fixed_param1], "#loops",[measurement3])
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

