# -*- coding: utf-8 -*-
"""
Created on Mon May  9 16:53:24 2016

@author: ubuntumate
"""

from Measure import Measure

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

#junta, agrupa por beans para la grafica final
class MeasureList(list):
    
    def __init__(self, *args):
        list.__init__(self, *args)
        
    
    def unique_add(self, obj):
        #si ya existe promedio y agrupo
        finded = False
        for o in self:
            if (o.getGG()==obj.getGG()):
                #ya existe un elemento del mismo cornet para el mismo gg
                o.addValue(obj) 
                
                #print "Encontrado->", o.getGG(), obj.getGG(), o.getLat(), obj.getLat(), o.getLon(), obj.getLonx()
                finded = True
                break;
        
        if not finded:
            o = Measure(obj.getLat(), obj.getLon(), obj.getGG(), obj.getSic())
            self.append(o)
            
    #Agrega todo sin filtrar, solo para propositos de test
    def normal_add(self, obj):
        #si ya existe promedio y agrupo
        #print "Mi SIC->", obj.getSic()
        o = Measure(obj.getLat(), obj.getLon(), obj.getGG(), obj.getSic())
        self.append(o)
        
        
    def getSicsAsArray(self):
        
        result = []        
        for o in self:
            
            result.append(o.getSic())
        
        return result
        
    def getGGAsArray(self):
        
        result = []        
        for o in self:
            result.append(o.getGG())
        
        return result
            
            
    def drawNPole(self):
        #No es muy ortodoxo dibujar dentro de la clase
        my_map = Basemap(projection='npstere',boundinglat=50,lon_0=270,resolution='h', round=True)    
        my_map.drawcoastlines()
        my_map.drawcountries()
        my_map.fillcontinents(color='coral')
        my_map.drawmapboundary()
    
        #print "tamano:", len(self)
        for measure in self:
            x,y = my_map(measure.getLon(), measure.getLat())
            print  measure.getLat(), measure.getLon(), measure.getSic()
            color = 'go'    
            #print "color->", measure.getSic()        
            if measure.getSic()>0 and measure.getSic()<=0.2:
                color = 'go'    
            elif measure.getSic()>0.2 and measure.getSic()<=0.5:
                color = 'yo'    
            else:
                color = 'ro'    
    
            
            my_map.plot(y, x, color, markersize=12)

        my_map.drawmeridians(np.arange(0, 360, 30))
        my_map.drawparallels(np.arange(-90, 90, 30))
        #m.hexbin(x1,y1, C=sic[beam],gridsize=len(sic[beam]),cmap=plt.cm.jet)
    
    
        plt.gcf().set_size_inches(18,10)
        plt.show()    
        
    def drawHk(self, filename="nodet"):
   
       #    print sic
       # setup south polar stereographic basemap.
       if (len(self)!=0):
            m = Basemap(projection='spstere',boundinglat=-50,lon_0=180,resolution='h', round=True)
        
        
            lat = []
            lng = []
            sic = []
            
            for s in self:
                lng.append(s.getLon())
                lat.append(s.getLat())
                sic.append(s.getSic())
            
        
            lng = np.array(lng)
            lat = np.array(lat)
            sic = np.array(sic)
            plt.figure()
       
            x1,y1= m(lng, lat)
       
            print "x, y, sic", x1, y1, sic
            m.hexbin(x1,y1, C=sic, gridsize=len(sic), cmap=plt.cm.jet)
    
       
            m.drawcoastlines()
            m.fillcontinents(lake_color='white')
            # draw parallels and meridians.
            m.drawparallels(np.arange(-80.,81.,20.))
            m.drawmeridians(np.arange(-180.,181.,20.))
            m.drawmapboundary(fill_color='green')
    
        
            m.colorbar(location="right",label="SIC") # draw colorbar
            plt.title("Sea Ice Concentration - South Pole")
            fig = plt.gcf()
            plt.show()
            f_name = "./img/"+filename + "_.png"
            fig.savefig(f_name)
            plt.close()
            
            # Delete auxiliar variables.
            del m
            del lng    
            del lat    
            del sic    
            del x1
            del y1
            
            return f_name
            
    def drawHkSPole(self, filename="nodet"):
        if (len(self)!=0):
            ms = Basemap(projection='spstere',boundinglat=-50,lon_0=180,resolution='h', round=True)
            lat = []
            lng = []
            sic = []
            for s in self:
                lng.append(s.getLon())
                lat.append(s.getLat())
                sic.append(s.getSic())
            lng = np.array(lng)
            lat = np.array(lat)
            sic = np.array(sic)
            
            plt.figure()
            x1,y1= ms(lng, lat) 
            ms.hexbin(x1,y1, C=sic, gridsize=len(sic), cmap=plt.cm.jet)
            
            ms.drawcoastlines()
            ms.fillcontinents(lake_color='green')
            ms.drawparallels(np.arange(-80.,81.,20.))
            ms.drawmeridians(np.arange(-180.,181.,20.))
            ms.drawmapboundary(fill_color='white')
            ms.colorbar(location="right",label="SIC") # draw colorbar            
            
            plt.title("Sea Ice south Concentration")
            fig = plt.gcf()
            plt.show()
            f_name = "./img/"+filename + "S.png"
            fig.savefig(f_name)
            
            plt.close()
            
            
            del ms

            del lng    
            del lat    
            del sic    
            del x1
            del y1
            
            return f_name
            
    def saveImageHkSPole(self, folder, filename):
        
        #print "Salvando, folder, filename:", folder, filename
        if (len(self)!=0):
            ms = Basemap(projection='spstere',boundinglat=-50,lon_0=180,resolution='h', round=True)
            lat = []
            lng = []
            sic = []
            for s in self:
                lng.append(s.getLon())
                lat.append(s.getLat())
                sic.append(s.getSic())
                #print s.getLat(), s.getLon(), s.getSic()                 
                
            lng = np.array(lng)
            lat = np.array(lat)
            sic = np.array(sic)
            
            #plt.figure()
            x1,y1= ms(lng, lat) 
            #ms.hexbin(x1,y1, C=sic, gridsize=len(sic), cmap=plt.cm.jet)
            ms.scatter(x1, y1, c=sic, s=20 , marker='o', cmap=plt.cm.jet, alpha=1, linewidth=1)
            
            ms.drawcoastlines()
            ms.fillcontinents(lake_color='green')
            ms.drawparallels(np.arange(-80.,81.,20.))
            ms.drawmeridians(np.arange(-180.,181.,20.))
            ms.drawmapboundary(fill_color='white')
            ms.colorbar(location="right",label="SIC") # draw colorbar            
            
            #plt.title("Sea Ice south Concentration")
            fig = plt.gcf()
            #plt.show()
            f_name = filename + "S.png"
            
            #mal solo sirve para linux
            fig.savefig(folder+"/"+f_name)
            
            plt.close()
            
            
            del ms

            del lng    
            del lat    
            del sic    
            del x1
            del y1
            
            return f_name
    
    
            
            
    def saveImageHkNPole(self, folder, filename):
        
        print "Salvando, folder, filename:", folder, filename
        if (len(self)!=0):
            ms = Basemap(projection='npstere',boundinglat=50,lon_0=180,resolution='h', round=True)
            lat = []
            lng = []
            sic = []
            for s in self:
                lng.append(s.getLon())
                lat.append(s.getLat())
                sic.append(s.getSic())
                #print s.getLat(), s.getLon(), s.getSic()                 
                
            lng = np.array(lng)
            lat = np.array(lat)
            sic = np.array(sic)
            
            #plt.figure()
            x1,y1= ms(lng, lat) 
            #ms.hexbin(x1,y1, C=sic, gridsize=len(sic), cmap=plt.cm.jet)
            ms.scatter(x1, y1, c=sic, s=20 , marker='o', cmap=plt.cm.jet, alpha=1, linewidth=1)
            ms.drawcoastlines()
            ms.fillcontinents(lake_color='green')
            ms.drawparallels(np.arange(-80.,81.,20.))
            ms.drawmeridians(np.arange(-180.,181.,20.))
            ms.drawmapboundary(fill_color='white')
            ms.colorbar(location="right",label="SIC") # draw colorbar            
            
            #plt.title("Sea Ice south Concentration")
            fig = plt.gcf()
            #plt.show()
            f_name = filename + "N.png"
            
            #mal solo sirve para linux
            fig.savefig(folder+"/"+f_name)
            
            plt.close()
            
            
            del ms

            del lng    
            del lat    
            del sic    
            del x1
            del y1
            
            return f_name
    
            
    def drawHkNPole(self, filename="nodet"):
        if (len(self)!=0):
            ms = Basemap(projection='npstere',boundinglat=50,lon_0=180,resolution='h', round=True)
            lat = []
            lng = []
            sic = []
            for s in self:
                lng.append(s.getLon())
                lat.append(s.getLat())
                sic.append(s.getSic())
                #print s.getLat(), s.getLon(), s.getSic()                 
                
            lng = np.array(lng)
            lat = np.array(lat)
            sic = np.array(sic)
            
            plt.figure()
            x1,y1= ms(lng, lat) 
            ms.hexbin(x1,y1, C=sic, gridsize=len(sic), cmap=plt.cm.jet)
            
            ms.drawcoastlines()
            ms.fillcontinents(lake_color='green')
            ms.drawparallels(np.arange(-80.,81.,20.))
            ms.drawmeridians(np.arange(-180.,181.,20.))
            ms.drawmapboundary(fill_color='white')
            ms.colorbar(location="right",label="SIC") # draw colorbar            
            
            plt.title("Sea Ice south Concentration")
            fig = plt.gcf()
            plt.show()
            f_name = "./img/"+filename + "S.png"
            fig.savefig(f_name)
            
            plt.close()
            
            
            del ms

            del lng    
            del lat    
            del sic    
            del x1
            del y1
            
            return f_name
    
    
    
            
    def drawHkPoles(self, filename="nodet"):
   
       #    print sic
       # setup south polar stereographic basemap.
       if (len(self)!=0):
            ms = Basemap(projection='spstere',boundinglat=-50,lon_0=180,resolution='h', round=True)
            mn = Basemap(projection='npstere',boundinglat=50,lon_0=180,resolution='h', round=True)
        
        
            lat = []
            lng = []
            sic = []
            
            for s in self:
                lng.append(s.getLon())
                lat.append(s.getLat())
                sic.append(s.getSic())
            
        
            lng = np.array(lng)
            lat = np.array(lat)
            sic = np.array(sic)
            
            plt.figure()
       
            x1,y1= ms(lng, lat)
            ms.hexbin(x1,y1, C=sic, gridsize=len(sic), cmap=plt.cm.jet)
            
            ms.drawcoastlines()
            ms.fillcontinents(lake_color='white')
            ms.drawparallels(np.arange(-80.,81.,20.))
            ms.drawmeridians(np.arange(-180.,181.,20.))
            ms.drawmapboundary(fill_color='white')
            ms.colorbar(location="right",label="SIC") # draw colorbar            
            
            plt.title("both poles")
            fig = plt.gcf()
            plt.show()
            f_name = "./img/"+filename + "S.png"
            fig.savefig(f_name)
            
            ##Finalizado el ploteo del sur
            plt.close()
            
            
            plt.figure()
            x1,y1= mn(lng, lat)
            mn.hexbin(x1,y1, C=sic, gridsize=len(sic), cmap=plt.cm.jet)
            
            mn.drawcoastlines()
            mn.fillcontinents(lake_color='green')
            # draw parallels and meridians.
            mn.drawparallels(np.arange(-80.,81.,20.))
            mn.drawmeridians(np.arange(-180.,181.,20.))
            mn.drawmapboundary(fill_color='white')
    
            mn.colorbar(location="right",label="SIC") # draw colorbar
                
            plt.title("Sea Ice north Concentration")
            fig = plt.gcf()
            plt.show()
            f_name = "./img/"+filename + "N.png"
            fig.savefig(f_name)

            
            
            
            

            plt.close()
            
            # Delete auxiliar variables.
            del ms
            del mn
            del lng    
            del lat    
            del sic    
            del x1
            del y1
            
            return f_name
