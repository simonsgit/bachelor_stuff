__author__ = 'stamylew'

from subprocess import call
from python_functions.handle_data.random_labels import get_number_of_labels, limit_label
from python_functions.handle_h5.handle_h5 import read_h5
import numpy as np
from autocontext.core.ilp import ILP

def create_copy(ilp_path):
    """creates copy of the ilp file for modification
    :param ilp: path to ilp project
    :return: path to copy of ilp project
    """

    #copy file name
    ilp_copy = ilp_path.split(".")[-2] + "_copy.ilp"

    #use system copy functions
    call(["cp", ilp_path, ilp_copy])

    return ilp_copy

def reduce_labels_in_ilp(ilp_path, labels):
    """Reduces amount of labeled pixels in ilp project to a set value
    :param ilpfile: path to ilp project
    :param labels:  limit for how many labeled pixels should remain
    :return: path to ilp project with reduced labels
    """

    #create copy project
    ilp_copy = create_copy(ilp_path)

    #work on copy file
    manipulate_me = ILP(ilp_copy, "/home/stamylew/delme")

    #extract blocks and block coordinates from ilp file
    blocks, block_slices = manipulate_me.get_labels(0)

    #get number of labeled pixels in the indiviual blocks and appending them to a list
    nolb = []
    for block in blocks:
        nolib = get_number_of_labels(block)
        nolb.append(nolib)

    #sum amount of labeled pixels of the individual blocks
    noal = float(np.sum(nolb))

    #limit amount of labeled pixels to the given limit
    new_all_blocks = limit_label(blocks,labels, noal)

    #insert altered blocks back into ilp file
    manipulate_me.replace_labels(0, new_all_blocks, block_slices, delete_old_blocks=True)

    return manipulate_me.project_filename

def check_ilp_labels(ilp_path):
    """Checks amount of labeled pixels in ilp project
    :param ilp_path: path to ilp project
    :return: Amount of labeled pixels
    """

    ilp = ILP(ilp_path, "/home/stamylew/delme")

    #extract blocks and block coordinates from ilp file
    blocks, blockslices = ilp.get_labels(0)

    #get number of labeled pixels in the indiviual blocks and appending them to a list
    nolb = []
    for block in blocks:
        nolib = get_number_of_labels(block)
        nolb.append(nolib)

    #sum amount of labeled pixels of the individual blocks
    noal = float(np.sum(nolb))

    return noal


if __name__ == '__main__':
    
    trimap_path = "/home/stamylew/volumes/groundtruth/trimaps/500p_cube2_trimap_t_05.h5"

    trimap_data = read_h5(trimap_path, "data")

    print "trimap labeled pixel amount", get_number_of_labels(trimap_data)

    ilp_path = "/home/stamylew/ilastik_projects/500p_cube2_less_feats.ilp"

    mod_ilp = reduce_labels_in_ilp(ilp_path, 1000)

    print "Amount of labeled pixels:", check_ilp_labels(mod_ilp)
