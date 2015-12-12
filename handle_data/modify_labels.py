__author__ = 'stamylew'

from subprocess import call
from python_functions.handle_data.random_labels import filter_all_labels, get_number_of_labels
from python_functions.handle_h5.handle_h5 import save_h5
import numpy as np

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

    #import ILP class from autocontext core
    from autocontext.core.ilp import ILP

    #create copy project
    ilp_copy = create_copy(ilpfile)

    #work on copy file
    manipulate_me = ILP(ilp_copy, "/home/stamyalew/delme")
    blocks, block_slices = manipulate_me.get_labels(0) # 0 selects the first data set imported in the ilp
    #save_h5(blocks, "/home/stamylew/delme/blocks.h5", "data", None)
    #gather amount of labeled pixels
    nolb = []
    for block in blocks:
        nolib = get_number_of_labels(block)
        nolb.append(nolib)
    print
    print "number of blocks:", len(blocks)
    noal = float(np.sum(nolb))
    #noal = noal.astype(np.float64)
    print
    print "number of all labels:", noal
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
    print
    #print "unique elements of new blocks:", np.unique(new_blocks)

    nonl = float(np.sum(nolnb))
    print
    print "number of new labels:", nonl

    manipulate_me.replace_labels(0, new_blocks, block_slices, delete_old_blocks=True)

    return manipulate_me.project_filename


def modify_labels_of_ilp(ilp, labels):
    ilp_copy = create_copy(ilp)
    modified_ilp = reduce_labels_in_ilp(ilp_copy,labels)
    return modified_ilp