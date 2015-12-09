# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 18:38:02 2015

@author: stamylew
"""

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
        
print "__name__ is:", __name__
        
    
if __name__ == '__main__':
    print factorial
