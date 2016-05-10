# -*- coding: utf-8 -*-
"""
Created on Tue May 10 11:07:38 2016

@author: ubuntumate
"""


from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

import numpy as np
import pylab as P

from mwr_tie_points_finder import print_tie_points

import h5py

class HD5FileList(list):
    
    def __init__(self):
        self._lats = []
        self._lons = []
        self._sics = []  
        
        self._AP   = []
        self._AG   = []
        
    
        
    def _draw(self, title, x, y, bins):
        plt.figure()
                   
        plt.hist2d(x, y, bins=500)
        plt.title(title)
        plt.show()
    
    def drawHistograms(self):
        """ Plots a 2d histogram
        """
        print "plotting histogram"

        ApEvenNorth = []
        ApOddNorth = []
        ApEvenSouth = []
        ApOddSouth = []        
        
        AgEvenSouth = []
        AgOddSouth = []  
        AgEvenNorth = []
        AgOddNorth = []  
        
        agNorth = []
        agSouth = []
        
        apNorth = []
        apSouth = []
        
        for h5 in self:
            mbbd = h5._multiBandBeanDict
            for i in range(0,8):
                bbl = mbbd["Bean"+str(i)]                
                
                for mbb in bbl:
                    #print "comparing", i, mbb.getCornet()
                    if((i+1) % 2 == 0):
                        
                        #es par--
                                            
                        if mbb.getLat()>0:
                            ApEvenNorth.append(mbb.getAP())
                            AgEvenNorth.append(mbb.getAG())
                            
                            apNorth.append(mbb.getAP())
                            agNorth.append(mbb.getAG())
                            
                        else:
                            ApEvenSouth.append(mbb.getAP())
                            AgEvenSouth.append(mbb.getAG())
                            
                            apSouth.append(mbb.getAP())
                            agSouth.append(mbb.getAG())
                            
                            
                    else:
                             
                        
                        if mbb.getLat()>0:
                            ApOddNorth.append(mbb.getAP())
                            AgOddNorth.append(mbb.getAG())
                            
                            apNorth.append(mbb.getAP())
                            agNorth.append(mbb.getAG())
                        else:
                            ApOddSouth.append(mbb.getAP())
                            AgOddSouth.append(mbb.getAG())
                            
                            apSouth.append(mbb.getAP())
                            agSouth.append(mbb.getAG())
                    
                    
       
            #iceCount, IceP, iceG, seaCount, SeaP, seaG = print_tie_points(agSouth, apSouth)
            #iceCount, IceP, iceG, seaCount, SeaP, seaG = print_tie_points(agNorth, apNorth)
            
        
        #self._draw("Points North", IceP, iceG, 500)
        #self._draw("Histrograma sur/par", ApEvenSouth, AgEvenSouth, 500)
        #self._draw("Histrograma norte/impar", ApOddNorth, AgOddNorth, 500)
        #self._draw("Histrograma sur/impar", ApOddSouth, AgOddSouth, 500)
        #self._draw("Histrograma norte/par", ApEvenNorth, AgEvenNorth, 500)
        
        
        
        
        
        
        """
        ICE. counts = 29.0 p = 37.2 g = -28.8
        ICE. counts = 25.0 p = 35.6 g = -28.8
        ICE. counts = 19.0 p = 37.2 g = -30.4
        SEA. counts = 15.0 p = 67.6 g = 38.4
        SEA. counts = 6.0 p = 66.0 g = 36.8
        SEA. counts = 5.0 p = 66.0 g = 38.4
        """
        
        
    
    def getLatAsNp(self):
        return np.array(self._lats)
        
        
    def getLonAsNp(self):
        return np.array(self._lons)
    
    def getSicAsNp(self):
        return np.array(self._sics)
    
    def _fillvalues(self):
        for h5 in self:
            for me in h5.getMeasureList():
                self._lats.append(me.getLat())
                self._lons.append(me.getLon())
                self._sics.append(me.getSic())
        
    
    def drawNPole(self):
        m = Basemap(projection='npstere',boundinglat=50,lon_0=270,resolution='h', round=True)    
    
        if (len(self._lats)==0):
            self._fillvalues()
            
            
        lng = self.getLonAsNp()
        lat = self.getLatAsNp() 
        sic = self.getSicAsNp()
        
        plt.figure()
           
        x1,y1= m(lng, lat)
           
        m.hexbin(x1,y1, C=sic, gridsize=len(sic), cmap=plt.cm.jet)
        
        m.drawcoastlines()
        m.drawcountries()
        m.fillcontinents(color='coral')
        m.drawmapboundary()
        
           
        
        # draw parallels and meridians.
        #m.drawparallels(np.arange(-80.,81.,20.))
        #m.drawmeridians(np.arange(-180.,181.,20.))
        #m.drawmapboundary(fill_color='white')
    
    
        #m.colorbar(location="right",label="SIC") # draw colorbar
        plt.title("Final")
        #fig = plt.gcf()
        plt.show()
        
       
        plt.close()
         
        # Delete auxiliar variables.
        del m
        del lng    
        del lat    
        del sic    
        del x1
        del y1

    