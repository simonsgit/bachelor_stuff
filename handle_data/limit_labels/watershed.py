__author__ = 'stamylew'
import numpy as np
from src.watershed.wsdt import wsDtSegmentation
from python_functions.handle_h5.handle_h5 import read_h5, save_h5
from python_functions.handle_data.dclass import predict_class

def make_superpixels(prob_map, gt):
    prob_map = predict_class(gt, prob_map)
    prob_map = prob_map.adjusted_predict
    save_h5(prob_map, "/home/stamylew/delme/prob_map.h5", "data", None)
    segmentation = wsDtSegmentation(prob_map, 0.5, 0, 10, 2, 2, cleanCloseSeeds=True, returnSeedsOnly=False)
    print "number of segments:", len(np.unique(segmentation))
    return segmentation

if __name__ == '__main__':
    prob_map = read_h5("/home/stamylew/test_folder/p_cache/100p_cube2_probs.h5")
    memb_map = read_h5("/home/stamylew/volumes/groundtruth/memb/100p_cube2_memb.h5")
    gt = read_h5("/home/stamylew/volumes/groundtruth/trimaps/100p_cube2_trimap_t_05.h5")
    seg = make_superpixels(prob_map, gt)

    save_h5(seg, "/home/stamylew/delme/segmentation.h5", "data", None)