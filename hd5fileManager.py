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

class hd5fileManager():
    
    _filename = ""
    _measurelist = None
    _multiBandBeanDict = None
    
    
    def __init__(self, filename, measurelist, multiBandBeanDict):
        self._filename = filename
        self._measurelist = measurelist
        self._multiBandBeanDict = multiBandBeanDict 
        
    def getMeasureList(self):
        return self._measurelist
        
    def getMultiBandBeanList(self):
        return self._multiBandBeanDict
        
    def save(self):

        f = h5py.File(self._filename, "w")
        
        grp_geo_retrieval = f.create_group("MWR Geophysical Retrieval Data")
        grp_geo_retrieval.create_dataset("sea_ice_concentration",data=self._measurelist.getSicsAsArray())
        
        grp_geo_data= f.create_group("Geolocation	Data")
        grp_geo_data.create_dataset("sea_ice_concentration_gg",data=self._measurelist.getGGAsArray())
   
        grp_inter_data= f.create_group("Intermediate	Data")
        
   
        grp_inter_data.create_dataset("DP", data=self._multiBandBeanDict.getAPAsMatrix())
        grp_inter_data.create_dataset("DG", data=self._multiBandBeanDict.getAGAsMatrix())
        grp_inter_data.create_dataset("gg_index", data=self._multiBandBeanDict.getGGAsMatrix())
        grp_inter_data.create_dataset("lat", data=self._multiBandBeanDict.getLatAsMatrix())
        grp_inter_data.create_dataset("lon", data=self._multiBandBeanDict.getLonAsMatrix())
        grp_inter_data.create_dataset("surface", data=self._multiBandBeanDict.getSurfaceAsMatrix())
        
        
        #self._multiBandBeanDict.getAPAsMatrix()
        #, data=self._multiBandBeanDict.getAsMatrix() 
        
        
        #ds_k_h_geodedic_grid_index = grp_inter_data.create_dataset("k_h_geodedic_grid_index",data=index_gg)
       
        
            
        
        
        ##recorro el dicc dp,dg para guardarlo por beam        
        
        """
        
        grp_inter_data.create_dataset("k_h_surface_type",data=surface_type)
        grp_inter_data.create_dataset("k_h_antenna_temperature",data=array_k_h_tb)
        grp_inter_data.create_dataset("ka_h_geodedic_grid_index",data=index_gg)
        grp_inter_data.create_dataset("ka_h_antenna_temperature",data=array_ka_h_tb)
        grp_inter_data.create_dataset("ka_v_geodedic_grid_index",data=index_gg)
        grp_inter_data.create_dataset("ka_v_antenna_temperature",data=array_ka_v_tb)
        for b in range(0, 8):
            #obtengo el bandbeanlist para la banda
            bbl = self["Band"+str(b)]
            for x in bbl:
                x.getSic()        
        
        
        
            
        for beam in dp:   
            b=str(beam)
            deltas_g="delta_g_beam_"+b
            deltas_p="delta_p_beam_"+b
            grp_inter_data.create_dataset(deltas_g,data=dg[beam])
            grp_inter_data.create_dataset(deltas_p,data=dp[beam])
        """
        
        f.flush()
        f.close()
            
            
        
                
        """
            
        print "Tamano del bandbeanlist", len(bbl)
            
            
            
           
        
        #dataset = mfile.create_dataset("dset",(1, len(sics)), )
        
        #dataset = mfile.create_dataset("dset",data=npsics)
        
        
        #print "Dataset dataspace is", dataset.shape
        #print "Dataset Numpy datatype is", dataset.dtype
        #print "Dataset name is", dataset.name
        #print "Dataset is a member of the group", dataset.parent
        #print "Dataset was created in the file", dataset.file    
    
        #mfile.flush()
        #mfile.close()
        """
 