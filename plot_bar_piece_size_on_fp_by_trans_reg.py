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
TRANSPORT_REGIME = "S"
FSD = 4.0
condition1 = count_data["flood"] == FLOOD
condition2 =  count_data["fsd"] == FSD

trans_regs = ["S", "U"]
exps_by_trans_reg = [[], []]

for i, trans_reg in enumerate(trans_regs):
    condition3 = count_data["trans_reg"] == trans_reg
    exps_by_trans_reg[i] = count_data.index[condition1 & condition2 & condition3].tolist()

print(exps_by_trans_reg)

#turn exps_by_fsd into a dictionary
dict_of_trials_by_trans_reg = {}

for i, trials_list in enumerate(exps_by_trans_reg):
    dict_of_trials_by_trans_reg[trans_regs[i]] = trials_list

print(dict_of_trials_by_trans_reg)


#now make a df with proportion data (only proportion columns for what you actually want to stack)
proportion_df = pd.DataFrame({
                              "short": (count_data["s_fp_injam"] + count_data["s_fp_ind"])/count_data["all_fp"],
                              "intermediate": (count_data["i_fp_injam"] + count_data["i_fp_ind"])/count_data["all_fp"],
                              "long": (count_data["l_fp_injam"] + count_data["l_fp_ind"])/count_data["all_fp"]
                                })

print(proportion_df)

# Initialize plot
fig, ax = plt.subplots(layout='constrained')
width = 0.8  # Width of each bar
experiment_gap = 1.5  # Gap between experiments

# Colors for consistent stacking across experiments
colors = ['tab:blue', 'tab:orange', 'tab:green']

# Keep track of x positions for bars
x = []
experiment_positions = []
counter = 0

# Loop through each experiment, stacking bars for its trials
for experiment, indices in dict_of_trials_by_trans_reg.items():
    trials = proportion_df.iloc[indices]
    num_trials = len(trials)
    
    # x positions for the trials of this experiment with gap between experiments
    x_positions = np.arange(counter, counter + num_trials)
    x.extend(x_positions)
    
    # Set the label position as the center of the group
    experiment_positions.append(np.mean(x_positions))
    
    # Initialize bottom to stack bars
    bottom = np.zeros(num_trials)
    
    # Stack each value column, maintaining consistent colors
    for i, col in enumerate(proportion_df.columns):
        ax.bar(x_positions, trials[col], width, label=col if counter == 0 else "", bottom=bottom, color=colors[i])
        bottom += trials[col].values
    
    # Add gap between experiments
    counter += num_trials + experiment_gap

# Set the x-ticks at experiment group level
ax.set_xticks(experiment_positions)
ax.set_xticklabels(dict_of_trials_by_trans_reg.keys())

# Labels and title
ax.set_ylabel('Proportion of Pieces on Floodplain')
ax.set_title(f'Size of Pieces on Floodplain vs. Transport Regime for {FSD}x Forest High Floods')
ax.legend(loc='upper right', ncols=3)
plt.show()