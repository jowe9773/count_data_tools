#plot_bar_charts_simple.py

#import neccesary packages and modules
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint 
import pandas as pd
from functions import FileFunctions, CountDataFunctions, PlotCountData


# Update font sizes globally
plt.rcParams.update({
    'font.size': 24,  # General font size
    'axes.titlesize': 26,  # Title font size
    'axes.labelsize': 24,  # Axis label font size
    'xtick.labelsize': 22,  # X-tick label font size
    'ytick.labelsize': 22,  # Y-tick label font size
    'legend.fontsize': 22,  # Legend font size
})

#initialize classes
ff = FileFunctions()
cdf = CountDataFunctions()
pcd = PlotCountData()

#choose a count data file
jam_count_data_fn = ff.load_fn("Select count data file")

count_data = pd.read_csv(jam_count_data_fn)
print(count_data)

#Choose parameters you would like to remain the same across all experiments that you will plot (comment out the parameter you would like to change):
FLOOD = "H"
FSD = 1.0

condition1 = count_data["flood"] == FLOOD
condition2 = count_data["fsd"] == FSD

# Define fsd values
trans_regs = ["U", "S"]

# Dictionary to store trials and indices by experiment type
trials_by_exp_type = {}
indices_by_exp_type = {}

for i, trans_reg in enumerate(trans_regs):
    condition3 = count_data["trans_reg"] == trans_reg
    
    # Find trials that meet the conditions
    trials = count_data["exp_name"][condition1 & condition2 & condition3].unique().tolist()
    print(trials)
    
    # Store trials by experiment type
    trials_by_exp_type[f"{trans_reg}"] = trials
    
    # Initialize the nested dictionary for the current `fsd`
    indices_by_exp_type[f"{trans_reg}"] = {}
    
    # Loop over each trial and find corresponding row indices
    for trial in trials:
        trial_condition = count_data["exp_name"] == trial
        indices = count_data.index[condition1 & condition2 & condition3 & trial_condition].tolist()
        
        # Store the indices for the specific trial under the current `fsd`
        indices_by_exp_type[f"{trans_reg}"][trial] = indices

# Pretty print the trials and nested indices

pprint(indices_by_exp_type)



#now make a df with proportion data (only proportion columns for what you actually want to stack)
proportion_df = pd.DataFrame({
                              "floodplain": count_data["all_fp"]/880,
                              "channel_marginal": count_data["all_cm"]/880,
                              "in_channel": count_data["all_ic"]/880
                                })

print(proportion_df)



# Initialize plot
fig, ax = plt.subplots(layout='constrained', figsize=(12, 6))
width = 0.8  # Width of each bar
experiment_gap = 1.5  # Gap between experiments
fsd_gap = 3  # Gap between FSD groups

# Color maps for different FSDs
fsd_colors = {
    'U': plt.cm.Blues,
    'S': plt.cm.Oranges,

}

# Keep track of x positions for bars
x = []
experiment_positions = []
counter = 0

# Loop through each FSD group
for fsd, experiments in indices_by_exp_type.items():
    # For each FSD, loop through the experiments
    for experiment, indices in experiments.items():
        # Extract data for the given indices (jams)
        trials = proportion_df.iloc[indices]
        num_trials = len(trials)
        
        # x positions for the trials (jams) of this experiment with gap between experiments
        x_positions = np.arange(counter, counter + num_trials)
        x.extend(x_positions)
        
        # Set the label position as the center of the group
        experiment_positions.append(np.mean(x_positions))
        
        # Initialize bottom to stack bars
        bottom = np.zeros(num_trials)
        
        # Get the color map for the current fsd
        colors = fsd_colors[fsd](np.linspace(0.2, 0.8, len(proportion_df.columns)))
        
        # Stack each value column (e.g., small, medium, large pieces)
        for i, col in enumerate(proportion_df.columns):
            ax.bar(x_positions, trials[col], width, label=col if counter == 0 else "", bottom=bottom, color=colors[i])
            bottom += trials[col].values
        
        # Add gap between experiments
        counter += num_trials + experiment_gap

    # Add additional gap between FSD groups
    counter += fsd_gap

# Set the x-ticks at experiment group level
ax.set_xticks(experiment_positions)
ax.set_xticklabels([f"{fsd}: {exp}" for fsd, exps in indices_by_exp_type.items() for exp in exps.keys()], rotation=45, ha='right')

# Labels and title
ax.set_ylabel('Proportion of Total Pieces Dropped')
ax.set_title('Proportion of Total Pieces Dropped by Jam, FSD, and Experiment')

# Add legend
ax.legend(loc='upper left', ncols=3)

# Add grid for better visualization
ax.grid(True, axis='y', linestyle='--', alpha=0.7)

ax.invert_xaxis()

# Show plot
plt.tight_layout()
plt.show()