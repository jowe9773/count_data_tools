#plot_bar_charts_simple.py

#import neccesary packages and modules
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint 
import pandas as pd
from functions import FileFunctions, CountDataFunctions, PlotCountData

#initialize classes
ff = FileFunctions()
cdf = CountDataFunctions()
pcd = PlotCountData()

plt.rcParams.update({
    'font.size': 18,  # General font size
    'axes.titlesize': 20,  # Title font size
    'axes.labelsize': 18,  # Axis label font size
    'xtick.labelsize': 16,  # X-tick label font size
    'ytick.labelsize': 16,  # Y-tick label font size
    'legend.fontsize': 16,  # Legend font size
})

#choose a count data file
jam_count_data_fn = ff.load_fn("Select count data file")

count_data = pd.read_csv(jam_count_data_fn)
print(count_data)

#Choose parameters you would like to remain the same across all experiments that you will plot (comment out the parameter you would like to change):
FLOOD = "H"
TRANSPORT_REGIME = "U"

condition1 = count_data["flood"] == FLOOD
condition2 = count_data["trans_reg"] == TRANSPORT_REGIME

# Define fsd values
fsds = [0.5, 1.0, 2.0, 4.0]

# Dictionary to store trials and indices by experiment type
trials_by_exp_type = {}
indices_by_exp_type = {}

for i, fsd in enumerate(fsds):
    condition3 = count_data["fsd"] == fsd
    
    # Find trials that meet the conditions
    trials = count_data["exp_name"][condition1 & condition2 & condition3].unique().tolist()
    print(trials)
    
    # Store trials by experiment type
    trials_by_exp_type[f"{fsd}"] = trials
    
    # Initialize the nested dictionary for the current `fsd`
    indices_by_exp_type[f"{fsd}"] = {}
    
    # Loop over each trial and find corresponding row indices
    for trial in trials:
        trial_condition = count_data["exp_name"] == trial
        indices = count_data.index[condition1 & condition2 & condition3 & trial_condition].tolist()
        
        # Store the indices for the specific trial under the current `fsd`
        indices_by_exp_type[f"{fsd}"][trial] = indices

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


# Keep track of x positions for bars
x = []
experiment_positions = []
counter = 0

# Color maps for different FSDs (for the bars)
fsd_colors = {
    '0.5': plt.cm.Blues,
    '1.0': plt.cm.Oranges,
    '2.0': plt.cm.Greens,
    '4.0': plt.cm.Purples,
}

# Grayscale map for the legend
legend_colors = plt.cm.Greys(np.linspace(0.2, 0.8, len(proportion_df.columns)))

# Keep track of x positions for bars
x = []
experiment_positions = []
counter = 0

# Loop through each FSD group
for fsd, experiments in indices_by_exp_type.items():
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
        
        # Get the color map for the current fsd (for the bars)
        colors = fsd_colors[fsd](np.linspace(0.2, 0.8, len(proportion_df.columns)))
        
        # Stack each value column
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
ax.set_title('Proportion of Total Pieces Dropped by FSD and Experiment')

# Custom legend (grayscale)
legend_handles = [
    plt.Line2D([0], [0], color=legend_colors[i], lw=4, label=col)
    for i, col in enumerate(proportion_df.columns)
]

ax.legend(handles=legend_handles, loc='upper left', ncols=3)

# Add grid for better visualization
ax.grid(True, axis='y', linestyle='--', alpha=0.7)

ax.invert_xaxis()

# Show plot
plt.tight_layout()
plt.show()

