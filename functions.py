#functions.py

#import neccesary packages and modules
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt
from matplotlib import gridspec



class FileFunctions:
    """Class contains methods for managing files"""

    def __init__(self):
        print("Initialized file managers")

    def load_dn(self, purpose):
        """this function opens a tkinter GUI for selecting a 
        directory and returns the full path to the directory 
        once selected
        
        'purpose' -- provides expanatory text in the GUI
        that tells the user what directory to select"""

        root = tk.Tk()
        root.withdraw()
        directory_name = filedialog.askdirectory(title = purpose)

        return directory_name

    def load_fn(self, purpose):
        """this function opens a tkinter GUI for selecting a 
        file and returns the full path to the file 
        once selected
        
        'purpose' -- provides expanatory text in the GUI
        that tells the user what file to select"""

        root = tk.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename(title = purpose)

        return filename
    
    def find_files_with_name(self, root_folder, substring):
        matching_files = []
        
        # Walk through the directory structure
        for dirpath, dirnames, filenames in os.walk(root_folder):
            # Check if the target substring is in any of the filenames
            for filename in filenames:
                if substring in filename:
                    # Append the full path of the matching file
                    full_path = Path(os.path.join(dirpath, filename)).as_posix()
                    matching_files.append(full_path)
        
        return matching_files

class CountDataFunctions:
    def __init__(self):
        print("Initialized CountDataFunctions")
    
    def load_exp_level_data(self, filename, exps_summary):
        "function to load in experiment level data (experiment totals)"

        #establish experiment name, flood type, transport regime, and forest stand density for the experiment
        fn_info = filename.split("/")[-1].split("_")
        exp_name = fn_info[0] + "_" + fn_info[1]                #grab experiment name from filename

        exps_deets = pd.read_excel(exps_summary)

        #check to see if experiment name is in experiment deets
        if exps_deets["Experiment Name"].isin([exp_name]).any():
            experiment = exps_deets[exps_deets["Experiment Name"] == exp_name]
            flood = experiment.iloc[0]["Flood type"]
            trans_reg = experiment.iloc[0]["Congestion"]
            fsd = experiment.iloc[0]["Forest Stand Density"]        #grab experiment setup details from experiment summary table
            print(exp_name + ": ", fsd, flood, trans_reg)

        else:
            print (f"Experiment name {exp_name} not in experiments summary file")
            return

        if flood == "A":
            print(f"Experiment {exp_name} is an autochthonous experiment and has no count data")
            return
        
        if flood == "x":
            print(f"Experiment {exp_name} is an 'x' experiment and has no count data")
            return
        
        # read file for experiment containing the cart data
        exp = pd.read_excel(filename, sheet_name="Summary")
  
        #handle count data differences between high and low flows due to remobilization
        if flood == "H":
            all_s = exp.iat[11,2] + exp.iat[6,2]
            all_i = exp.iat[11,3] + exp.iat[6,3]
            all_l = exp.iat[11,4] + exp.iat[6,4]
            all_pieces = all_s + all_i + all_l

            remobilized_s = np.nan
            remobilized_i = np.nan
            remobilized_l = np.nan
            remobilized_total = np.nan

        elif flood == "L":
            remobilized_s = exp.iat[16,2]
            remobilized_i = exp.iat[16,3]
            remobilized_l = exp.iat[16,4]
            remobilized_total = exp.iat[16,5]

            all_s = exp.iat[11,2] + exp.iat[6,2] + remobilized_s
            all_i = exp.iat[11,3] + exp.iat[6,3] + remobilized_i
            all_l = exp.iat[11,4] + exp.iat[6,4] + remobilized_l
            all_pieces = all_s + all_i + all_l

        output_data = pd.DataFrame([[exp_name, flood, trans_reg, fsd,
                                            
                                    exp.iat[1,2], exp.iat[1,3], exp.iat[1,4], exp.iat[1,5],

                                    exp.iat[3,2], exp.iat[3,3], exp.iat[3,4], exp.iat[3,5],
                                    exp.iat[4,2], exp.iat[4,3], exp.iat[4,4], exp.iat[4,5],
                                    exp.iat[5,2], exp.iat[5,3], exp.iat[5,4], exp.iat[5,5],
                                    exp.iat[6,2], exp.iat[6,3], exp.iat[6,4], exp.iat[6,5],

                                    exp.iat[8,2], exp.iat[8,3], exp.iat[8,4], exp.iat[8,5],
                                    exp.iat[9,2], exp.iat[9,3], exp.iat[9,4], exp.iat[9,5],
                                    exp.iat[10,2], exp.iat[10,3], exp.iat[10,4], exp.iat[10,5],
                                    exp.iat[11,2], exp.iat[11,3], exp.iat[11,4], exp.iat[11,5],

                                    all_s, all_i, all_l, all_pieces,
                                    exp.iat[3,5] + exp.iat[8,5], exp.iat[4,5] + exp.iat[9,5], exp.iat[5,5] + exp.iat[10,5],

                                    remobilized_s, remobilized_i, remobilized_l, remobilized_total]],
                        columns = ["exp_name", "flood", "trans_reg", "fsd",
                                            
                                    "s_dropped", "i_dropped", "l_dropped", "all_dropped",

                                    "s_fp_injam", "i_fp_injam", "l_fp_injam", "all_fp_injam",
                                    "s_cm_injam", "i_cm_injam", "l_cm_injam", "all_cm_injam",
                                    "s_ic_injam", "i_ic_injam", "l_ic_injam", "all_ic_injam",
                                    "s_tot_injam", "i_tot_injam", "l_tot_injam", "all_injam",

                                    "s_fp_ind", "i_fp_ind", "l_fp_ind", "all_fp_ind",
                                    "s_cm_ind", "i_cm_ind", "l_cm_ind", "all_cm_ind",
                                    "s_ic_ind", "i_ic_ind", "l_ic_ind", "all_ic_ind",
                                    "s_tot_ind", "i_tot_ind", "l_tot_ind", "all_ind",

                                    "all_s", "all_i", "all_l", "all_pieces",
                                    "all_fp", "all_cm", "all_ic",

                                    "remobilized_s", "remobilized_i", "remobilized_l", "remobilized_total"])

        return output_data
    
