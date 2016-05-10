# -*- coding: utf-8 -*-
"""
Created on Mon May  9 16:51:07 2016

@author: ubuntumate
"""
import numpy as np


class MultiBandBeanDict(dict):

    def getSurfaceAsMatrix(self):
        #Elemento mas largo  de todos los beams
        maxval = 0
        for i in range(0,8):
            mbbl = self["Bean"+str(i)]
            val = len(mbbl)
            if val>maxval:                        
                maxval = val
        result = -99*np.ones((maxval, 8))
        for i in range(0,8):
            mbbl = self["Bean"+str(i)]
            j=0
            for mbb in mbbl:
                result[j,i] = mbb.getGG()
                j = j + 1 
                
        return result
        
    def getGGAsMatrix(self):
        #Elemento mas largo  de todos los beams
        maxval = 0
        for i in range(0,8):
            mbbl = self["Bean"+str(i)]
            val = len(mbbl)
            if val>maxval:                        
                maxval = val
        result = -99*np.ones((maxval, 8))
        for i in range(0,8):
            mbbl = self["Bean"+str(i)]
            j=0
            for mbb in mbbl:
                result[j,i] = mbb.getGG()
                j = j + 1     
        
        return result
    
    def getLonAsMatrix(self):
        #Elemento mas largo  de todos los beams
        maxval = 0
        for i in range(0,8):
            mbbl = self["Bean"+str(i)]
            val = len(mbbl)
            if val>maxval:                        
                maxval = val
        result = -99*np.ones((maxval, 8))
        for i in range(0,8):
            mbbl = self["Bean"+str(i)]
            j=0
            for mbb in mbbl:
                result[j,i] = mbb.getLon()
                j = j + 1 
        return result
    
    def getLatAsMatrix(self):
        #Elemento mas largo  de todos los beams
        maxval = 0
        for i in range(0,8):
            mbbl = self["Bean"+str(i)]
            val = len(mbbl)
            if val>maxval:                        
                maxval = val
        result = -99*np.ones((maxval, 8))
        for i in range(0,8):
            mbbl = self["Bean"+str(i)]
            j=0
            for mbb in mbbl:
                result[j,i] = mbb.getLat()
                j = j + 1 
        return result
    
    
    def getAGAsMatrix(self):
        #Elemento mas largo  de todos los beams
        maxval = 0
        for i in range(0,8):
            mbbl = self["Bean"+str(i)]
            val = len(mbbl)
            if val>maxval:
                maxval = val
        result = -99*np.ones((maxval, 8))
        for i in range(0,8):
            mbbl = self["Bean"+str(i)]
            j=0
            for mbb in mbbl:
                result[j,i] = mbb.getAG()
                j = j + 1
        return result
    
    def getAPAsMatrix(self):
        #Elemento mas largo  de todos los beams
        maxval = 0
        for i in range(0,8):
            mbbl = self["Bean"+str(i)]
            val = len(mbbl)
            if val>maxval:
                maxval = val
        result = -99*np.ones((maxval, 8))
        for i in range(0,8):
            mbbl = self["Bean"+str(i)]
            j=0
            for mbb in mbbl:
                result[j,i] = mbb.getAP()
                j = j + 1      
        return result
