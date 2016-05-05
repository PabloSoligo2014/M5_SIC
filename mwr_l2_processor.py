import sys
import os

import tarfile
import numpy as np
import h5py

import tarfile

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
#import gdal

#import numpy as np

#basemap

#Calibrar: 1 sea / 5 posible hielo
#L2 1,5 3


CONST_K_H_BAND  =  "k_h"
CONST_KA_H_BAND =  "ka_h" 
CONST_KA_V_BAND =  "ka_v" 
    
    
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
        numerador = (self.getAG()-self.getOpenWaterG()) - ((self.getAP()-self.getOpenWaterP()) * self.getAlpha())
        denominador = (self.getMultiYearIceG()-self.getOpenWaterG())-((self.getMultiYearIceP()-self.getOpenWaterP())*self.getAlpha())

         
        #print "Numerador, Denominador, Cornet", numerador, denominador, self.cornet    
        ##return numerador/denominador
        #ponemos valor absoluto aunque no se bien porque es necesario
        val = numerador/denominador
        if(val<0):
            return 0
        elif(val>1):
            return 1
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
        


class Bean:
    
    #No pueden ser privados?
    gg_index  = 0
    lat       = 0.0
    lon       = 0.0
    tbs       = 0.0
    band      = "No det"
    bean      = 0
    surface   = 0    
    
    def __init__(self):
              
        self.gg_index  = 0
        self.lat       = 0.0
        self.lon       = 0.0
        self.tbs       = 0
        self.band      = "No det"
        self.bean      = 0
        self.surface   = 0
        
    def getTbs(self):
        #MATIAS Como es que python no permite acceder a mas de un nivel de profundidad
        #Java, C#, Delphi, C++, VB permiten
        #print "getTbs: ", self.__tbs         
        return self.tbs
        
    def setTbs(self, value):
        #print "set tbs", value
        self.tbs = value    
        
    def addLat(self, value):
        self.lat = value
    def addLon(self, value):
        self.lon = value
        
     
    
    def getLat(self):
        return self.lat                
    
    def getLon(self):
        return self.lon
        
    def getBand(self):
        return self.band 
        
    def getSurface(self):
        return self.surface
        
    def getGG(self):
        return self.gg_index
        
    def __eq__(self, other):
        return self.gg_index == other.gg_index
        
    def __hash__(self):
        return 1
        
    def __cmp__(self,other):
        return cmp(self.getGG(),other.getGG())
        
        

        
    
#Esta clase agrupa todos los beans en uno solo sic
class Measure:
    lat=0.0
    lon=0.0
    gg = 0  
    meds = 0
    sics = 0
    
    def __init__(self, lat, lon, gg, sic):
        self.lat = lat
        self.lon = lon
        self.gg = gg
        self.sics = sic
        self.meds = 1       
    def getLat(self):
        return self.lat/self.meds
    def getLon(self):
        return self.lon/self.meds
   
    def getGG(self):
        return self.gg
    def getSic(self):
        return self.sics/(self.meds)

        
    def addValue(self, mbBean):
        self.sics = self.sics + mbBean.getSic() 
        self.lat = self.lat + mbBean.getLat() 
        self.lon = self.lon + mbBean.getLon()
        self.meds = self.meds + 1

        
    def __eq__(self, other):
        return type(self) == type(other) and self.getGG() == other.getGG()
        
    def __hash__(self):
        return 1
        
    
 

   
        
class BandBeanList(list):
    
    _band = -1
    def __init__(self, band, *args):
        list.__init__(self, *args)
        self._band = band
    
    def getBand(self):
        return self._band
        
    def add(self, obj):
        
        if(obj.getCornet()!=self.getBand()):
            raise Exception('Error al asignar elemento a lista de banda distinta')
        else:
            super(BandBeanList, self).append(obj)
            
