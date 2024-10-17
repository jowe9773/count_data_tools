#import necessary packages and modules
import matplotlib.pyplot as plt
from pprint import pprint 
import pandas as pd
from functions import FileFunctions, CountDataFunctions, PlotCountData

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
FSD = 2.0

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

# Initialize the plot
fig, ax = plt.subplots(figsize=(12, 6))

# Define colors for each FSD
fsd_colors = {
    'U': 'tab:blue',
    'S': 'tab:orange',
}

# Initialize an offset value to separate points from different experiments
experiment_offset = 0.1  # Adjust this value for spacing between experiments

# Create a mapping for x positions based on FSD
fsd_positions = {fsd: idx for idx, fsd in enumerate(fsd_colors.keys())}

# Loop through each FSD group
for fsd, experiments in indices_by_exp_type.items():
    # Initialize a counter for x positions
    x_positions = []

    # Loop through the experiments within the current FSD
    for i, (experiment, indices) in enumerate(experiments.items()):
        # Extract the jam sizes for the given indices
        jam_sizes = count_data['all'].iloc[indices]  # Replace 'all' with the correct column name for jam sizes

        # Calculate x positions with an offset for this experiment
        x_pos = [fsd_positions[fsd] + (i - len(experiments) / 2) * experiment_offset] * len(jam_sizes)
        x_positions.extend(x_pos)

        # Plot the jam sizes as scatter points
        ax.scatter(
            x_pos,                   # X positions with offset
            jam_sizes,               # Y positions are the jam sizes
            label=experiment,        # Use the experiment name for labeling
            color=fsd_colors[fsd],   # Color based on FSD
            alpha=0.7,               # Set transparency for better visibility
            edgecolor='black'        # Add edge color for points
        )

# Set axis labels and title
ax.set_xlabel('FSD')
ax.set_ylabel('Jam Size')
ax.set_title('Jam Size by Experiment and Transport Regime')

# Create a legend with unique experiment names
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))

# Show grid for better readability
ax.grid(True)

# Set x-ticks with categorical labels
ax.set_xticks(list(fsd_positions.values()))  # Set ticks as numeric positions
ax.set_xticklabels(list(fsd_colors.keys()))  # Use the FSD categorical values for labels

# Show the plot
plt.tight_layout()
plt.show()