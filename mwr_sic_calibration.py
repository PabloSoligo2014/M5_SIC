import os
import sys

import mwr_l2_processor
import matplotlib.pyplot as plt
import os

from HD5FileList import HD5FileList






if __name__ == "__main__":
    
    
    #l1b_directory = sys.argv[1]
    #l1b_files = get_l1b_products_in_folder(l1b_directory)
    
    folder = sys.argv[1]   
    
    filelist = []
    #for fi in range(1, len(sys.argv)):
    #    filelist.append(sys.argv[fi])
     
    
    for fs in os.listdir(folder):
        if fs.endswith("h5"):
            filelist.append(fs)
        
    #print filelist
   
    fm = HD5FileList(folder, filelist)
    fm.saveToFile("dgdp.txt") 
    #fm.drawWholeMap()
    #fm.drawPointsHistograms2()    
    fm.drawTiePointsHistograms()
    #fm.drawWholeSouthMap()
    #fm.drawWholeNorthMap()
    
    
    
    
    
    """    
    dp, dg, sic = obtain_deltas(l1b_files)
    dp_odd, dg_odd, dp_even, dg_even = concat_data(dp, dg)
    print_tie_points(dp_odd, dg_odd)
    plot_histogram(dp_odd, dg_odd, "Odd beams")
    print_tie_points(dg_even, dg_even)
    plot_histogram(dp_even, dg_even, "Even beams")
    """


