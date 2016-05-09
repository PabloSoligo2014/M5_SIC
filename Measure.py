# -*- coding: utf-8 -*-
"""
Created on Mon May  9 16:49:57 2016

@author: ubuntumate
"""

#Esta clase agrupa todos los beans en uno solo sic
class Measure:
    lat=0.0
    lon=0.0
    gg = 0  
    meds = 0
    sics = 0
    
    def __init__(self, lat, lon, gg, sic):
        self.lat = lat
        self.lon = lon
        self.gg = gg
        self.sics = sic
        self.meds = 1       
    def getLat(self):
        return self.lat/self.meds
    def getLon(self):
        return self.lon/self.meds
    def getGG(self):
        return self.gg
    def getSic(self):
        return self.sics/(self.meds)
    def addValue(self, mbBean):
        print "Sic agregado->",  mbBean.getSic()  
        self.sics = self.sics + mbBean.getSic() 
        self.lat = self.lat + mbBean.getLat() 
        self.lon = self.lon + mbBean.getLon()
        self.meds = self.meds + 1
    def __eq__(self, other):
        return type(self) == type(other) and self.getGG() == other.getGG()
    def __hash__(self):
        return 1