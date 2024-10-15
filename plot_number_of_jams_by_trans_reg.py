#import necessary packages and modules
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pprint import pprint 
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
FSD = 0.5

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

# Prepare data for plotting
fsd_values = []
jam_counts = []

for fsd, trials in indices_by_exp_type.items():
    for trial, indices in trials.items():
        # Count the number of jams for the current trial
        jam_count = len(indices)
        
        # Append data for plotting
        fsd_values.append(fsd)  # Keep fsd as a string or category
        jam_counts.append(jam_count)

# Create a scatter plot for number of jams
fig, ax = plt.subplots(figsize=(12, 6))

# Create scatter plot
ax.scatter(fsd_values, jam_counts, color='tab:blue', alpha=0.7)

# Labels and title
ax.set_xlabel('FSD Values')
ax.set_ylabel('Number of Jams')
ax.set_title('Number of Jams per by Transport Regime')

# Set categorical values on the x-axis
ax.set_xticks(np.arange(len(trans_regs)))  # Number of categories
ax.set_xticklabels(trans_regs)  # Use the categorical labels

# Optionally, add a grid
ax.grid()

# Show the plot
plt.tight_layout()
plt.show()
