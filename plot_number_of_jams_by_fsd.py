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

#Choose parameters you would like to remain the same across all experiments
FLOOD = "H"
TRANSPORT_REGIME = "U"

condition1 = count_data["flood"] == FLOOD
condition2 = count_data["trans_reg"] == TRANSPORT_REGIME

# Define fsd values
fsds = [0.5, 1.0, 2.0, 4.0]

# Dictionary to store trials and indices by experiment type
indices_by_exp_type = {}

for fsd in fsds:
    condition3 = count_data["fsd"] == fsd
    
    # Find trials that meet the conditions
    trials = count_data["exp_name"][condition1 & condition2 & condition3].unique().tolist()
    
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

# Prepare data for plotting
fsd_values = []
jam_counts = []

for fsd, trials in indices_by_exp_type.items():
    for trial, indices in trials.items():
        # Count the number of jams for the current trial
        jam_count = len(indices)
        
        # Append data for plotting
        fsd_values.append(str(fsd))  # Convert fsd to float for plotting
        jam_counts.append(jam_count)

# Create a scatter plot for number of jams
fig, ax = plt.subplots(figsize=(12, 6))

# Create scatter plot
ax.scatter(fsd_values, jam_counts, color='tab:blue', alpha=0.7)

# Labels and title
ax.set_xlabel('FSD Values')
ax.set_ylabel('Number of Jams')
ax.set_title('Number of Jams per FSD Value')

# Optionally, add a grid
ax.grid()

ax.invert_xaxis()

# Show the plot
plt.tight_layout()
plt.show()
