#functions.py

#import neccesary packages and modules
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
import os


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
    
    def find_files_with_name(root_folder, substring):
        matching_files = []
        
        # Walk through the directory structure
        for dirpath, dirnames, filenames in os.walk(root_folder):
            # Check if the target substring is in any of the filenames
            for filename in filenames:
                if substring in filename:
                    # Append the full path of the matching file
                    matching_files.append(os.path.join(dirpath, filename))
        
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
        experiment = exps_deets[exps_deets["Experiment Name"] == exp_name]
        flood = experiment.iloc[0]["Flood type"]
        trans_reg = experiment.iloc[0]["Congestion"]
        fsd = experiment.iloc[0]["Forest Stand Density"]        #grab experiment setup details from experiment summary table
        
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

        if flood == "L":
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