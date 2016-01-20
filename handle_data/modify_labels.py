__author__ = 'stamylew'

from subprocess import call
from python_functions.handle_data.random_labels import filter_all_labels, get_number_of_labels
from python_functions.handle_h5.handle_h5 import read_h5, save_h5
import numpy as np
from autocontext.core.ilp import ILP
import socket

def create_copy(ilp):
    """creates copy of the ilp file for modification
    """

    #copy file name
    ilp_copy = ilp.split(".")[-2] + "_copy.ilp"

    #use system copy functions
    call(["cp", ilp, ilp_copy])

    return ilp_copy


def reduce_labels_in_ilp(ilpfile, labels):
    """ Reduces amount of labeled pixels to given value for labels
    :param: ilpfile: path to ilastik project
    :param: labels : amount labeled pixels
    """

    #create copy project
    ilp_copy = create_copy(ilpfile)

    #work on copy file
    manipulate_me = ILP(ilp_copy, "/home/stamylew/delme")
    blocks, block_slices = manipulate_me.get_labels(0) # 0 selects the first data set imported in the ilp
    #save_h5(blocks, "/home/stamylew/delme/blocks.h5", "data", None)
    #gather amount of labeled pixels
    nolb = []
    for block in blocks:
        nolib = get_number_of_labels(block)
        nolb.append(nolib)
    print
    print "amount of label blocks:", len(blocks)
    noal = float(np.sum(nolb))
    #noal = noal.astype(np.float64)
    print
    print "amount of all labels:", noal
    labels = float(labels)

    #limit amount of labeled pixels
    assert labels < noal
    percentage = labels/noal
    print
    print "percentage of labels:", percentage
    new_blocks = []
    for block in blocks:
        new_block = filter_all_labels(block, percentage)
        new_blocks.append(new_block)
    #save_h5(new_blocks, "/home/stamylew/delme/new_blocks.h5", "data", None)

    #check new blocks
    nolnb = []
    for block in new_blocks:
        nolinb = get_number_of_labels(block)
        nolnb.append(nolinb)
#    print "unique elements of new blocks:", np.unique(new_blocks)

    nonl = float(np.sum(nolnb))
    print
    print "reduced amount of labels:", nonl
#    assert labels == nonl

    manipulate_me.replace_labels(0, new_blocks, block_slices, delete_old_blocks=True)

    return manipulate_me.project_filename


def modify_labels_of_ilp(ilp, labels):
    ilp_copy = create_copy(ilp)
    modified_ilp = reduce_labels_in_ilp(ilp_copy,labels)
    return modified_ilp

def check_ilp_labels(ilp_path):
    ilp = ILP(ilp_path, "/home/stamylew/delme")
    blocks, blockslices = ilp.get_labels(0)
    list = []
    for block in blocks:
        noilb = get_number_of_labels(block)
        list.append(noilb)
    al = list[0]
    for i in range(1, len(list)):
        al += list[i]
    print al

if __name__ == '__main__':
    trimap_path = "/home/stamylew/volumes/groundtruth/trimaps/500p_cube1_trimap_t_05.h5"
    #trimap_path = "/home/stamylew/volumes/groundtruth/trimaps/100p_cube1_trimap_t_05.h5"
    trimap_data = read_h5(trimap_path, "data")
    print "trimap labeled pixel amount", get_number_of_labels(trimap_data)
    ilp_path = "/home/stamylew/ilastik_projects/500p_cube1_hand_drawn.ilp"
    #ilp_path = "/home/stamylew/ilastik_projects/100p_cube1.ilp"
    mod_ilp = modify_labels_of_ilp(ilp_path, 1000)
    check_ilp_labels(mod_ilp)

