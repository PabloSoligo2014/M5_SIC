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

    def isNorth(self):
        return (self._lat>0)
        
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
        
     
        
    def getSic(self):
        numerador = (self.getDG()-self.getOpenWaterG()) - ((self.getDP()-self.getOpenWaterP()) * self.getAlpha())
        denominador = (self.getMultiYearIceG()-self.getOpenWaterG())-((self.getMultiYearIceP()-self.getOpenWaterP())*self.getAlpha())
         
        val = numerador/denominador
        if(val<0):
            return 0.0
        elif(val>1):
            return 1.0
        else:
            return val
            
        
    def getAlpha(self):
        return (self.getFirstYearIceG()-self.getMultiYearIceG())/(self.getFirstYearIceP()-self.getMultiYearIceP())
    
    def getOpenWaterG(self):
        if ((self._bean+1) % 2 == 0):
            #es par
            return 12.36
        else:
            return 13.87
    
    def getFirstYearIceG(self):
        if ((self._bean+1) % 2 == 0):
            #es par
            return -5.66
        else:
            return -4.40
    
    def getMultiYearIceG(self):
        if ((self._bean+1) % 2 == 0):
            #es par
            return -10.24
        else:
            return -11.20
            
    def getOpenWaterP(self):
        if ((self._bean+1) % 2 == 0):
            #es par
            return 62.73
        else:
            return 73.31
    
    def getFirstYearIceP(self):
        if ((self._bean+1) % 2 == 0):
            #es par
            return 27.35
        else:
            return 21.60
    
    def getMultiYearIceP(self):
        if ((self._bean+1) % 2 == 0):
            #es par
            return 25.04
        else:
            return 20.51
            

        
       
            
            