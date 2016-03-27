__author__ = 'stamylew'

from subprocess import call
from python_functions.handle_data.random_labels import get_number_of_labels, get_number_of_unique_labels,  limit_label
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
    print "noal", noal
    #limit amount of labeled pixels to the given limit
    new_all_blocks = limit_label(blocks,labels, noal)

    #insert altered blocks back into ilp file
    manipulate_me.replace_labels(0, new_all_blocks, block_slices, delete_old_blocks=True)

    return manipulate_me.project_filename

def concentrated_labels(ilp_path, labels):
    labels = float(labels)
    #create copy project
    ilp_copy_path = create_copy(ilp_path)

    #work on copy file
    manipulate_me = ILP(ilp_copy_path, "/home/stamylew/delme")
    print
    print "amount of label blocks:", manipulate_me._label_block_count(0)
    blocks, block_slices = manipulate_me.get_labels(0) # 0 selects the first data set imported in the ilp
    random_block_no = np.random.randint(0, len(blocks))
    print
    print "random_block_no", random_block_no
    random_block = blocks[random_block_no]
    print
    print "random block shape", random_block.shape
    random_slice_no = np.random.randint(0,random_block.shape[2])
    smaller_slice_no = random_slice_no
    bigger_slice_no = random_slice_no+1
    print
    print "random_slice_no", random_slice_no
    random_slice = random_block[:,:,random_slice_no:random_slice_no+1]
    print "random slice", random_slice.shape
    label_number = float(get_number_of_labels(random_slice))

    while label_number < labels:

        if bigger_slice_no < random_block.shape[0]-1:
            bigger_slice_no = bigger_slice_no +1
        else:
            smaller_slice_no = smaller_slice_no-2

        random_slice = random_block[:,:,smaller_slice_no:bigger_slice_no]
        print "random slice", random_slice.shape
        label_number = get_number_of_labels(random_slice)
        print "label number", label_number
        if label_number > labels:
            break
    concentrated_data = limit_label(random_slice, labels, label_number)
    new_label_number = get_number_of_labels(concentrated_data)
    print "new_label number", new_label_number

    #create new blocks
    new_blocks = []
    for block in blocks:
        new_block = np.zeros(block.shape, dtype=np.uint)
        new_blocks.append(new_block)

    # replace random block with labeled data
    new_labeled_block = new_blocks[random_block_no]
    new_labeled_block[:,:,smaller_slice_no:bigger_slice_no] = concentrated_data
    assert get_number_of_labels(new_labeled_block) == labels

    # replace old blocks with new blocks
    manipulate_me.replace_labels(0, new_blocks, block_slices, delete_old_blocks=True)
    print
    print "new_label_number", get_number_of_labels(new_block)
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
    
    # trimap_path = "/home/stamylew/volumes/groundtruth/trimaps/500p_cube2_trimap_t_05.h5"
    #
    # trimap_data = read_h5(trimap_path, "data")
    #
    # print "trimap labeled pixel amount", get_number_of_labels(trimap_data)
    # ilp_path = "/home/stamylew/ilastik_projects/500p_cube2_less_feats.ilp"
    # mod_ilp = reduce_labels_in_ilp(ilp_path, 1000)
    # print "Amount of labeled pixels:", check_ilp_labels(mod_ilp)
    ilp = "/mnt/CLAWS1/stamilev/ilastik_projects/100p_cubes/100p_cube1_clever_labeling.ilp"
    # ilp_copy = create_copy(ilp)
    manipulate_me = ILP(ilp, "/home/stamylew/delme")

    #extract blocks and block coordinates from ilp file
    blocks, block_slices = manipulate_me.get_labels(0)

    #get number of labeled pixels in the indiviual blocks and appending them to a list
    nol = []
    # noil = []
    for block in blocks:
        nolib = get_number_of_labels(block)
        nol.append(nolib)
        # noilib = get_number_of_unique_labels(block)
        # noil.append(noilib)
    noal = float(np.sum(nol))
    # noail = float(np.sum(noil))
    print "noal", noal
    # print "noail", noail

