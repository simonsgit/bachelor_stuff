__author__ = 'stamylew'

from subprocess import call
from python_functions.handle_data.random_labels import filter_all_labels, get_number_of_labels, limit_label
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



# def reduce_labels_in_ilp2(ilpfile, labels):
#     """
#     :param ilpfile:
#     :param labels:
#     :return:
#     """
#
#     #create copy project
#     ilp_copy = create_copy(ilpfile)
#
#     #work on copy file
#     manipulate_me = ILP(ilp_copy, "/home/stamylew/delme")
#     blocks, block_slices = manipulate_me.get_labels(0)
#
#     nolb = []
#
#     for block in blocks:
#         nolib = get_number_of_labels(block)
#         nolb.append(nolib)
#
#     noal = float(np.sum(nolb))
#
#     noal2= get_number_of_labels(blocks)
#     print
#     print "noal and noal2:", noal, noal2
#
#     new_all_blocks = limit_label(blocks,labels, noal)
#     manipulate_me.replace_labels(0, new_all_blocks, block_slices, delete_old_blocks=True)
#
#     return manipulate_me.project_filename

def reduce_labels_in_ilp(ilpfile, labels):
    """ Reduces amount of labeled pixels to given value for labels
    :param: ilpfile: path to ilastik project
    :param: labels : amount labeled pixels
    """

    #create copy project
    ilp_copy = create_copy(ilpfile)

    #work on copy file
    manipulate_me = ILP(ilp_copy, "/home/stamylew/delme")
    print
    print "amount of label blocks:", manipulate_me._label_block_count(0)
    blocks, block_slices = manipulate_me.get_labels(0) # 0 selects the first data set imported in the ilp
    #save_h5(blocks, "/home/stamylew/delme/blocks.h5", "data", None)

    #gather amount of labeled pixels
    nolb = []
    all_blocks = []
    for block in blocks:
        all_blocks.append(block)
        nolib = get_number_of_labels(block)
        nolb.append(nolib)
    noal = float(np.sum(nolb))

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
    # print "unique elements of new blocks:", np.unique(new_blocks)

    nonl = float(np.sum(nolnb))
    print
    print "reduced amount of labels:", nonl
    # assert labels == nonl

    manipulate_me.replace_labels(0, new_blocks, block_slices, delete_old_blocks=True)

    return manipulate_me.project_filename


# def modify_labels_of_ilp(ilp, labels):
#     modified_ilp = reduce_labels_in_ilp2(ilp,labels)
#     return modified_ilp

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
    print "reduced amount of labels", al


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
    random_slice = random_block[:,:,random_slice_no]
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


if __name__ == '__main__':
    trimap_path = "/home/stamylew/volumes/groundtruth/trimaps/500p_cube2_trimap_t_05.h5"
    #trimap_path = "/home/stamylew/volumes/groundtruth/trimaps/100p_cube1_trimap_t_05.h5"
    trimap_data = read_h5(trimap_path, "data")
    print "trimap labeled pixel amount", get_number_of_labels(trimap_data)
    ilp_path = "/home/stamylew/ilastik_projects/100p_cube1.ilp"
    #ilp_path = "/home/stamylew/ilastik_projects/100p_cube1.ilp"
    # mod_ilp = modify_labels_of_ilp(ilp_path, 3000)
    # check_ilp_labels(mod_ilp)
    concentrated_data = concentrated_labels(ilp_path, 1000)
    # save_h5(concentrated_data, "/home/stamylew/delme/concentrated_ilp_labels.h5", "data", None)
    print "done"