class MultiBandBeanDict(dict):
    def saveToFile(self, filename):
       
        #mfile = h5py.File("./output/"+filename,'w')
        # Open "dset" dataset under the root group.
        
        for b in range(0, 8):
            #obtengo el bandbeanlist para la banda
            bbl = self["Band"+str(b)]
            for x in bbl:
                MultibandBean(x).
                        
            
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
        o = Measure(obj.getLat(), obj.getLon(), obj.getGG(), obj.getSic())
        self.append(o)
            
    def draw(self):
        #No es muy ortodoxo dibujar dentro de la clase
        my_map = Basemap(projection='spstere',boundinglat=-50,lon_0=270,resolution='h', round=True)    
        my_map.drawcoastlines()
        my_map.drawcountries()
        my_map.fillcontinents(color='coral')
        my_map.drawmapboundary()
    
        for measure in self:
            x,y = my_map(measure.getLon(), measure.getLat())
            
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
            m.drawmapboundary(fill_color='white')
    
        
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
            
            plt.title("Sea Ice south Concentration")
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
            mn.fillcontinents(lake_color='white')
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
        
        

def obtain_hdf5_from_l1b(l1b_file):
    """Get the hdf5 file inside the L1B MWR product.

    Parameters
    ----------
    l1b_file : tar.gz file path
        the L1B product path

    Returns
    -------
    string
        The file path of the hdf5 file
    """
    try:
        
        #print "FOLDER->", "/MWR_pasadas/"+l1b_file
        
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
        
    except ValueError:
        print ValueError.message
        
     
    
    


def read_l1b_hdf5_data(hdf5_fname):
    """Get the hdf5 file inside the L1B MWR product.

    Parameters
    ----------
    hdf5_fname : string
        The file path of the hdf5 file

    Returns
    -------
    dict
        It should contain these keys:
            * k_h_geodedic_grid_index
            * k_h_surface_type
            * ka_h_geodedic_grid_index
            * ka_h_surface_type
            * ka_v_geodedic_grid_index
            * ka_v_surface_type
            * k_h_latitude
            * ka_h_latitude
            * ka_v_latitude
            * k_h_antenna_temperature
            * ka_h_antenna_temperature
            * ka_v_antenna_temperature
    """
    
    f = h5py.File(hdf5_fname, "r")
    
    #for n in f.keys():
    #    print n
    
    result = dict()
    
    result["k_h_geodedic_grid_index"]   = f["Ancillary Data"]["k_h_geodedic_grid_index"][:] 
    result["k_h_surface_type"]          = f["Ancillary Data"]["k_h_surface_type"][:] 
    result["ka_h_geodedic_grid_index"]  = f["Ancillary Data"]["ka_h_geodedic_grid_index"][:]   
    result["ka_h_surface_type"]         = f["Ancillary Data"]["ka_h_surface_type"][:]             
    result["ka_v_geodedic_grid_index"]  = f["Ancillary Data"]["ka_v_geodedic_grid_index"][:]             
    result["ka_v_surface_type"]         = f["Ancillary Data"]["ka_v_surface_type"][:]             
    
    result["k_h_latitude"]              = f["Geolocation Data"]["k_h_latitude"][:]             
    result["ka_h_latitude"]             = f["Geolocation Data"]["ka_h_latitude"][:]   
    result["ka_v_latitude"]             = f["Geolocation Data"]["ka_v_latitude"][:]   

    
    result["k_h_longitude"]              = f["Geolocation Data"]["k_h_longitude"][:]             
    result["ka_h_longitude"]             = f["Geolocation Data"]["ka_h_longitude"][:]   
    result["ka_v_longitude"]             = f["Geolocation Data"]["ka_v_longitude"][:]   

    #print "->",len(result["k_h_longitude"])
    #print "->",len(result["ka_h_longitude"])
    #print "->",len(result["ka_v_longitude"])

    result["k_h_antenna_temperature"]   = f["MWR Calibrated Radiometric Data"]["k_h_antenna_temperature"][:]           
    result["ka_h_antenna_temperature"]  = f["MWR Calibrated Radiometric Data"]["ka_h_antenna_temperature"][:]           
    result["ka_v_antenna_temperature"]  = f["MWR Calibrated Radiometric Data"]["ka_v_antenna_temperature"][:]
    
    
    #print "->",len(result["k_h_antenna_temperature"])
    #print "->",len(result["ka_h_antenna_temperature"])
    #print "->",len(result["ka_v_antenna_temperature"])
    
    f.close()
    
    return result


