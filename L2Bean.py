# -*- coding: utf-8 -*-
"""
Created on Wed May 11 16:56:18 2016

@author: ubuntumate
"""

class L2Bean:
    
    
    #datadic["gg_index"][i][j], datadic["lat"][i][j], datadic["lon"][i][j], 0, 0, j, datadic["surface"][i][j]
    def __init__(self, gg, lat, lon, bean, surface, DP, DG):
        self._gg = gg
        self._lat = lat
        self._lon = lon
       
        self._bean = bean
        self._surface = surface
        self._DP = DP
        self._DG = DG

    
    def getGG(self):
        return self._gg
        
    def getLat(self):
        return self._lat
        
    def getLon(self):
        return self._lon
    
    def getBean(self):
        return self._bean
        
    def getSurface(self):
        return self._surface

    def getDP(self):
        return self._DP
        
        
    def getDG(self):
        return self._DG