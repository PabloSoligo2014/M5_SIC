import sys
import os

import tarfile
import numpy as np
import h5py



from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

from Bean import Bean
from hd5fileManager import hd5fileManager
#import Measure
from MeasureList import MeasureList


from MultiBandBeanDict import MultiBandBeanDict

from BandBeanList import BandBeanList
from MultibandBean import MultibandBean
#from HD5FileList import HD5FileList



#import gdal

#import numpy as np

#basemap

#Calibrar: 1 sea / 5 posible hielo
#L2 1,5 3

#Surface -1 unknow, 0=land 1=ocean 2=coast 3=near coast 4=ice 5=possible Ice


CONST_K_H_BAND  =  "k_h"
CONST_KA_H_BAND =  "ka_h" 
CONST_KA_V_BAND =  "ka_v" 
  
    
    
       
        
        

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
                
                #print "mySet TBS", dic[value][i][n_bean]
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
            tbsAcu = 0
            cont = 0
            surfacef = None            
            while (indexActual==indexAnterior)and(i<len(filtrados)-1):
                tbsAcu = tbsAcu + filtrados[i].getTbs()
                cont = cont + 1
                i = i + 1
                indexActual = filtrados[i].gg_index
                
                if (surface in (1,5)) and (filtrados[i].surface==3):
                    surfacef = filtrados[i].surface #3 tiene precedencia
                    
            
            indexAnterior = indexActual            
            promediado = Bean()
            
            promediado.setTbs(tbsAcu/cont)
            
            promediado.lat        = filtrados[i-1].getLat()
            promediado.lon        = filtrados[i-1].getLon()
            promediado.gg_index   = filtrados[i-1].getGG()
            promediado.band       = filtrados[i-1].band
            promediado.bean       = filtrados[i-1].bean
            if surfacef!=None:
                promediado.surface    = surfacef # filtrados[i-1].surface 
            else:
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
    
    bean_k_h    = pf.getbeans_k_h()[0]
    bean_ka_h   = pf.getbeans_ka_h()[0]
    bean_ka_h   = pf.getbeans_ka_v()[0]
    
    
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
    
    measureListB = MeasureList()
   
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
                        
            mb = MultibandBean(bean_k_h[y], bean_ka_h[y], bean_ka_v[y], x, bean_k_h[y].getGG(), bean_k_h[y].getSurface())
                        
            #print mb.getLat(), mb.getLon(), mb.getSic()
            
            #Creo un bean multibanda y lo meto en un lista que solo permite un gg
            bandbeans.add(mb)                        
            measureListB.normal_add(mb)
            #measureListB.unique_add(mb)
        beandic["Bean"+str(x)] = bandbeans
        

    #print "Tamano de measure list->", len(measureListB)
     
    return measureListB, beandic


if __name__ == "__main__":
   
    #EO_20130430_190916_CUSS_SACD_MWR_L1B_SCI_099_000_004.tar.gz EO_20130430_173128_CUSS_SACD_MWR_L1B_SCI_003_000_004.tar.gz EO_20130424_144718_CUSS_SACD_MWR_L1B_SCI_015_000_004.tar.gz
   
    l1b_file = sys.argv[1]   
    
    if not os.path.exists("./output/"):
        os.makedirs("./output/") 
    
    if not os.path.exists("./tmp/"):
        os.makedirs("./tmp/") 
    
    #si el parametro segundo es -f trabaja por folder, sino modo tradicional
    if len(sys.argv)<2:
        print "Faltan argumentos"
    else:
        if sys.argv[1]=="-f":
            #Vamos por folder
            folder = sys.argv[2] #"./MWR_pasadas/"
            for fs in os.listdir(folder):        
                if fs.endswith("tar.gz") and fs.startswith("EO"):
                    l1b_file = fs  
                    print "procesando...", l1b_file
                    print l1b_file
                  
                    #Surface -1 unknow, 0=land 1=ocean 2=coast 3=near coast 4=ice 5=possible Ice
                    pf = passfile(l1b_file, [1,3,5])
                    mlist, beandic = processPassFile(pf)
                    l1fn = pf.getSimpleFileName()
                    l2fn = l1fn.replace("L1B", "L2B")
                    h5f = hd5fileManager("./output/", l2fn ,mlist, beandic)
                    #Con true elimina los archivos ya comprimidos
                    h5f.save(True)
                    
                    
        else:
            #vamos por archivo
            l1b_file = sys.argv[1]   
            print "procesando...", l1b_file
            print l1b_file
            
            os.system("clear")
            #Surface -1 unknow, 0=land 1=ocean 2=coast 3=near coast 4=ice 5=possible Ice
            pf = passfile(l1b_file, [1,3,5])
            mlist, beandic = processPassFile(pf)
            l1fn = pf.getSimpleFileName()
            l2fn = l1fn.replace("L1B", "L2B")
            h5f = hd5fileManager("./output/", l2fn ,mlist, beandic)
            h5f.save(True)
            
           
            
            

        
        
        
    print "Proceso finalizado"
        
    