def generate_l2_from_l1b_product(l1b_file):
    """Creates a L2 product from a L1B product.

    Parameters
    ----------
    l1b_file : tar.gz file path

    Returns
    -------
    dp : dict (keys: beams) of np.array
        delta P array for the SIC computation
    dg : dict (keys: beams) of np.array
        delta G array for the SIC computation
    sic : dict (keys: beams) of np.array
        sea ice concentration 
    gg : dict (keys: beams) of np.array
        the corresponding geodesic grid indices       
    """

    hdf5_fname = obtain_hdf5_from_l1b(l1b_file)
    
    if not hdf5_fname:
        print "unable to process", l1b_file, "file, no hdf5 in it"
        return
    
    l1b_hdf5_data = read_l1b_hdf5_data(hdf5_fname)
    
    dp, dg, sic, gg = compute_sic_product(l1b_hdf5_data) 
    create_l2_product(l1b_file, l1b_hdf5_data, dp, dg, sic, gg)
    
    return dp, dg, sic, gg

def printBean(bean):
    print bean.gg_index, bean.lat, bean.lon, bean.getTbs()
    #, bean.__AP, bean.__AG, bean.__AP, bean.__SIC




def promediados(band, dic, latitude, longitude, surface, value, grid_index, tam, surface_filter):
    beans = []
    
    
    
    #print "TAMANO", tam
    for n_bean in range(0, 8):
        filtrados = []
        for i in range(0, tam):   
            lat = dic[latitude][i][n_bean]
            lon = dic[longitude][i][n_bean]
            sur = dic[surface][i][n_bean]
            
            #0=land 1=ocean 2=coast 3=near coast 4=ice 5=possible ice
            if ( 60<=abs(lat))and(sur in surface_filter):
                ne = Bean()
                ne.gg_index   = dic[grid_index][i][n_bean]
                    
                ne.lat        = lat
                ne.lon        = lon
                ne.setTbs(dic[value][i][n_bean])
                ne.band       = band
                ne.bean       = n_bean
                ne.surface    = sur
                filtrados.append(ne)
        
        
        filtrados.sort()
        #sorted(filtrados, key=lambda bean: bean.getGG())
        
        
        promediados = []
        
        
        
        i = 0
        tbsAcu = 0
        cont   = 0
        
        
        while i<len(filtrados)-1:
            #print indexActual, indexAnterior, len(filtrados), i  
        
            indexActual   = filtrados[i].gg_index
            indexAnterior = filtrados[i].gg_index
            while (indexActual==indexAnterior)and(i<len(filtrados)-1):
                tbsAcu = filtrados[i].getTbs()
                cont = cont + 1
                i = i + 1
                indexActual = filtrados[i].gg_index
                    
            
            indexAnterior = indexActual            
            promediado = Bean()
            promediado.setTbs(tbsAcu/cont)
            promediado.lat        = filtrados[i-1].getLat()
            promediado.lon        = filtrados[i-1].getLon()
            promediado.gg_index   = filtrados[i-1].getGG()
            promediado.band       = filtrados[i-1].band
            promediado.bean       = filtrados[i-1].bean
            promediado.surface    = filtrados[i-1].surface 
            #print "ingreso promediado"
            promediados.append(promediado)
            
        
            
        beans.append(promediados)
        
    #for w in beans:
    #    print "Cuantos quedan?->", len(w)
     
    #print "salida"
    return beans
            
   
def draw_map(lat, lng, sic):
    # setup south polar stereographic basemap.
    # The longitude lon_0 is at 6-o'clock, and the
    # latitude circle boundinglat is tangent to the edge
    # of the map at lon_0. Default value of lat_ts
    # (latitude of true scale) is pole.


    m = Basemap(projection='spstere',boundinglat=-50,lon_0=270,resolution='h', round=True)
   # Basemap()
  
    plt.figure()
    for beam in range(8):        
        x1,y1 = m(lng[beam], lat[beam])
        m.hexbin(x1,y1, C=sic[beam],gridsize=len(sic[beam]),cmap=plt.cm.jet)
            
    m.drawcoastlines()
    m.fillcontinents(color='coral',lake_color='aqua')
    # draw parallels and meridians.
    m.drawparallels(np.arange(-80.,81.,20.))
    m.drawmeridians(np.arange(-180.,181.,20.))
    m.drawmapboundary(fill_color='aqua')
    
    m.colorbar(location="bottom",label="SIC") # draw colorbar
    plt.title("North Polar Stereographic Projection")
    plt.gcf().set_size_inches(18,10)
    plt.show()
    
    
