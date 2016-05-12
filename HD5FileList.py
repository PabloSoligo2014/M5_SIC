# -*- coding: utf-8 -*-
"""
Created on Tue May 10 11:07:38 2016

@author: ubuntumate

AUXDATA

EO_20130424_000704_CUSS_SACD_MWR_L1B_SCI_078_000_004.tar.gz EO_20130424_014452_CUSS_SACD_MWR_L1B_SCI_071_000_004.tar.gz EO_20130424_032240_CUSS_SACD_MWR_L1B_SCI_064_000_004.tar.gz
EO_20130424_050028_CUSS_SACD_MWR_L1B_SCI_057_000_004.tar.gz



EO_20130424_000704_CUSS_SACD_MWR_L2B_SCI_078_000_004.h5 EO_20130424_014452_CUSS_SACD_MWR_L2B_SCI_071_000_004.h5 EO_20130424_032240_CUSS_SACD_MWR_L2B_SCI_064_000_004.h5 EO_20130424_050028_CUSS_SACD_MWR_L2B_SCI_057_000_004.h5
"""


from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

import numpy as np
import pylab as P

from mwr_tie_points_finder import print_tie_points
from L2Bean import L2Bean


import h5py
import sys


"""
EO_20130426_003316_CUSS_SACD_MWR_L2B_SCI_074_000_004.h5 EO_20130430_190916_CUSS_SACD_MWR_L2B_SCI_099_000_004.h5 EO_20130430_204704_CUSS_SACD_MWR_L2B_SCI_092_000_004.h5
"""


class HD5FileList(list):
    
    def __init__(self, filelist):
        
        super(list, self).__init__()
        self._lats = []
        self._lons = []
        self._sics = []  
        
        self._AP   = []
        self._AG   = []
        self._filelist = filelist
        
        print self._filelist
        
        #beanlist = []
        for fl in self._filelist:
            
            f = h5py.File("./output/"+fl, "r")
            datadic = dict()
            
            
            datadic["DP"]   = f["Intermediate Data"]["DP"][:] 
            datadic["DG"]   = f["Intermediate Data"]["DG"][:] 
            datadic["gg_index"]   = f["Intermediate Data"]["gg_index"][:] 
            datadic["lat"]   = f["Intermediate Data"]["lat"][:] 
            datadic["lon"]   = f["Intermediate Data"]["lon"][:] 
            datadic["surface"]   = f["Intermediate Data"]["surface"][:] 
            
                     
            for i in range(0, len(datadic["DP"])):
                for j in range(0, 8):
                   
                   
                   l2bean = L2Bean( datadic["gg_index"][i][j], datadic["lat"][i][j], datadic["lon"][i][j], j, datadic["surface"][i][j], datadic["DP"][i][j], datadic["DG"][i][j] )
                    #(Ak_h_bean, Aka_h_bean, Aka_v_bean, cornet, gg, surface)                   
                   
                   
                   self.append(l2bean)
                                        

            f.close()
        #print "Total de beans:", len(self)
        
              
        
        #listsurface1 = [elem for elem in self if elem.surface == 1]    
        
    #Dibuja histrogramas a partir de los datos tomados de los archivo
        
        
    def drawTiePointsHistrogram(self):
        pass
    
    def drawFHistrograms(self) :


        
        ApEvenSouth = [elem.getDP() for elem in self if ( (elem.getSurface() in (1,5))  and  (elem.getBean()+1) % 2) == 0 and elem.getLat()<0] 
        AgEvenSouth = [elem.getDG() for elem in self if ( (elem.getSurface() in (1,5))  and  (elem.getBean()+1) % 2) == 0 and elem.getLat()<0] 
        minv = min(len(ApEvenSouth), len(AgEvenSouth))
        self._draw("Histrograma sur/par", ApEvenSouth[0:minv], AgEvenSouth[0:minv], 500)


        ApEvenNorth = [elem.getDP() for elem in self if ( (elem.getSurface() in (1,5))  and  (elem.getBean()+1) % 2) == 0 and elem.getLat()>0] 
        AgEvenNorth = [elem.getDG() for elem in self if ( (elem.getSurface() in (1,5))  and  (elem.getBean()+1) % 2) == 0 and elem.getLat()>0] 
        minv = min(len(ApEvenNorth), len(AgEvenNorth))
        self._draw("Histrograma norte/par", ApEvenNorth[0:minv], AgEvenNorth[0:minv], 500)


        ApOddSouth = [elem.getDP() for elem in self if ( (elem.getSurface() in (1,5))  and  (elem.getBean()+1) % 2) != 0 and elem.getLat()<0] 
        AgOddSouth = [elem.getDG() for elem in self if ( (elem.getSurface() in (1,5))  and  (elem.getBean()+1) % 2) != 0 and elem.getLat()<0] 
        minv = min(len(ApOddSouth), len(AgOddSouth))
        self._draw("Histrograma sur/impar", ApOddSouth[0:minv], AgOddSouth[0:minv], 500)

        
        ApOddNorth = [elem.getDP() for elem in self if ( (elem.getSurface() in (1,5))  and  (elem.getBean()+1) % 2) != 0 and elem.getLat()>0] 
        AgOddNorth = [elem.getDG() for elem in self if ( (elem.getSurface() in (1,5))  and  (elem.getBean()+1) % 2) != 0 and elem.getLat()>0] 
        minv = min(len(ApOddNorth), len(AgOddNorth))
        self._draw("Histrograma norte/impar", ApOddNorth[0:minv], AgOddNorth[0:minv], 500)
 
        """
        Ultima charla con Sergio indica hacer lo siguiente:
            ->Usar la funcion de Matias, hacerlo por numero de bean...obtener DP/DG y count, la funcion devuelve mas de uno, quedarse
            con el mas grande (imagino que de count) o el promedio. Hacerlo por hemisferio, quedan 16 "Graficos"

            ->Tomar los valores resultantes que y graficarlos en 4 graficos ahora si por beans pares e impares y norte y sur. Quedarian
            4 graficos con cuatro 4 puntos no???

        """
        
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


if __name__ == "__main__":
    
    l1b_file = sys.argv[1]   
    
    filelist = []
    for fi in range(1, len(sys.argv)):
        filelist.append(sys.argv[fi])
        
        
    fm = HD5FileList(filelist)
    fm.drawFHistrograms()
    