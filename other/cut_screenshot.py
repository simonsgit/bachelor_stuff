__author__ = 'stamylew'
# coding=utf-8

# import vigra
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

mypath = "/mnt/CLAWS1/stamilev/delme/srceenshots"

from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f[-4:]==".png" and f[-7:-4] != "cut"]


for f in onlyfiles:

    img=mpimg.imread(f)
    print f
    print img.shape

    img = np.array(img)
    img = img[216:1218, 656:1662]


    fig = plt.figure()
    fig.set_size_inches(1, 1)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    # plt.set_cmap('hot')
    ax.imshow(img, aspect = 'normal')
    plt.savefig(mypath+"/"+f[:-3]+"_cut.png", dpi=500)#, bbox_inches='tight')

    # plt.figure(frameon=False)
    # plt.imshow(img)
    # plt.savefig(mypath+"/"+f[:-3]+"_cut.png", bbox_inches='tight')
    # plt.show()

