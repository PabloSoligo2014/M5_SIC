# -*- coding: utf-8 -*-
"""
Created on Mon May  9 16:48:13 2016

@author: ubuntumate
"""

class Bean:
    
    #No pueden ser privados?
    gg_index  = 0
    lat       = 0.0
    lon       = 0.0
    tbs       = 0.0
    band      = "No det"
    bean      = 0
    surface   = 0    
    """
    def __init__(self):
              
        self.gg_index  = 0
        self.lat       = 0.0
        self.lon       = 0.0
        self.tbs       = 0.0
        self.band      = "No det"
        self.bean      = 0
        self.surface   = 0
    """    
    def __init__(self, gg_index=0, lat=0.0, lon=0.0, tbs=0.0, band="No det", bean=0, surface=0):
        self.gg_index  = gg_index
        self.lat       = lat
        self.lon       = lon
        self.tbs       = tbs
        self.band      = band
        self.bean      = bean
        self.surface   = surface
        
    def getTbs(self):
        #MATIAS Como es que python no permite acceder a mas de un nivel de profundidad
        #Java, C#, Delphi, C++, VB permiten
        #print "getTbs: ", self.__tbs         
        return self.tbs
        
    def setTbs(self, value):
        #print "set tbs", value
    
        self.tbs = value    
        
    def addLat(self, value):
        self.lat = value
    def addLon(self, value):
        self.lon = value
            
    def getLat(self):
        return self.lat                
    
    def getLon(self):
        return self.lon
        
    def getBand(self):
        return self.band 
        
    def getSurface(self):
        return self.surface
        
    def getGG(self):
        return self.gg_index
        
    def __eq__(self, other):
        return self.gg_index == other.gg_index
        
    def __hash__(self):
        return 1
        
    def __cmp__(self,other):
        return cmp(self.getGG(),other.getGG())
