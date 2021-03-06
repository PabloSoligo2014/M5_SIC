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

from mwr_tie_points_finder import print_tie_points
from L2Bean import L2Bean


import h5py
import sys
import mwr_tie_points_finder
from scipy.stats import gaussian_kde
from L3Bean import L3Bean



"""
EO_20130426_003316_CUSS_SACD_MWR_L2B_SCI_074_000_004.h5 EO_20130430_190916_CUSS_SACD_MWR_L2B_SCI_099_000_004.h5 EO_20130430_204704_CUSS_SACD_MWR_L2B_SCI_092_000_004.h5
"""


class HD5FileList(list):
    
    def getSics(self):
        return self._sics
    def getLons(self):
        return self._lons
    def getLats(self):
        return self._lats
        
    
    
    def __init__(self, filefolder, filelist):
        
        super(list, self).__init__()
        self._lats = []
        self._lons = []
        self._sics = []  
        
        self._AP   = []
        self._AG   = []
        self._filelist = filelist
        
        #print self._filelist
        
        #beanlist = []
        
        for fl in self._filelist:
            
            f = h5py.File(filefolder+fl, "r")
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
        
        

    
    def plot_histogram(self, x, y, title):
        
        """ Plots a 2d histogram
        """
        print "plotting", title, "histogram"  
        new_x=np.array(x[1])
        new_y=np.array(y[1])
        xy = np.vstack([new_x,new_y])
        z = gaussian_kde(xy)(xy)       
        idx = z.argsort()
        x, y, z = new_x[idx], new_y[idx], z[idx]
        fig, ax = plt.subplots()
        ax.scatter(x,y,c=z, s=20, edgecolor='')
        plt.title(title)
        plt.show()
        fig = plt.gcf()
        fig.savefig(title + ".png")
        plt.close()
        #plt.clf()
        
    def plot_points(self, x, y, title, save=True, folder="./"):      
        plt.figure()
        plt.title(title)
        #plt.plot([x[0], y[0]], [x[1], y[1]] ,'o',label=1)
        
        #print "x,y", len(x), len(y)
        
        plt.plot(x, y,'o',label=1)
        plt.xlabel("DP")
        plt.ylabel("DG")
        plt.legend(loc='best')
        
        
        if (save):
            plt.savefig(folder+title)
            
        plt.show()
        #plt.clf()
        #sys.exit()

    
        
    def drawPointsHistograms2(self):
                #result
        """
        parNorteAp   = []
        parNorteAg   = []
        imparNorteAp = []
        imparNorteAg = []
        
        parSurAp   = []
        parSurAg   = []
        imparSurAp = []
        imparSurAg = []
        """
            
                    
        
    
        ApEvenSouth = [elem.getDP() for elem in self if ( (elem.getSurface() in (1,5))  and  (elem.getBean()+1) % 2) == 0 and elem.getLat()<0 and elem.getGG()!=-99] 
        AgEvenSouth = [elem.getDG() for elem in self if ( (elem.getSurface() in (1,5))  and  (elem.getBean()+1) % 2) == 0 and elem.getLat()<0 and elem.getGG()!=-99] 
        
        
        minv = min(len(ApEvenSouth), len(AgEvenSouth))
        #print "histo con problemas", ApEvenSouth, AgEvenSouth
        self._draw("Densigrama sur/par", ApEvenSouth[0:minv], AgEvenSouth[0:minv], 200)

        
        
    
        ApEvenNorth = [elem.getDP() for elem in self if ( (elem.getSurface() in (1,5))  and  (elem.getBean()+1) % 2) == 0 and elem.getLat()>0 and elem.getGG()!=-99] 
        AgEvenNorth = [elem.getDG() for elem in self if ( (elem.getSurface() in (1,5))  and  (elem.getBean()+1) % 2) == 0 and elem.getLat()>0 and elem.getGG()!=-99] 
        minv = min(len(ApEvenNorth), len(AgEvenNorth))
        self._draw("Densigrama norte/par", ApEvenNorth[0:minv], AgEvenNorth[0:minv], 200)
        

        ApOddSouth = [elem.getDP() for elem in self if ( (elem.getSurface() in (1,5))  and  (elem.getBean()+1) % 2) != 0 and elem.getLat()<0 and elem.getGG()!=-99] 
        AgOddSouth = [elem.getDG() for elem in self if ( (elem.getSurface() in (1,5))  and  (elem.getBean()+1) % 2) != 0 and elem.getLat()<0 and elem.getGG()!=-99] 
        minv = min(len(ApOddSouth), len(AgOddSouth))
        self._draw("Densigrama sur/impar", ApOddSouth[0:minv], AgOddSouth[0:minv], 200)
    
        
        
        ApOddNorth = [elem.getDP() for elem in self if ( (elem.getSurface() in (1,5))  and  (elem.getBean()+1) % 2) != 0 and elem.getLat()>0 and elem.getGG()!=-99] 
        AgOddNorth = [elem.getDG() for elem in self if ( (elem.getSurface() in (1,5))  and  (elem.getBean()+1) % 2) != 0 and elem.getLat()>0 and elem.getGG()!=-99] 
        minv = min(len(ApOddNorth), len(AgOddNorth))
        self._draw("Densigrama norte/impar", ApOddNorth[0:minv], AgOddNorth[0:minv], 200)

        
        
        
        
        
    def drawTiePointsHistograms(self):
        
        ##realizamos todos los agrupamientos para estar listo segun consigna indique        
        
        print "Drawing histograms"
        icePs = []
        iceGs = []
        seaPs = []
        seaGs = []
      
        
        
        ap = []
        ag = []
        for i in range(0,8):
            #print "tam:", len(self.getDGbyBean(i, 'N'))
            if((i+1)%2==1):
                iceCount, IceP, IceG, seaCount, SeaP, SeaG = mwr_tie_points_finder.print_tie_points( self.getDPbyBean(i, 'N'), self.getDGbyBean(i, 'N') )
                icePs.append(IceP)
                iceGs.append(IceG)
                seaPs.append(SeaP)
                seaGs.append(SeaG)
                ap.append(IceP)
                ap.append(SeaP)
                
                ag.append(IceG)
                ag.append(SeaG)
                
        
        print "Drawing north Odd"
        self.plot_points(ap, ag, "Points Norte, impar", True, "./p2output/")    
        
        ap = []
        ag = []
        i = 0
        
        for i in range(0,8):
            if(((i+1)%2)==0):
                iceCount, IceP, IceG, seaCount, SeaP, SeaG = mwr_tie_points_finder.print_tie_points( self.getDPbyBean(i, 'N'), self.getDGbyBean(i, 'N') )
                icePs.append(IceP)
                iceGs.append(IceG)
                seaPs.append(SeaP)
                seaGs.append(SeaG)
                ap.append(IceP)
                ap.append(SeaP)
                
                ag.append(IceG)
                ag.append(SeaG)
                
            
        
        self.plot_points(ap, ag, "Points Norte, par", True, "./p2output/")    
        #self._draw("Tie points South Odd", iceGsOddSouth, icePsOddSouth, 100)     
        
        
        ap = []
        ag = []
        
        for i in range(0,8):
            if((i+1)%2==1):
                iceCount, IceP, IceG, seaCount, SeaP, SeaG = mwr_tie_points_finder.print_tie_points( self.getDPbyBean(i, 'S'), self.getDGbyBean(i, 'S') )
                icePs.append(IceP)
                iceGs.append(IceG)
                seaPs.append(SeaP)
                seaGs.append(SeaG)
                ap.append(IceP)
                ap.append(SeaP)
                
                ag.append(IceG)
                ag.append(SeaG)
                
            
        
        self.plot_points(ap, ag, "Points sur, impar", True, "./p2output/")    
        
        
        
        ap = []
        ag = []
        
        for i in range(0,8):
            if((i+1)%2==0):
                iceCount, IceP, IceG, seaCount, SeaP, SeaG = mwr_tie_points_finder.print_tie_points( self.getDPbyBean(i, 'S'), self.getDGbyBean(i, 'S') )
                icePs.append(IceP)
                iceGs.append(IceG)
                seaPs.append(SeaP)
                seaGs.append(SeaG)
                ap.append(IceP)
                ap.append(SeaP)
                
                ag.append(IceG)
                ag.append(SeaG)
                
            
        
        self.plot_points(ap, ag, "Points sur, par", True, "./p2output/")    
        #self._draw("Tie points South Odd", iceGsOddSouth, icePsOddSouth, 100)
        
        
    def saveH5L3(self, filename):
        
        
        #Agrupamiento
        l3beanDict = dict()
        print "Arrancando lista final"
        for element in self:
            
            b = l3beanDict.get(str(element.getGG()), None)
            
            if b==None:
                
                b = L3Bean()
                b.add(element)
                l3beanDict[str(element.getGG())] = b
                
            else:
                
                b.add(element)
        
        f = h5py.File(filename, "w")
        
        l3beanlist = list(l3beanDict.values())
        grp = f.create_group("L3 Final")
        grp.create_dataset("sic",data=[elem.getMedSic() for elem in l3beanlist])
        grp.create_dataset("lat",data=[elem.getLat() for elem in l3beanlist])
        grp.create_dataset("lon",data=[elem.getLon() for elem in l3beanlist])
        grp.create_dataset("gg",data=[elem.getGG() for elem in l3beanlist])
                           
        f.flush()
        f.close()
        
    def drawWholeSouthMap(self, save=True, folder="./"):
       
        #Se usa diccionario tratando de mejorar tiempos
        l3beanDict = dict()
        print "Arrancando lista final"
        for element in self:
            
            b = l3beanDict.get(str(element.getGG()), None)
            
            if b==None:
                
                b = L3Bean()
                b.add(element)
                l3beanDict[str(element.getGG())] = b
                
            else:
                
                b.add(element)

        
        plt.figure()
        ms = Basemap(projection='spstere',boundinglat=-50,lon_0=270,resolution='h', round=True)    
        ms.drawcoastlines()
        ms.drawcountries()
        ms.fillcontinents(color='grey')
        ms.drawmapboundary(fill_color='aqua')
        
        
        #Al no existir o no conocer la posibilidad de crear listas con tipos
        #Generics(C#-Java)/Templates(C++) no es clara la mejor solucion
        #si crear listas propias o realizar los filtros como se indica
        #sics = [elem.getMedSic for elem in l3beanlist if (True) ]    
            
        l3beanlist = list(l3beanDict.values())
        
        
        
        sics = [elem.getMedSic() for elem in l3beanlist if not elem.isNorth()]
        lats = [elem.getLat() for elem in l3beanlist if not elem.isNorth()]
        lons = [elem.getLon() for elem in l3beanlist if not elem.isNorth()]
        
        
        print "tam sics sur", len(sics)
        x1 = []
        y1 = []
        x1,y1= ms(lons, lats)
        
        ms.scatter(x1, y1, c=sics, s=20 , marker='o', cmap=plt.cm.jet, alpha=1, linewidth=1)
         
        
        ms.drawmeridians(np.arange(0, 360, 30))
        ms.drawparallels(np.arange(-90, 90, 30))
        #print "fin scatter"     
       
        #plt.gcf().set_size_inches(18,10)
        if(save):
           
            plt.savefig(folder+"WholeSouth.png")
        plt.show()    
        del sics
        del lats
        del lons
        #points.remove()
        del ms
        del l3beanDict
        
        
        
        
        
    def drawWholeNorthMap(self, save=True, folder="./"):
       
        #Se usa diccionario tratando de mejorar tiempos
        l3beanDict = dict()
        print "Arrancando lista final"
        for element in self:
            
            b = l3beanDict.get(str(element.getGG()), None)
            if b==None:
                b = L3Bean()
                b.add(element)
                l3beanDict[str(element.getGG())] = b
                
            else:
                
                b.add(element)
                #print "encontrado"
        
        print "tamano de lista final", len(l3beanDict)
        
        
        plt.figure()
        
        
        my_map = Basemap(projection='npstere',boundinglat=50,lon_0=270,resolution='h', round=True)    
        my_map.drawcoastlines()
        my_map.drawcountries()
        my_map.fillcontinents(color='grey')
        my_map.drawmapboundary(fill_color='aqua')
        
        
        #Al no existir o no conocer la posibilidad de crear listas con tipos
        #Generics(C#-Java)/Templates(C++) no es clara la mejor solucion
        #si crear listas propias o realizar los filtros como se indica
        #sics = [elem.getMedSic for elem in l3beanlist if (True) ]    
            
        l3beanlist = list(l3beanDict.values())
        
        
        
        sics = [elem.getMedSic() for elem in l3beanlist if elem.isNorth()]
        lats = [elem.getLat() for elem in l3beanlist if elem.isNorth()]
        lons = [elem.getLon() for elem in l3beanlist if elem.isNorth()]
        
        print "tam sics norte", len(sics)
        x1 = []
        y1 = []
       
        x1,y1= my_map(lons, lats)
        
        points = my_map.scatter(x1, y1, c=sics, s=20 , marker='o', cmap=plt.cm.jet, alpha=1, linewidth=1)
        
         
        my_map.drawmeridians(np.arange(0, 360, 30))
        my_map.drawparallels(np.arange(-90, 90, 30))
        #print "fin scatter"     
        
        #plt.gcf().set_size_inches(18,10)
        
        if(save):
           
            plt.savefig(folder+"WholeNorth.png")
        plt.show()    
        
        del sics
        del lats
        del lons
        points.remove()
        del my_map
        del l3beanDict
        
    def saveToFile(self, filename):
        ##realizamos todos los agrupamientos para estar listo segun consigna indique        
        
        
        text_file = open(filename, "w")
        text_file.writelines("Hemisferio Norte\n")    
        text_file.writelines("Nro\t\tIceP\t\tIceG\t\tSeaP\t\tSeaG\n")    
            
        for i in range(0,8):
            iceCount, IceP, IceG, seaCount, SeaP, SeaG = mwr_tie_points_finder.print_tie_points( self.getDPbyBean(i, 'N'), self.getDGbyBean(i, 'N') )
            text_file.writelines(str(i)+"\t\t"+str(IceP)+"\t\t"+str(IceG)+"\t\t"+str(SeaP)+"\t\t"+str(SeaG)+"\n")    
         
         
        text_file.writelines("Hemisferio Sur\n")    
        text_file.writelines("Nro\t\tIceP\t\tIceG\t\tSeaP\t\tSeaG\n")   
        for i in range(0,8):
            iceCount, IceP, IceG, seaCount, SeaP, SeaG = mwr_tie_points_finder.print_tie_points( self.getDPbyBean(i, 'S'), self.getDGbyBean(i, 'S') )
            text_file.writelines(str(i)+"\t\t"+str(IceP)+"\t\t"+str(IceG)+"\t\t"+str(SeaP)+"\t\t"+str(SeaG)+"\n")    
         
       
            
        text_file.close()
        
        
        
    def getDPbyBean(self, nroBean, hemisferio):
        if (hemisferio=='N'):
            result = [elem.getDP() for elem in self if ((elem.getSurface() in (1,5))  and  (elem.getBean() == nroBean) and (elem.isNorth()) and elem.getGG()!=-99)] 
        else:
            result = [elem.getDP() for elem in self if ((elem.getSurface() in (1,5))  and  (elem.getBean() == nroBean) and (not elem.isNorth()) and elem.getGG()!=-99)] 
        
        return result
            
        
    def getDGbyBean(self, nroBean, hemisferio):
        if (hemisferio=='N'):
            result = [elem.getDG() for elem in self if ((elem.getSurface() in (1,5))  and  (elem.getBean() == nroBean) and (elem.isNorth()) and elem.getGG()!=-99) ] 
        else:
            result = [elem.getDG() for elem in self if ((elem.getSurface() in (1,5))  and  (elem.getBean() == nroBean) and (not elem.isNorth()) and elem.getGG()!=-99)] 
            
        return result
    
    def drawFHistrograms(self):
        #result
        ApEvenSouth = [elem.getDP() for elem in self if ( (elem.getSurface() in (1,5))  and  (elem.getBean()+1) % 2) == 0 and (not elem.isNorth()) and elem.getGG()!=-99] 
        AgEvenSouth = [elem.getDG() for elem in self if ( (elem.getSurface() in (1,5))  and  (elem.getBean()+1) % 2) == 0 and (not elem.isNorth()) and elem.getGG()!=-99] 
        minv = min(len(ApEvenSouth), len(AgEvenSouth))
        
        #print "histo con problemas", ApEvenSouth, AgEvenSouth
        self._draw("Histrograma sur/par", ApEvenSouth[0:minv], AgEvenSouth[0:minv], 200)


        ApEvenNorth = [elem.getDP() for elem in self if ( (elem.getSurface() in (1,5))  and  (elem.getBean()+1) % 2) == 0 and elem.isNorth() and elem.getGG()!=-99] 
        AgEvenNorth = [elem.getDG() for elem in self if ( (elem.getSurface() in (1,5))  and  (elem.getBean()+1) % 2) == 0 and elem.isNorth() and elem.getGG()!=-99] 
        minv = min(len(ApEvenNorth), len(AgEvenNorth))
        self._draw("Histrograma norte/par", ApEvenNorth[0:minv], AgEvenNorth[0:minv], 200)


        ApOddSouth = [elem.getDP() for elem in self if ( (elem.getSurface() in (1,5))  and  (elem.getBean()+1) % 2) != 0 and (not elem.isNorth()) and elem.getGG()!=-99] 
        AgOddSouth = [elem.getDG() for elem in self if ( (elem.getSurface() in (1,5))  and  (elem.getBean()+1) % 2) != 0 and (not elem.isNorth()) and elem.getGG()!=-99] 
        minv = min(len(ApOddSouth), len(AgOddSouth))
        self._draw("Histrograma sur/impar", ApOddSouth[0:minv], AgOddSouth[0:minv], 200)

        
        ApOddNorth = [elem.getDP() for elem in self if ( (elem.getSurface() in (1,5))  and  (elem.getBean()+1) % 2) != 0 and elem.isNorth() and elem.getGG()!=-99] 
        AgOddNorth = [elem.getDG() for elem in self if ( (elem.getSurface() in (1,5))  and  (elem.getBean()+1) % 2) != 0 and elem.isNorth() and elem.getGG()!=-99] 
        minv = min(len(ApOddNorth), len(AgOddNorth))
        self._draw("Histrograma norte/impar", ApOddNorth[0:minv], AgOddNorth[0:minv], 200)
 
        """
        Ultima charla con Sergio indica hacer lo siguiente:
            ->Usar la funcion de Matias, hacerlo por numero de bean...obtener DP/DG y count, la funcion devuelve mas de uno, quedarse
            con el mas grande (imagino que de count) o el promedio. Hacerlo por hemisferio, quedan 16 "Graficos"

            ->Tomar los valores resultantes que y graficarlos en 4 graficos ahora si por beans pares e impares y norte y sur. Quedarian
            4 graficos con cuatro 4 puntos no???

        """
        
    def _draw(self, title, x, y, bins):
        plt.figure()
                   
        plt.hist2d(x, y, bins)
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
        

        



    