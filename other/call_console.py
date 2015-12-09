# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 13:06:01 2015

@author: stamylew
"""

from subprocess import call
import time

call(["ls"])
call(["ls", "-l"])
call(["df", "-h"])


# for n in range(1, 5):
#    print n
#    callthis = "python autocontext.py --train /home/stamylew/ilastik_projects/test_75cube_labeled.ilp -o /home/stamylew/ilastik_projects/test_75cube_labeled_trained.ilp --cache training/cache -n "+str(n)+" --ilastik /home/stamylew/software/ilastik-1.1.6-Linux/run_ilastik.sh"
#    print callthis
#
#
#
#
#    call([callthis])
#
#    call(["Y"])


print "done"
