import numpy as np


def print_tie_points(delta_P, delta_G):
    """Prints three candidates for Tie Points for the ICE and the SEA.

    Parameters
    ----------
    delta_P : np.array
    delta_G : np.array

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


    hist = np.zeros((DIM_PR,DIM_GR))
    for i in xrange(len(delta_P)):
        if delta_P[i] < PR_MIN or delta_P[i] > PR_MAX:
            continue
        if delta_G[i] < GR_MIN or delta_G[i] > GR_MAX:
            continue
        r = int((delta_G[i]-GR_MIN) / DELTA_GR)
        c = int((delta_P[i]-PR_MIN) / DELTA_PR)
        hist[r, c] += 1


    for i in range(3):
        ice = hist[:,:iPR]
        (j , k) = np.where(ice == np.max(ice))
        j = j[0]
        k = k[0]
        print "ICE. counts =", np.max(ice), 
        print "p =", j * DELTA_PR + PR_MIN, "g =", k * DELTA_GR + GR_MIN
        hist[j,k] = 0
    
    for i in range(3):
        sea = hist[:,iPR:]
        (j , k) = np.where(sea == np.max(sea))
        j = j[0]
        k = k[0]
        print "SEA. counts =", np.max(sea), 
        print "p =", (j) * DELTA_PR + PR_MIN, "g =", (k+iPR) * DELTA_GR + GR_MIN
        hist[j,k+iPR] = 0
