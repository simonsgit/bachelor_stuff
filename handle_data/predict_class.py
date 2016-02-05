# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 17:18:52 2015

@author: stamylew
"""
from python_functions.quality.quality import apr, exclude_ignore_label, adjust_predict, roc_auc, draw_roc_curve
from python_functions.handle_data.random_labels import get_number_of_labels
from python_functions.handle_h5.handle_h5 import read_h5, save_h5
import matplotlib.pyplot as plt
import numpy as np



class predict_class:
    def __init__(self, gt, predict, threshold = 0.5):
        self.gt                 = gt
        self.adjusted_predict   = adjust_predict(predict)
        self.relevant_data      = exclude_ignore_label(gt, self.adjusted_predict)
        self.nlables            = get_number_of_labels(gt)
        self.apr                = apr(self.relevant_data[0], self.relevant_data[1])
        self.auc_score          = roc_auc(self.relevant_data[0], self.relevant_data[1])
        self.quality            = np.array((self.apr[0], self.apr[1], self.apr[2], self.auc_score))
        self.roc_curve          = draw_roc_curve(self.relevant_data[0], self.relevant_data[1])


    def show_images(self):
        plt.imshow(self.gt[0])
        plt.imshow(self.adjusted_predict[0])

class quality_values:
    def __init__(self, gt, predict):
        self.accuracy
        self.prevalence
        self.specifity
        self.sensitivity
        self.PPV
        self.NPV
        self.AUC

if __name__ == '__main__':
    #g = read_h5("/home/stamylew/volumes/trimaps/50cube3_tri.h5", "50cube3_tri")
    #p = read_h5("/home/stamylew/volumes/training_data/50cube3_bp", "n3")
    #p = adjust_predict_file(p)
    #p = exclude_ignore_label(g, p)
    #
    #q = read_h5("/home/stamylew/src/autocontext/training/cache_mw/0000_smallcubes_probs.h5", "exported_data")
    #save_h5(q, "/home/stamylew/volumes/training_data/50cube3_bp.h5", "all_labels/n3/w_1_2_3")
    #q = adjust_predict_file(q)
    #q = exclude_ignore_label(g, q)
    #
    #
    #
    #c = config(p[0], p[1])
    #c.show_quality()
    #
    #d = config(q[0], q[1])
    #d.show_quality()
    
    I = read_h5("/home/stamylew/volumes/trimaps/50cube2_tri.h5", "50cube2_tri")
    
    II = read_h5("/home/stamylew/src/autocontext/prediction/cache/smallcubes_probs.h5", "exported_data")
    II = adjust_predict(II)
    
    
    q = exclude_ignore_label(I,II)
    c = predict_class(q[0], q[1])
    c.show_quality()
    print c.return_quality()
    
    #III = read_h5("/home/stamylew/volumes/training_data/50cube3_bp.h5", "all_labels/n3/w_3_2_1")
    #III = adjust_predict_file(III)
    
    #plt.figure()
    #plt.imshow(I[11])
    #
    #plt.figure()
    #plt.imshow(II[11])
    #
    #plt.show()
    
    
    #for k in d.keys():
    #    k.showAllConfigs()
    #    print d[k]
    #    print
    
    
    print "done"