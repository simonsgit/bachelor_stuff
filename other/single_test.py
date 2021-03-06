# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 15:21:51 2015

@author: stamylew
"""

import os
import types
import socket
from subprocess import call
from python_functions.handle_h5.handle_h5 import save_h5, read_h5
from python_functions.other.host_config import assign_path
from python_functions.quality.quality import adjust_predict, save_quality_values
from python_functions.handle_data.new_modify_labels import reduce_labels_in_ilp, check_ilp_labels, concentrated_labels

#appendages for training command
def modify_loop_number(command, n):
    """Modify the loop parameter
    :param command: shell command for autocontext training
    :param n: number of loops
    :return: appended shell command
    """
    command.append("-n")
    command.append(str(n))
    return command

def modify_weights(command, weights):
    """ Modify the weights parameter
    :param command: shell command for autocontext training
    :param weights: weighting for the label distribution
    :return: appended shell command
    """
    command.append("--weights")
    for n in range(len(weights)):
        command.append(str(weights[n]))
    return command


#autocontext training
def ac_train(ilp, labels="", loops=3, weights="", t_cache = "", outpath= ""):
    """ Use autocontext train function and returns used shell command
    :param: ilp     :   path to ilp project
    :param: labels  :   number of labeled pixels
    :param: loops   :   number of loops
    :param: weights :   weighted label distribution
    :param: t_cache :   path to training cache folder
    :param: outpath :   outpath for the ilp file
    :return shell command
    """
    # Check if given parameters are valid
    if labels != "":
        assert type(labels) is types.IntType, "Labels parameter is not an integer: %d" % labels

    assert type(loops) is types.IntType, "Parameter loops is not an integer: %d" % loops

    if weights != "":
        print len(weights)
        print loops
        assert type(weights) is types.ListType, "Parameter weights is not a list: %d" % weights
        assert len(weights) == loops, "Parameter weights needs to have as many entries as loops."
        #modify weights

    #paths
    hostname = socket.gethostname()
    autocontext_path = assign_path(hostname)[4]
    ilastik_path = assign_path(hostname)[3]

    #reduce number of labeled pixels if wanted
    # if labels != "":
    #     print
    #     print "reducing labels to " + str(labels)
    #     ilp = reduce_labels_in_ilp(ilp, labels)

    #create ilp outpath
    if outpath != "":
        outpath = ilp.split(".")[-2] + "_out.ilp"

    #create training command
    command = ["python", autocontext_path, "--train", ilp, "-o", outpath,
               "--cache", t_cache, "--clear_cache", "--ilastik", ilastik_path]

    #modify shell command
    command = modify_loop_number(command, loops)
    command = modify_weights(command, weights)

    #call shell command
    call(command)
    return command


#autocontext batch prediction    
def ac_batch_predict(files, t_cache, p_cache = "", overwrite = "no"):
    """ Use autocontext batch prediction
    :param: files       :   files to do batch prediction on
    :param: t_cache     :   path to training cache folder
    :param: p_cache     :   path to prediction cache folder
    :param: overwrite   :   decides if prediction files should be overwritten after each iteration
    :return shell command
    """

    #paths
    hostname = socket.gethostname()
    autocontext_path = assign_path(hostname)[4]
    ilastik_path = assign_path(hostname)[3]


    #create batch command
    command = ["python", autocontext_path, "--batch_predict",
               t_cache, "--ilastik", ilastik_path,
               "--cache", p_cache, "--files", files]
    if overwrite == "no" or overwrite == "No":
        command.append("--no_overwrite")

    #clear cache
    command.append("--clear_cache")

    call(command)
    return command


#test
def test(ilp, files, gt_path, dense_gt_path, labels="", loops=3, weights="", repeats=1, outpath= "",
         t_cache = "", p_cache = ""):
    """ Run test
    :param: ilp             : path to ilp project to use for training
    :param: files           : path to file to do batch prediction on
    :param: gt_path         : path to trimap groundtruth
    :param: dense_gt_path   : path to dense groundtruth
    :param: labels          : amount of labeled pixels to use in training
    :param: loops           : amount of autocontext loops
    :param: weights         : weighting of the labels over the autocontext loops
    :param: repeats         : amount of repeat runs of the test
    :param: outpath         : outpath for test outputs
    :param: t_cache         : path to training data cache
    :param: p_cache         : path to prediction data cache
    """

    hostname = socket.gethostname()
    print "test information:"
    print
    print "hostname:", hostname
    print
    print "ilp_file:", ilp
    print
    print "files to predict:", files
    print
    print "groundtruth:", gt_path
    print
    print "dense groundtruth:", dense_gt_path
    print
    print "labels:", labels
    print
    print "loops:", loops
    print
    print "weights:", weights
    print
    print "repeats:", repeats

    # Collect the test specifications
    ilp_split = ilp.split(".")[-2]
    training_file = "training file: "+ilp_split.split("/")[-1]

    gt_split = gt_path.split(".")[-2]
    trimap_file = "trimap file: " + gt_split.split("/")[-1]


    # Assign paths
    filesplit = files.split(".")[-2]
    filename = filesplit.split("/")[-1]
    prediction_file = "prediction file: "+ filename

    test_folder_path = assign_path(hostname)[5]

    if t_cache == "":
        t_cache = test_folder_path + "/t_cache"

    if p_cache == "":
        p_cache = test_folder_path + "/p_cache/" + filename
        if not os.path.exists(p_cache):
            os.mkdir(p_cache)

    if outpath == "":
        output = test_folder_path + "/q_data"
    else:
        output = outpath

    print
    print "outpath:", outpath
    print
    print "t_cache:", t_cache
    print
    print "p_cache:", p_cache

    # Create file tags
    if labels == "":
        label_tag = "all"
    else:
        # assert labels == check_ilp_labels(ilp)
        true_labels = check_ilp_labels(ilp)
        label_tag = true_labels
    if weights == "":
        weight_tag = "none"
    else:
        weight_tag = str(weights)

    # Make folder for quality data

    if "manual" in ilp:
        filename += "_manual"
    if "hand_drawn" in ilp:
        filename += "_hand_drawn"
    if "clever" in ilp:
        filename += "_clever"
    if "less_feat" in ilp:
        filename += "_less_feat"


    #change labels for every test
    # if labels != "":
    #     print
    #     print "reducing labels to " + str(labels)
    #     ilp = reduce_labels_in_ilp(ilp, labels)

    file_dir = output + "/" + filename
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)

    # Overwrite folder directory
    # file_dir = "/mnt/CLAWS1/stamilev/delme"

    # Check if file directory exists, if not make such directory
    if not os.path.exists(file_dir):
        print
        print "Output folder did not exist."
        os.mkdir(file_dir)
        print
        print "New one named " + file_dir + " was created."

    q_outpath = file_dir + "/n_" + str(loops) + "_l_" + str(label_tag) + "_w_" + weight_tag
    prob_folder = q_outpath + "/prob_files"
    q_data_outpath = q_outpath + "/n_" + str(loops) + "_l_" + str(label_tag) + "_w_" + weight_tag + ".h5"


    # Check if test directory exists, if not make such directory
    if not os.path.exists(q_outpath):
        print
        print "Output h5 file did not exist"
        os.mkdir(q_outpath)
        os.mkdir(prob_folder)
        print
        print "New one named " + q_outpath + " was created."
    if not os.path.exists(prob_folder):
        os.mkdir(prob_folder)

    # Run the test
    for i in range(repeats):
        print
        print "round of repeats %d of %d" % (i+1, repeats)

        #train on ilp project
        ac_train(ilp, labels, loops, weights, t_cache, outpath)
        print
        print "training completed"

        #batch predict files
        ac_batch_predict(files, t_cache, p_cache, overwrite = "")
        print
        print "batch prediction completed"

        #save prob files and quality data
        prob_file = [x for x in os.listdir(p_cache) if ("probs" in x)]
        predict_path = p_cache + "/" + prob_file[0]
        predict_data = adjust_predict(read_h5(predict_path))
        prob_path = prob_folder + "/prob_"+ str(i+1)+ ".h5"
        # if os.path.exists(prob_path):
        #     # TODO:not working yet
        #     prob_path = prob_path.split("/")[-2] + "/new_" + prob_path.split("/")[-1]
        #     print prob_path
        save_h5(predict_data, prob_path, "data")
        save_quality_values(predict_path, gt_path, dense_gt_path, q_data_outpath, (0,49,99))

        #save test specification data
        save_h5([training_file, prediction_file, trimap_file], q_data_outpath, "used files", None)
        save_h5([labels],q_data_outpath, "autocontext_parameters/#labels")
        save_h5([loops], q_data_outpath, "autocontext_parameters/#loops")
        save_h5([str(weight_tag)], q_data_outpath, "autocontext_parameters/weights")
        print
        print "quality data saved"

    #save configuration data
    # call(["cp", predict_path, q_outpath])
    save_h5(["pmin", "minMemb", "minSeg", "sigMin", "sigWeights", "sigSmooth", "cleanCloseSeeds", "returnSeedsOnly"],
            q_data_outpath, "segmentation/wsDt parameters", None)
    save_h5(["edge_weights", "edgeLengths", "nodeFeatures", "nodeSizes", "nodeLabels", "nodeNumStop", "beta", "metric",
             "wardness", "out"], q_data_outpath, "segmentation/agglCl parameters", None)
    print
    print "quality data saved"

if __name__ == '__main__':
    hostname = socket.gethostname()

    ilp_folder = assign_path(hostname)[1]
    volumes_folder = assign_path(hostname)[2]
    ilp_file = ilp_folder + "100p_cube2_t_05.ilp"
    files = volumes_folder + "test_data/100p_cube1.h5/data"
    gt_path = volumes_folder + "groundtruth/trimaps/100p_cube1_trimap_t_05.h5"
    dense_gt_path = volumes_folder + "groundtruth/dense_groundtruth/100p_cube1_dense_gt.h5"

    ilp = reduce_labels_in_ilp(ilp_file, 10000)
    test(ilp, files, gt_path, dense_gt_path, 10000, 3, "", 10)


    print
    print "done"