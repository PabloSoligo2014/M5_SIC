# -*- coding: utf-8 -*-
"""
Created on Mon May  9 16:50:26 2016

@author: ubuntumate
"""

class BandBeanList(list):
    
    _band = -1
    def __init__(self, band, *args):
        list.__init__(self, *args)
        self._band = band
    
    def getBand(self):
        return self._band
        
    def add(self, obj):
        
        if(obj.getCornet()!=self.getBand()):
            raise Exception('Error al asignar elemento a lista de banda distinta')
        else:
            super(BandBeanList, self).append(obj)
    
    def getSicAsList(self):
        result = []
        for s in self:
            result.append(self.getSic())
        return result

    def getGGAsArray(self):
        result = []
        for s in self:
            result.append(self.getSic())
        return result
        
    def getSurfaceAsArray(self):
        result = []
        for s in self:
            result.append(self.getSurface())
        return result
        
    def getBandAsArray(self):
        result = []
        for s in self:
            result.append(self.getBand())
        return result
        
    def getTbsAsArray(self):
        result = []
        for s in self:
            result.append(self.getTbs())
        return result