class passfile:
    uncompressedFileName = "Empty"
    simpleFileName = "-"
    filename = ""
    cleanFileName = ""    
    
    beans_k_h   = []
    beans_ka_h  = []
    beans_ka_v  = []
    
    def __init__(self, filename, surface_filter):
        
        
        self.uncompressedFileName = obtain_hdf5_from_l1b(filename)   
        print "uncompressedfilename", self.uncompressedFileName
        dic = read_l1b_hdf5_data(self.uncompressedFileName)
        
        self.simpleFileName = os.path.basename(self.uncompressedFileName)
        tam = len(dic["k_h_geodedic_grid_index"])
            #print tam
        
        
        


            
        self.beans_k_h      = promediados(CONST_K_H_BAND, dic, "k_h_latitude", "k_h_longitude", "ka_h_surface_type", "k_h_antenna_temperature", "k_h_geodedic_grid_index", tam, surface_filter)    
        self.beans_ka_h     = promediados(CONST_KA_H_BAND, dic,"ka_h_latitude", "ka_h_longitude", "ka_h_surface_type", "ka_h_antenna_temperature", "ka_h_geodedic_grid_index", tam, surface_filter)    
        self.beans_ka_v     = promediados(CONST_KA_V_BAND, dic,"ka_v_latitude", "ka_v_longitude", "ka_v_surface_type", "ka_v_antenna_temperature", "ka_v_geodedic_grid_index", tam, surface_filter)    
        self.filename       = filename          
         
    def getSimpleFileName(self):
        return self.simpleFileName  
        
    def getCleanFileName(self):
        return self.getSimpleFileName().split(".")[-2] 
         
    def getbeans_k_h(self):
        return self.beans_k_h
        
    def getbeans_ka_h(self):
        return self.beans_ka_h
        
    def getbeans_ka_v(self):
        return self.beans_ka_v
    
    def getFileName(self):
        return self.filename
        
    def getUncompressedFileName(self):
        return self.uncompressedFileName
        


