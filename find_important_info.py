#plot_bar_charts_simple.py

#import neccesary packages and modules
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from functions import FileFunctions, CountDataFunctions, PlotCountData

#initialize classes
ff = FileFunctions()
cdf = CountDataFunctions()
pcd = PlotCountData()

#choose a count data file
count_data_fn = ff.load_fn("Select count data file")

count_data = pd.read_csv(count_data_fn)
print(count_data)

#Choose parameters you would like to remain the same across all experiments that you will plot (comment out the parameter you would like to change):
FLOOD = "H"
TRANSPORT_REGIME = "U"
FSD = 1.0
condition1 = count_data["flood"] == FLOOD
condition2 =  count_data["trans_reg"] == TRANSPORT_REGIME

fsds = [0.5, 1.0, 2.0, 4.0]
exps_by_fsd = [[], [], [], []]

for i, fsd in enumerate(fsds):
    condition3 = count_data["fsd"] == fsd
    exps_by_fsd[i] = count_data.index[condition1 & condition2 & condition3].tolist()

print(exps_by_fsd)

#turn exps_by_fsd into a dictionary
dict_of_trials_by_fsd = {}

for i, trials_list in enumerate(exps_by_fsd):
    dict_of_trials_by_fsd[f"{fsds[i]}"] = trials_list

print(dict_of_trials_by_fsd)

#now make a df with proportion data (only proportion columns for what you actually want to stack)
proportion_df = pd.DataFrame({
                              "fp": count_data["all_fp"]/count_data["all_pieces"],
                              "cm": count_data["all_cm"]/count_data["all_pieces"],
                              "ic": count_data["all_ic"]/count_data["all_pieces"],
                              "all_pieces_in_flume": count_data["all_pieces"]/count_data["all_dropped"]
                                })

print(proportion_df)

# Calculate and print row averages for each FSD group
column_names_to_average = ["fp", "cm", "ic", "all_pieces_in_flume"]  # replace with your column names

averages_by_fsd = {}

for i, trials_list in enumerate(exps_by_fsd):
    if trials_list:
        # Select rows corresponding to trials_list
        group_data = proportion_df.loc[trials_list, column_names_to_average]
        # Calculate mean for each column
        averages = group_data.mean()
        averages_by_fsd[f"{fsds[i]}"] = averages
        print(f"Averages for FSD {fsds[i]}:\n{averages}\n")

# You can now use averages_by_fsd for further processing or plotting