__author__ = 'stamylew'
import numpy as np
import skneuro.learning._learning as skl
from src.watershed.wsdt import wsDtSegmentation
from python_functions.handle_h5.handle_h5 import read_h5, save_h5
from python_functions.quality.quality import adjust_predict
from vigra import analysis, filters



def make_superpixels(prob_map, gt):
    prob_map = adjust_predict(prob_map)
    #save_h5(prob_map, "/home/stamylew/delme/prob_map.h5", "data", None)
    print "type", type(prob_map)
    print "shape", prob_map.shape
    segmentation = wsDtSegmentation(prob_map, 0.5, 0, 10, 2, 2, cleanCloseSeeds=True, returnSeedsOnly=False)

    # gtsegmentation = wsDtSegmentation(gt, 0.5, 0, 10, 2, 2, cleanCloseSeeds=True, returnSeedsOnly=True)
    # save_h5(gtsegmentation, "/home/stamylew/delme/gt_seg_seeds.h5", "data", None)

    print "number of segments:", len(np.unique(segmentation))

    return segmentation

def compare_segmentation(segmentation, gt, ignoreLabel= True):
    ri_data = skl.randIndex(segmentation.flatten().astype(np.uint32), gt.flatten().astype(np.uint32), ignoreLabel)
    voi_data = skl.variationOfInformation(segmentation.flatten().astype(np.uint32), gt.flatten().astype(np.uint32), ignoreLabel)
    return ri_data, voi_data

if __name__ == '__main__':
    prob_map = read_h5("/home/stamylew/test_folder/p_cache/100p_cube2_probs.h5")
    memb_map = read_h5("/home/stamylew/volumes/groundtruth/memb/100p_cube2_memb.h5")
    dense_gt = read_h5("/home/stamylew/volumes/groundtruth/dense_groundtruth/100p_cube2_dense_gt.h5")
    gt = read_h5("/home/stamylew/volumes/groundtruth/trimaps/100p_cube2_trimap_t_05.h5")
    seg = make_superpixels(prob_map, gt)
    print skl.__file__

    print compare_segmentation(seg,dense_gt, True)
    #save_h5(seg, "/home/stamylew/delme/segmentation.h5", "data", None)
