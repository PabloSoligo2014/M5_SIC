# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 10:10:14 2016

@author: ubuntumate
"""

from mwr_l2_processor import passfile, processPassFile
import os
import sys
import numpy as np

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

if __name__ == "__main__":
    
    m = Basemap(projection='spstere',boundinglat=-50,lon_0=180,resolution='h', round=True)
    
    #m = Basemap(projection='mill',lon_0=0)
    lat = []
    lng = []
    sic = []
            
    for fs in os.listdir(sys.argv[1]):        
        if fs.endswith("tar.gz") and fs.startswith("EO"):
            
            print "procesando... ", fs
    
            pf = passfile(fs)
            ml = processPassFile(pf)
            for mi in ml:
                #print mi.getLat(), mi.getLon(), mi.getSic()
                lng.append(mi.getLon())
                lat.append(mi.getLat())
                sic.append(mi.getSic())
            
    
    
    lng = np.array(lng)
    lat = np.array(lat)
    sic = np.array(sic)
    
    x1,y1= m(lng, lat)
    
    print "imprimiendo----"    
    plt.figure()        
    
    print "tamano x,y, sics", len(x1), len(y1), len(sic)
    
    #print lng, lat, x1[0:10000], y1[0:10000], sic[0:10000] 
    #
    m.hexbin(x1, y1, C=sic, gridsize=len(sic)/3, cmap=plt.cm.jet)
    
   
    m.drawcoastlines()
    #m.fillcontinents(lake_color='white')
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,20.))
    m.drawmeridians(np.arange(-180.,181.,20.))
    #m.drawmapboundary(fill_color='white')


    m.colorbar(location="right",label="SIC") # draw colorbar
    plt.title("Sea Ice Concentration - South Pole")
    fig = plt.gcf()
    plt.show()
    #f_name = "./img/"+filename + "_.png"
    #fig.savefig(f_name)
    plt.close()
    print "FIN"    
    # Delete auxiliar variables.
    del m
    del lng    
    del lat    
    del sic    
    del x1
    del y1
              
            
                        
            
    
    print "finaliza proceso...", fs
    print "finalizado completo..."

