import os
import sys

import mwr_l2_processor
import matplotlib.pyplot as plt
import os

from HD5FileList import HD5FileList
import tarfile






if __name__ == "__main__":
    
    
    #l1b_directory = sys.argv[1]
    #l1b_files = get_l1b_products_in_folder(l1b_directory)
    
    if not os.path.exists("./p3output/"):
        os.makedirs("./p3output/")   
        
    if not os.path.exists("./p2output/"):
        os.makedirs("./p2output/")    
    
    folder = sys.argv[1]   
    
    filelist = []
    
    #Descomprimo todo
    for fs in os.listdir(folder):        
        if fs.endswith("tar.gz") and fs.startswith("EO"):
            l2b_file = fs   
            #print "tratando de abrir:"+l2b_file
            tar = tarfile.open("./output/"+l2b_file)
            tar.extractall(path="./output/",members=None)
            #archivos = tar.getnames()        
            tar.close()
        
     
    firstFileName = None
    for fs in os.listdir(folder):
        if fs.endswith("h5"):
            filelist.append(fs)
            if firstFileName==None:
                firstFileName = fs
            
        
   
   
    fm = HD5FileList(folder, filelist)
    
    fm.saveToFile("./p2output/dgdp.txt") 
    
    #fm.drawPointsHistograms2()
    fm.drawTiePointsHistograms()
    fm.drawWholeSouthMap(True, "./p3output/")
    fm.drawWholeNorthMap(True, "./p3output/")
    
    #EOyyyymmddL3
    filename = "./p3output/"+"EO"+firstFileName[2:11]+"L3.h5"
   
    fm.saveH5L3(filename)
    
    
    
    
    """    
    dp, dg, sic = obtain_deltas(l1b_files)
    dp_odd, dg_odd, dp_even, dg_even = concat_data(dp, dg)
    print_tie_points(dp_odd, dg_odd)
    plot_histogram(dp_odd, dg_odd, "Odd beams")
    print_tie_points(dg_even, dg_even)
    plot_histogram(dp_even, dg_even, "Even beams")
    """


