import numpy as np


def print_tie_points(delta_P, delta_G):
    """Prints three candidates for Tie Points for the ICE and the SEA.

    Parameters
    ----------
    delta_P : np.array
    delta_G : np.array

    """
    """
    ICE. counts = 1.0 p = 78.8 g = -40.0
    ICE. counts = 1.0 p = 82.0 g = -38.4
    ICE. counts = 1.0 p = 82.0 g = -32.0
    
    SEA. counts = 0.0 p = 10.0 g = -8.0
    SEA. counts = 0.0 p = 10.0 g = -8.0
    SEA. counts = 0.0 p = 10.0 g = -8.0
    """    
    
    DIM_PR = 50
    DIM_GR = 50

    PR_MIN = 10
    PR_MAX = 90
    GR_MIN = -40
    GR_MAX = 40

    DELTA_PR  = (PR_MAX - PR_MIN) / float(DIM_PR)
    DELTA_GR  = (GR_MAX - GR_MIN) / float(DIM_GR)

    PR_0 = 40 # threshold to separate ice and ocean
    iPR = int(round((PR_0 - PR_MIN) / DELTA_PR) + 1)

    
    iceCount    = 0
    IceP        = 0
    iceG        = 0
    seaCount    = 0
    SeaP        = 0 
    seaG        = 0     
    
    hist = np.zeros((DIM_PR,DIM_GR))
    for i in xrange(len(delta_P)):
        if delta_P[i] < PR_MIN or delta_P[i] > PR_MAX:
            continue
        if delta_G[i] < GR_MIN or delta_G[i] > GR_MAX:
            continue
        r = int((delta_G[i]-GR_MIN) / DELTA_GR)
        c = int((delta_P[i]-PR_MIN) / DELTA_PR)
        hist[r, c] += 1


    maxicecount = 0
    maxseacount = 0
    maxiceg = 0
    maxseag = 0
    maxicep = 0
    maxseap = 0
    
    for i in range(3):
        ice = hist[:,:iPR]
        (j , k) = np.where(ice == np.max(ice))
        j = j[0]
        k = k[0]
        print "ICE. counts =", np.max(ice),
        iceCount = np.max(ice) 
        iceP = j * DELTA_PR + PR_MIN
        iceG = k * DELTA_GR + GR_MIN
        
        
        if iceCount>maxicecount:
            maxicecount=iceCount
            maxicep = iceP
            maxiceg = iceG
        print "p =", iceP, "g =", iceG
        hist[j,k] = 0
    
    for i in range(3):
        sea = hist[:,iPR:]
        (j , k) = np.where(sea == np.max(sea))
        j = j[0]
        k = k[0]
        seaCount = np.max(sea)
        seaP     = (j) * DELTA_PR + PR_MIN       
        seaG     = (k+iPR) * DELTA_GR + GR_MIN
        
        if seaCount>maxseacount:
            maxseacount = seaCount
            maxseap = seaP
            maxseag = seaG
            
        print "SEA. counts =", seaCount, 
        print "p =", seaP , "g =", seaG
        hist[j,k+iPR] = 0

    return maxicecount, maxicep, maxiceg, maxseacount, maxseap, maxseag    
    