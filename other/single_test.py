# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 15:21:51 2015

@author: stamylew
"""

from subprocess import call
from python_functions.handle_data.new_modify_labels import reduce_labels_in_ilp
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
        print "reducing labels to " + str(labels)
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
        t_cache = test_folder_path + "/t_cache"

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
    if "hand_drawn" in ilp:
        filename += "_hand_drawn"
    if "less_feat" in ilp:
        filename += "_less_feat"
    file_dir = output + "/" + filename
    file_dir = "/home/stamylew/delme"

    if not os.path.exists(file_dir):
        print
        print "Output folder did not exist."
        os.mkdir(file_dir)
        print
        print "New one named " + file_dir+ " was created."

    q_outpath = file_dir + "/n_" + str(loops) + "_l_" + str(label_tag) + "_w_" + weight_tag
    q_data_outpath = q_outpath + "/n_" + str(loops) + "_l_" + str(labels) + "_w_" + weight_tag + ".h5"
    #q_data_outpath = "/home/stamylew/delme/test.h5"
    if not os.path.exists(q_outpath):
        print
        print "Output h5 file did not exist"
        os.mkdir(q_outpath)
        print
        print "New one named " + q_outpath + " was created."
        qdata = np.zeros((repeats, 4), dtype= np.float)
    else:
        print
        print "Output h5 existed. Extra rows will be created."
        old_qdata = read_h5(q_data_outpath, "a_p_r_auc")
        qdata = np.zeros((repeats +  old_qdata.shape[0], 4), dtype= np.float)
        qdata[repeats::] = old_qdata

    # #create outpath
    # q_data_outpath = q_outpath + "/n_" + str(loops) + "_l_" + str(labels) + "_w_" + str(weights) + ".h5"
    # save_h5([labels],q_data_outpath, "labels")
    # save_h5([loops], q_data_outpath, "loops")

    for i in range(repeats):
        print
        print "round of repeats:", i+1
        #train ilp file
        ac_train(ilp, labels, loops, weights, t_cache, outpath)
        print
        print "training completed"

        #batch predict files
        ac_batch_predict(files, t_cache, p_cache, overwrite = "")
        print
        print "batch prediction completed"

        #archive data
        archive_qdata(p_cache + "/", gt, qdata, i, q_data_outpath, (0, 24, 49))
        print
        print "quality computed"

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
    gt = volumes_folder + "groundtruth/trimaps/100p_cube2_trimap_t_09.h5"
    # ilp_file = "/home/stamylew/ilastik_projects/500p_cube1.ilp"
    # files = "/home/stamylew/volumes/test_data/500p_cube2.h5"
    # gt = "/home/stamylew/volumes/groundtruth/trimaps/500p_cube2_trimap_t_05.h5"


    #
    test(ilp_file, files, gt, 1000, 1, "", 10)

    print
    print "done"