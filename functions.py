#functions.py

#import neccesary packages and modules
import tkinter as tk
from tkinter import filedialog
import pandas as pd


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

class CountDataFunctions:
    def __init__(self):
        print("Initialized CountDataFunctions")

    def load_jam_level_data(self, filename, summary_table):
        "function to load in jam level data from an experiment"

        #start by making what will be the output dataframe
        output_df = pd.DataFrame(columns = ["exp_name", "flood", "trans_reg", "fsd", "jam_num",
                                            
                                            "s_fp", "i_fp", "l_fp", "fp_tot",
                                            "s_cm", "i_cm", "l_cm", "cm_tot",
                                            "s_ic", "i_ic", "l_ic", "ic_tot",
                                            "s_tot", "i_tot", "l_tot", "total"])

        return output_df
    
    def load_exp_level_data(self, filename, summary_table):
        "function to load in experiment level data (experiment totals)"

        #start by making what will be the output dataframe
        output_df = pd.DataFrame(columns = ["exp_name", "flood", "trans_reg", "fsd",
                                            
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

        return output_df