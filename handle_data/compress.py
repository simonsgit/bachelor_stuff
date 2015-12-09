__author__ = 'stamylew'
from python_functions.handle_h5.handle_h5 import read_h5, save_h5

def compress(input, ouput):
    file = read_h5(input[0], input[1])
    save_h5(file, output[0], output[1], "lzf")
if __name__ == '__main__':
    input = ("/home/stamylew/volumes/training_data/smallcubes.h5", "50cube1_memb")
    output = ("/home/stamylew/volumes/groundtruth/memb/50cube1_memb.h5", "data")
    compress(input, output)