def processPassFile(pf):
    beans_k_hFinal = []
    beans_ka_hFinal = []
    beans_ka_vFinal = []
    
    bean_k_h = pf.getbeans_k_h()[0]
    bean_ka_h = pf.getbeans_ka_h()[0]
    bean_ka_h = pf.getbeans_ka_v()[0]
    
    
    for i in range(0,8):
        bean_k_h = pf.getbeans_k_h()[i]
        bean_ka_h = pf.getbeans_ka_h()[i]
        bean_ka_v = pf.getbeans_ka_v()[i]
        
        bkhl  = []
        bkahl = []
        bkavl = []
        #Muy ineficiente pero la interseccion no funciono
        for bkh in bean_k_h:
            for bkah in bean_ka_h:
                if bkh.getGG()==bkah.getGG():
                    for bkav in bean_ka_v:
                        if bkah.getGG()==bkav.getGG():
                            bkhl.append(bkh)
                            bkahl.append(bkah)
                            bkavl.append(bkav)

        
        beans_k_hFinal.append(bkhl)
        beans_ka_hFinal.append(bkahl)
        beans_ka_vFinal.append(bkavl)
                            
                            
                    
        
    
    """
    
    #Las intersecciones no funcionaron, busco de hacerlo manual
    for i in range(0,8):
        bean_k_h = pf.getbeans_k_h()[i]
        bean_ka_h = pf.getbeans_ka_h()[i]
        bean_ka_v = pf.getbeans_ka_v()[i]

        #print "values-->", bean_k_h[i].getTbs(), bean_ka_h[i].getTbs(), bean_ka_v[i].getTbs()
        
        bfkh = set(bean_k_h).intersection(bean_ka_h)
        bfkh = bfkh.intersection(bean_ka_v)
        beans_k_hFinal.append(list(bfkh))

        
        
        bfkah = set(bean_ka_h).intersection(bean_k_h)
        bfkah =  bfkah.intersection(bean_ka_v)
        beans_ka_hFinal.append(list(bfkah))
        
        
        bfkav = set(bean_ka_v).intersection(bean_k_h)
        bfkav = bfkav.intersection(bean_ka_h)  
        beans_ka_vFinal.append(list(bfkav))
        
    """    
    #Ahora para cada bean quedan exactamente los mismos elementos
   
    #for i in range(0,8):
    #    for x in range(0, len(beans_ka_hFinal[i])):
    #        print "Valores, beans", i, beans_k_hFinal[i][x].getGG(), beans_ka_hFinal[i][x].getGG(), beans_ka_vFinal[i][x].getGG()
    
    
    
    
    measureListB = MeasureList()
   
    #bean_k_h = beans_k_hFinal[0]
    #bean_ka_h = beans_ka_hFinal[0]
    #print "control 2->", bean_k_h[0].getGG(), bean_ka_h[0].getGG(), bean_k_h[0].getTbs(), bean_ka_h[0].getTbs() 


    
    
    """
    for x in range(0, 8):
        bean_k_h    = beans_k_hFinal[x]
        bean_ka_h   = beans_ka_hFinal[x]       
        bean_ka_v   = beans_ka_vFinal[x]
        mrange = max(len(bean_k_h), len(bean_ka_h), len(bean_ka_v))
        for y in range(0, mrange):
            print "Los 3 gg deberian ser los mismos", bean_k_h[y].getGG(), bean_ka_h[y].getGG(), bean_ka_v[y].getGG()  
            print "Las 3 temperaturas", bean_k_h[y].getTbs(), bean_ka_h[y].getTbs(), bean_ka_v[y].getTbs()  
     """    
    
    beandic = MultiBandBeanDict()
    
    for x in range(0, 8):
        
        bean_k_h    = beans_k_hFinal[x]
        bean_ka_h   = beans_ka_hFinal[x]       
        bean_ka_v   = beans_ka_vFinal[x]
        #print "tamano", len(bean_k_h), len(bean_ka_h), len(bean_ka_v)
        
        
        mrange = max(len(bean_k_h), len(bean_ka_h), len(bean_ka_v))
        
        
        bandbeans = BandBeanList(x)
        for y in range(0, mrange):
            
            #print "values post post-->", bean_k_h[y].getTbs(), bean_ka_h[y].getTbs(), bean_ka_v[y].getTbs()
            #agrupa para una toma todas las bandas.... 
            #print "values-->", bean_k_h[y].getTbs(), bean_ka_h[y].getTbs(), bean_ka_v[y].getTbs()                  
                        
            mb = MultibandBean(bean_k_h[y], bean_ka_h[y], bean_ka_v[y], x, bean_k_h[y].getGG())
                        
            #print mb.getLat(), mb.getLon(), mb.getSic()
            
            #Creo un bean multibanda y lo meto en un lista que solo permite un gg
            bandbeans.add(mb)                        
            measureListB.normal_add(mb)
        
        beandic["Band"+str(x)] = bandbeans
        

    print "Tamano de measure list->", len(measureListB)
     

    # Open an existing file using default properties.

    l1fn = pf.getSimpleFileName()
    l2fn = l1fn.replace("L1B", "L2B")
    print "simpleFileName", l2fn
    mfile = h5py.File("./output/"+l2fn,'w')
    # Open "dset" dataset under the root group.
  
    psics = []

        
    npsics = np.array(psics)
    
    #dataset = mfile.create_dataset("dset",(1, len(sics)), )
    
    dataset = mfile.create_dataset("dset",data=npsics)
    
    
    #print "Dataset dataspace is", dataset.shape
    #print "Dataset Numpy datatype is", dataset.dtype
    #print "Dataset name is", dataset.name
    #print "Dataset is a member of the group", dataset.parent
    #print "Dataset was created in the file", dataset.file    

    mfile.flush()
    mfile.close()
    
    
    #return measureListA
    return measureListB, beandic


if __name__ == "__main__":

    
        
    
    l1b_file = sys.argv[1]   
    #l1b_file = mfile
    print "procesando...", l1b_file
    print l1b_file
    
    #clear = lambda: os.system('cls')
    #clear()   
    
    #os.system("clear")
    
    pf = passfile(l1b_file, [1])
    mlist, beandic = processPassFile(pf)
    
    beandic.saveToFile("test.h5")
    
    
    
    #mlist.drawHk()
    
    
    #SIC, lat, lon, gg, dp, dg, Surface_type 
    
        
    
    print "Clean filename->",pf.getCleanFileName()
    #mlist.drawHkPoles(pf.getCleanFileName()+"L2")
    
    
    
    
    
    #A esta altura ya estan las latitudes mayores y tierra
    
    
    
    #c3 = [filter(lambda x: x in c1, sublist) for sublist in c2]
   
   
   
   
    