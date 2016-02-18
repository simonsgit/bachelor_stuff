__author__ = 'stamylew'

import argparse
import subprocess
import os
import sys
import glob
import shutil
from autocontext import train, batch_predict
import colorama as col
from python_functions.handle_data.modify_labels import reduce_labels_in_ilp

def test(ilastik_path, ilp_path, runs, labels, weights, repeats):

    reduce_labels_in_ilp(ilp_path, labels)

    for i in range(repeats):
        print col.Fore.GREEN + "- Running repeat %d of %d -" % (i+1, repeats) + col.Fore.RESET
        train(ilastik_path, ilp_path, runs, -1, weights,)
        # autocontext.batch_predict()

def process_command_line():
    """ Parse command line arguments
    """

    # Add the command lien arguments
    parser = argparse.ArgumentParser(description="test autocontext", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Arguments
    parser.add_argument("--ilastik", type=str, required=True,
                        help="path to the file run_ilastik.sh")

    parser.add_argument("--train", type=str,
                        help="path to the ilastik project that will be used for training")

    parser.add_argument("--batch_predict", type=str,
                        help="path of the cache folder of a previously trained autocontext that will be used for batch "
                             "prediction")
def main():
    """
    """

    # Read command line arguments.
    args = process_command_line

if __name__ == '__main__':
    print ac.__file__
    test("/home/stamylew/software/ilastik-1.1.6-Linux/run_ilastik.sh", "/home/stamylew/ilastik_projects/100p_cube1.ilp",
         3, 10000,None,2)