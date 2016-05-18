# -*- coding: utf-8 -*-
"""
Created on Mon May  9 16:52:30 2016

@author: ubuntumate
"""


"""
    Clase para administrar el guardado, 
    Idealmente las mismas listas podrian tener un save to file, 
    pero finalmente los datos agrupados quedaron en listas distintas
    a los datos por beans, por tanto se necesito una clase que 
    concentre todo
"""
    
import h5py
import tarfile
import os



import matplotlib.pyplot as plt

class hd5fileManager():
    
    #private ¡Como hago private?
    _filename = ""
    _measurelist = None
    _multiBandBeanDict = None
    _folder = ""
    
    
    def __init__(self, folder, filename, measurelist, multiBandBeanDict):
        self._filename = filename
        self._measurelist = measurelist
        self._multiBandBeanDict = multiBandBeanDict 
        self._folder = folder
        
    def getMeasureList(self):
        return self._measurelist
        
    def getMultiBandBeanList(self):
        return self._multiBandBeanDict
        
        
            
        
        
    def save(self, deletefiles=True):

        f = h5py.File(self._folder+self._filename, "w")
        
        grp_geo_retrieval = f.create_group("MWR Geophysical Retrieval Data")
        grp_geo_retrieval.create_dataset("sea_ice_concentration",data=self._measurelist.getSicsAsArray())
        
        grp_geo_data= f.create_group("Geolocation	Data")
        grp_geo_data.create_dataset("sea_ice_concentration_gg",data=self._measurelist.getGGAsArray())
   
        grp_inter_data= f.create_group("Intermediate Data")
        
   
        grp_inter_data.create_dataset("DP", data=self._multiBandBeanDict.getAPAsMatrix())
        grp_inter_data.create_dataset("DG", data=self._multiBandBeanDict.getAGAsMatrix())
        grp_inter_data.create_dataset("gg_index", data=self._multiBandBeanDict.getGGAsMatrix())
        grp_inter_data.create_dataset("lat", data=self._multiBandBeanDict.getLatAsMatrix())
        grp_inter_data.create_dataset("lon", data=self._multiBandBeanDict.getLonAsMatrix())
        grp_inter_data.create_dataset("surface", data=self._multiBandBeanDict.getSurfaceAsMatrix())
        
           
        f.flush()
        f.close()
        
        
        imgfilenamenorth = self._measurelist.saveImageHkNPole(self._folder, self._filename)
        imgfilenamesouth = self._measurelist.saveImageHkSPole(self._folder, self._filename)
        
        #print "archivos tar", self._folder+self._filename, self._folder+imgfilename 
        tar = tarfile.open(self._folder+self._filename+".tar.gz", "w:gz")
        
        #print "arcnames", imgfilename, self._filename
        
        if imgfilenamenorth!=None:
            tar.add(self._folder+imgfilenamenorth, arcname=imgfilenamenorth)  
            
        if imgfilenamesouth!=None:
            tar.add(self._folder+imgfilenamesouth, arcname=imgfilenamesouth)  
            
            
            
        tar.add(self._folder+self._filename, arcname=self._filename)    
        tar.close()
        
        if deletefiles==True:
            os.remove(self._folder+self._filename)
            os.remove(self._folder+imgfilenamenorth)
            os.remove(self._folder+imgfilenamesouth)    
        