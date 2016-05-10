# -*- coding: utf-8 -*-
"""
Created on Tue May 10 15:49:10 2016

@author: ubuntumate
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

import numpy as np
import pylab as P

from mwr_tie_points_finder import print_tie_points

import h5py

            """        
            for f in filelist:
                s = l1b_file.split(".")
            
            
            tar = tarfile.open("./MWR_pasadas/"+l1b_file)
            tar.extractall(path="./tmp/",members=None)
            archivos = tar.getnames()
            
            tar.close()
            
            for n in archivos:
                if n.endswith(".h5"):
                    filename = n
            
            #print "./tmp/"+s[0]+filename
            return "./tmp/"+filename
            
            
            """

class HD5L2Files(list):

    def __init_(self, filelist):
        self.dic = {} 
        for filename in filelist:
                    reahcer
            f = h5py.File(filename, "r")
           
            self.dic['seaIceConcetration'] = f["MWR Geophysical Retrieval Data"]["sea_ice_concentration"]
            self.dic['sea_ice_concentration_gg'] =f["Geolocation	Data"]["sea_ice_concentration_gg"])
            
            self.dic['DP']          = f["Intermediate Data"]["DP"][:]) 
            self.dic['DG']          = f["Intermediate Data"]["DG"][:]) 
            self.dic['gg_index']    = f["Intermediate Data"]["gg_index"][:]) 
            self.dic['lat']         = f["Intermediate Data"]["lat"][:]) 
            self.dic['lon']         = f["Intermediate Data"]["lon"][:]) 
            self.dic['surface']     = f["Intermediate Data"]["surface"][:]) 
                        
            
            
            
            f.close()
        