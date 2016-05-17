# -*- coding: utf-8 -*-
"""
Created on Tue May 17 10:41:10 2016

@author: ubuntumate
"""

class L3Bean:
    
    """
    self._gg = 0
    self._lat = 0
    self._lon = 0
    self._sicvalues = 0
    """
    def __init__(self):
      self._gg  = 0
      self._lat = 0
      self._lon = 0
        
      self._sicsum = 0
      self._sics = []
    
    def add(self, bean):
      self._gg  = bean.getGG() 
      self._lat = bean.getLat()
      self._lon = bean.getLon()
        
      self._sics.append(bean.getSic())
      self._sicsum = self._sicsum + bean.getSic()
        
    def getMedSic(self):
        return self._sicsum/len(self._sics)
        
    def getLat(self):
        return self._lat
        
    def getLon(self):
        return self._lon
        
    #def __eq__(self, other):
    #    return self._gg == other.getGG()
    
    
        
        
        
    
    

    """
    from L2Bean import L2Bean
    
    
    class L3BeanList(list):
        
    
                
    
        def addlist(self, l2beanlist):
            for l2b in l2beanlist:
                o = None            
                try
                    index = self.index(l2b)
                    o = self[index]
                    #Ya encontro con mismo gg_index
                except ValueError:
                    print "valor no encontrado: ", ValueError
                
                self.append(l2b)                    
            
        
        def getSics(self):
            pass
        
        def getLats(self):
            pass 
    
           
        def getLons(self):
            pass
    """