class PlotCountData:
    def __init__(self):
        print('Initialized PlotCountData')
    
    def make_count_matrix(self, count_data_all_exps, row_index):
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

        exp_matrix = np.array([[s_fp, i_fp, l_fp, fp_tot],
                            [s_cm, i_cm, l_cm, cm_tot],
                            [s_ic, i_ic, l_ic, ic_tot],
                            [s_tot, i_tot, l_tot, total]])
        
        return exp_matrix

    def make_proportion_matrix(self):
        return

    def plot_heatmaps(self, experiments):
        # Custom word labels for the x and y axes
        x_labels = ["S", "I ", "L ", "T"]
        y_labels = ["FP", "CM", "IC", "TOT"]

        # Determine the maximum number of trials across all experiment types
        max_trials = max(len(trials) for trials in experiments.values())
        n_cols = len(experiments)  # Number of experiment types

        # Create a gridspec layout with extra space for the colorbar
        fig = plt.figure(figsize=(15, 10))
        gs = gridspec.GridSpec(max_trials, n_cols + 1, width_ratios=[1] * n_cols + [0.05])  # Extra column for colorbar

        # Find global min and max values across all experiments for consistent color scaling
        vmin = min([np.min(heatmap) for heatmaps in experiments.values() for heatmap in heatmaps])
        vmax = max([np.max(heatmap) for heatmaps in experiments.values() for heatmap in heatmaps])

        # Plot each heatmap in its corresponding row (trial) and column (experiment type)
        # Plot each heatmap in its corresponding row (trial) and column (experiment type)
        axes = []
        for col, (exp_type, heatmaps) in enumerate(experiments.items()):
            for row in range(max_trials):
                if row < len(heatmaps):  # Check if there is a heatmap for this trial
                    ax = plt.subplot(gs[row, col])
                    im = ax.imshow(heatmaps[row], cmap='coolwarm', vmin=vmin, vmax=vmax)
                    
                    # Set custom x and y labels using words
                    ax.set_xticks(range(len(x_labels)))
                    ax.set_xticklabels(x_labels, rotation=45, ha="right")  # Rotate for better readability
                    ax.set_yticks(range(len(y_labels)))
                    ax.set_yticklabels(y_labels)

                else:
                    # Create an empty subplot if no data exists for this row (trial)
                    ax = plt.subplot(gs[row, col])
                    ax.axis('off')  # Turn off the axis for empty plots

                if row == 0:
                    ax.set_title(exp_type)  # Set title for each column
                if col == 0 and row < len(heatmaps):
                    ax.set_ylabel(f'Trial {row + 1}')  # Label for each trial row
                axes.append(ax)

        # Create the colorbar in the extra column (last column of the gridspec)
        cbar_ax = plt.subplot(gs[:, -1])  # Use the entire last column for the colorbar
        fig.colorbar(im, cax=cbar_ax)

        # Adjust layout to avoid overlapping
        plt.tight_layout()
        plt.show()