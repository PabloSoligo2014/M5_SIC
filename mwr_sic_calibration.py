import os
import sys

import mwr_l2_processor
import matplotlib.pyplot as plt


def get_l1b_products_in_folder(l1b_directory):
    """Get the list of all the L1B products (.tar.gz) in a directory

    Parameters
    ----------
    l1b_directory : string
        directory path containing L1B products

    Returns
    -------
    list of strings
        The file paths found
    """
    return ""


def obtain_deltas(l1b_files):
    """ Generates a structure containing all the DP and DG for all the passes

    Parameters
    ----------
    l1b_files : list of tar.gz file paths 
        the L1B product paths

    Returns
    -------
    dp : dict (or list)
    dg : dict (or list)
    sic : dict (or list)
    """
    return {}, {}, {}


def concat_data(dp, dg):
    """ Concatenates all the data in dp and dg variables.

    Parameters
    ----------
    dp : tar.gz file path
        the L1B product path

    Returns
    -------
    dp_odd : np.array
        DP values for all the passes for odd beams
    dg_odd : np.array
        DG values for all the passes for odd beams
    dp_even : np.array
        DP values for all the passes for even beams
    dg_even : np.array
        DG values for all the passes for even beams
    """
    return [], [], [], []


def plot_histogram(x, y, title):
    """ Plots a 2d histogram
    """
    print "plotting", title, "histogram"
    plt.hist2d(x, y, bins=500)
    plt.title(title)
    plt.show()


if __name__ == "__main__":
    
    
    l1b_directory = sys.argv[1]
    l1b_files = get_l1b_products_in_folder(l1b_directory)
    
    """    
    dp, dg, sic = obtain_deltas(l1b_files)
    dp_odd, dg_odd, dp_even, dg_even = concat_data(dp, dg)
    print_tie_points(dp_odd, dg_odd)
    plot_histogram(dp_odd, dg_odd, "Odd beams")
    print_tie_points(dg_even, dg_even)
    plot_histogram(dp_even, dg_even, "Even beams")
    """


