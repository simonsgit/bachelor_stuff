# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 15:21:51 2015

@author: stamylew
"""

from subprocess import call
from python_functions.handle_data.modify_labels import reduce_labels_in_ilp
from python_functions.handle_data.archive import archive_qdata
from python_functions.handle_h5.handle_h5 import save_h5, read_h5
from python_functions.other.host_config import assign_path
import socket
import os
import numpy as np


#appendages for training and batch prediction commands
def clear_cache(command, answer):
    if answer == "y" or answer == "Y":
        command.append("--clear_cache")
        return command
    else:
        return command

def modify_loop_number(command, n):
    command.append("-n") 
    command.append(str(n))
    return command
   
def modify_weights(command, weights):
    command.append("--weights")
    for n in range(len(weights)):
        command.append(str(weights[n]))
    return command


#autocontext training
def ac_train(ilp, labels="", loops=3, weights="", t_cache = "", outpath= ""):
    """ Use autocontext train function
    :param: ilp     :   path to ilp project
    :param: labels  :   number of labeled pixels
    :param: loops   :   number of loops
    :param: weights :   weighted label distribution
    :param: t_cache :   path to training cache folder
    :param: outpath :   outpath for the ilp file
    """

    #paths
    hostname = socket.gethostname()
    autocontext_path = assign_path(hostname)[3]
    ilastik_path = assign_path(hostname)[2]

    #reduce number labeled pixels if wanted
    if labels != "":
        print
        print "modify labels:"
        ilp = reduce_labels_in_ilp(ilp, labels)
    
    #create outpath    
    if outpath != "":
        outpath = ilp.split(".")[-2] + "_out.ilp"

    #create training command
    command = ["python", autocontext_path,
          "--train", ilp, "-o", outpath, "--cache", t_cache, "--clear_cache",
        "--ilastik", ilastik_path]


    #modify loop number
    command = modify_loop_number(command, loops)
    
    #modify weights
    command = modify_weights(command, weights)

    call(command)
    return command


#autocontext batch prediction    
def ac_batch_predict(files, t_cache, p_cache = "", overwrite = "no"):
    """ Use autocontext batch prediction
    :param: files       :   files to do batch prediction on
    :param: t_cache     :   path to training cache folder
    :param: p_cache     :   path to prediction cache folder
    :param: overwrite   :   decides if prediction files should be overwritten after each iteration
    """

    #path
    hostname = socket.gethostname()
    autocontext_path = assign_path(hostname)[3]
    ilastik_path = assign_path(hostname)[2]


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
def test(ilp, files, gt, labels="", loops=3, weights="", repeats=1, outpath= "",
         t_cache = "", p_cache = ""):
    """get quality values of batch predicition for adjusted number of labels, loops and weights
    """

    #path
    hostname = socket.gethostname()
    test_folder_path = assign_path(hostname)[4]

    if t_cache == "":
        t_cache = test_folder_path + "/t-cache"

    if p_cache == "":
        p_cache = test_folder_path + "/p_cache"

    if outpath == "":
        output = test_folder_path + "/q_data"
    else:
        output = outpath

    #create file tags
    if labels == "":
        label_tag = "all"
    else:
        label_tag = labels

    if weights == "":
        weight_tag = "none"
    else:
        weight_tag = str(weights)

    #make folder
    filesplit = files.split(".")[-2]
    filename = filesplit.split("/")[-1]
    file_dir = output + "/" + filename

    if not os.path.exists(file_dir):
        os.mkdir(file_dir)

    q_outpath = file_dir + "/n_" + str(loops) + "_l_" + str(label_tag) + "_w_" + weight_tag
    q_data_outpath = q_outpath + "/n_" + str(loops) + "_l_" + str(labels) + "_w_" + weight_tag + ".h5"

    if not os.path.exists(q_outpath):
        os.mkdir(q_outpath)
        qdata = np.zeros((repeats, 4), dtype= np.float)
    else:
        old_qdata = read_h5(q_data_outpath, "a_p_r_auc")
        qdata = np.zeros((repeats +  old_qdata.shape[0], 4), dtype= np.float)
        qdata[repeats::] = old_qdata

    # #create outpath
    # q_data_outpath = q_outpath + "/n_" + str(loops) + "_l_" + str(labels) + "_w_" + str(weights) + ".h5"
    # save_h5([labels],q_data_outpath, "labels")
    # save_h5([loops], q_data_outpath, "loops")

    for i in range(repeats):
        print
        print "round of repeats:", i
        #train ilp file
        ac_train(ilp, labels, loops, weights, t_cache, outpath)
        print
        print "trained"

        #batch predict files
        ac_batch_predict(files, t_cache, p_cache, overwrite = "")
        print
        print "batch predicted"

        #archive data
        archive_qdata(p_cache + "/", gt, qdata, i, q_data_outpath, 0)
        print
        print "archived"

    save_h5([filename], q_data_outpath, "filename")
    save_h5(qdata, q_data_outpath, "a_p_r_auc", None)
    save_h5([labels],q_data_outpath, "labels")
    save_h5([loops], q_data_outpath, "loops")
    print
    print "saved"

if __name__ == '__main__':
    hostname = socket.gethostname()
    print
    print "hostname:", hostname

    ilp_folder = assign_path(hostname)[0]
    volumes_folder = assign_path(hostname)[1]
    ilp_file = ilp_folder + "100p_cube1.ilp"
    files = volumes_folder + "test_data/100p_cube2.h5/data"
    gt = volumes_folder + "groundtruth/trimaps/100p_cube2_trimap_t_05.h5"
    # ilp_file = "/home/stamylew/ilastik_projects/500p_cube1.ilp"
    # files = "/home/stamylew/volumes/test_data/500p_cube2.h5"
    # gt = "/home/stamylew/volumes/groundtruth/trimaps/500p_cube2_trimap_t_05.h5"

    test(ilp_file, files, gt, 2000, 1, "", 1)

    print
    print "done"