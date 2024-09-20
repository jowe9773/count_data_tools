#plotting_count_data.py

#import neccesary packages and modules
from functions import FileFunctions
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

#generate a matrix containing the information you want to put into a heatmap for a single experiment
def make_count_matrix(count_data_all_exps, row_index):
    #input values
    s_in = count_data_all_exps.loc[count_data_all_exps.index[row_index], "s_dropped"]
    i_in = count_data_all_exps.loc[count_data_all_exps.index[row_index], "i_dropped"] 
    l_in = count_data_all_exps.loc[count_data_all_exps.index[row_index], "l_dropped"]
    in_tot = s_in + i_in + l_in

    #floodplain values
    s_fp = count_data_all_exps.loc[count_data_all_exps.index[row_index], "s_fp_injam"] + count_data_all_exps.loc[count_data_all_exps.index[row_index], "s_fp_ind"]
    i_fp = count_data_all_exps.loc[count_data_all_exps.index[row_index], "i_fp_injam"] + count_data_all_exps.loc[count_data_all_exps.index[row_index], "i_fp_ind"]
    l_fp = count_data_all_exps.loc[count_data_all_exps.index[row_index], "l_fp_injam"] + count_data_all_exps.loc[count_data_all_exps.index[row_index], "l_fp_ind"]
    fp_tot = s_fp + i_fp + l_fp

    #channel marginal values
    s_cm = count_data_all_exps.loc[count_data_all_exps.index[row_index], "s_cm_injam"] + count_data_all_exps.loc[count_data_all_exps.index[row_index], "s_cm_ind"]
    i_cm = count_data_all_exps.loc[count_data_all_exps.index[row_index], "i_cm_injam"] + count_data_all_exps.loc[count_data_all_exps.index[row_index], "i_cm_ind"]
    l_cm = count_data_all_exps.loc[count_data_all_exps.index[row_index], "l_cm_injam"] + count_data_all_exps.loc[count_data_all_exps.index[row_index], "l_cm_ind"]
    cm_tot = s_cm + i_cm + l_cm

    #in channel values
    s_ic = count_data_all_exps.loc[count_data_all_exps.index[row_index], "s_ic_injam"] + count_data_all_exps.loc[count_data_all_exps.index[row_index], "s_ic_ind"]
    i_ic = count_data_all_exps.loc[count_data_all_exps.index[row_index], "i_ic_injam"] + count_data_all_exps.loc[count_data_all_exps.index[row_index], "i_ic_ind"]
    l_ic = count_data_all_exps.loc[count_data_all_exps.index[row_index], "l_ic_injam"] + count_data_all_exps.loc[count_data_all_exps.index[row_index], "l_ic_ind"]
    ic_tot = s_ic + i_ic + l_ic

    #values by size
    s_tot = s_fp + s_cm + s_ic
    i_tot = i_fp + i_cm + i_ic
    l_tot = l_fp + l_cm + l_ic
    total = s_tot + i_tot + l_tot

    exp_matrix = np.array([[s_in, i_in, l_in, in_tot],
                        [s_fp, i_fp, l_fp, fp_tot],
                        [s_cm, i_cm, l_cm, cm_tot],
                        [s_ic, i_ic, l_ic, ic_tot],
                        [s_tot, i_tot, l_tot, total]])
    
    return exp_matrix



if __name__ == "__main__":
    #initialize classes
    ff = FileFunctions()

    #choose a count data file
    count_data_fn = ff.load_fn("Select count data file")

    #import count data file
    count_data = pd.read_csv(count_data_fn)
    row_index = 0

    #plot a single experiment as a heatmap
    exp_matrix = make_count_matrix(count_data, row_index)


    plt.imshow(exp_matrix, cmap='hot', interpolation='nearest')
    plt.title('Heatmap Example')
    plt.colorbar()  # Adds a color bar
    plt.show()
