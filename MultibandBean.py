# -*- coding: utf-8 -*-
"""
Created on Mon May  9 16:49:09 2016

@author: ubuntumate
"""

class MultibandBean:
    k_h_bean    = None
    ka_h_bean   = None
    ka_v_bean   = None
    cornet      = 0
    gg          = 0
    
    def __init__(self, Ak_h_bean, Aka_h_bean, Aka_v_bean, cornet, gg):
        self.k_h_bean     = Ak_h_bean
        self.ka_h_bean    = Aka_h_bean
        self.ka_v_bean    = Aka_v_bean
        self.cornet       = cornet
        self.gg           = gg
        
        #MATIAS: Porque no puedo hacer un len de un atributo?"
        #Cualquier lenguaje permitiria hacerlo
        #len(self.k_h_bean)

    def getGG(self):
        return self.gg

    def getK_h_bean(self):
        return self.k_h_bean
    def getKa_h_bean(self):
        return self.ka_h_bean
    def getKa_v_bean(self):
        return self.k_v_bean
        
        
    def getLat(self):
        return (self.k_h_bean.getLat()+self.ka_h_bean.getLat()+self.ka_v_bean.getLat())/3
    
    def getLon(self):
        return (self.k_h_bean.getLon()+self.ka_h_bean.getLon()+self.ka_v_bean.getLon())/3
        
    def getAP(self):
        #print "ka_v/ka_h tbs: ", self.ka_v_bean.getTbs(), self.ka_h_bean.getTbs() 
        
        return (self.ka_v_bean.getTbs()) - (self.ka_h_bean.getTbs())
    
    def getAG(self):
        #print "ka_h/k_h tbs: ", self.ka_h_bean.getTbs(), self.k_h_bean.getTbs() 
        return (self.ka_h_bean.getTbs()) - (self.k_h_bean.getTbs())
        
    def getSic(self):
        
        #print "Cornet->", self.cornet        
        #print "numerador", self.getAG(),self.getOpenWaterG(),self.getAP(),self.getOpenWaterP(),self.getAlpha()
        #print "denominador", self.getMultiYearIceG(),self.getOpenWaterG(),self.getMultiYearIceP(),self.getOpenWaterP(),self.getAlpha()
        
        numerador = (self.getAG()-self.getOpenWaterG()) - ((self.getAP()-self.getOpenWaterP()) * self.getAlpha())
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
        if (self.cornet+1 % 2 == 0):
            #es par
            return 12.36
        else:
            return 13.87
    
    def getFirstYearIceG(self):
        if (self.cornet+1 % 2 == 0):
            #es par
            return -5.66
        else:
            return -4.40
    
    def getMultiYearIceG(self):
        if (self.cornet+1 % 2 == 0):
            #es par
            return -10.24
        else:
            return -11.20
            
    def getOpenWaterP(self):
        if (self.cornet+1 % 2 == 0):
            #es par
            return 62.73
        else:
            return 73.31
    
    def getFirstYearIceP(self):
        if (self.cornet+1 % 2 == 0):
            #es par
            return 27.35
        else:
            return 21.60
    
    def getMultiYearIceP(self):
        if (self.cornet+1 % 2 == 0):
            #es par
            return 25.04
        else:
            return 20.51
            
    def getCornet(self):
        return self.cornet
        
