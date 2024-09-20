#plotting_count_data.py

#import neccesary packages and modules
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import gridspec
from functions import FileFunctions, CountDataFunctions

#initialize classes
ff = FileFunctions()
cdf = CountDataFunctions()

#choose a count data file
count_data_fn = ff.load_fn("Select count data file")

count_data = pd.read_csv(count_data_fn)
print(count_data)

#Choose parameters you would like to remain the same across all experiments that you will plot (comment out the parameter you would like to change):
#FSD = 0.5
FLOOD = "H"
TRANSPORT_REGIME = "U"
condition1 = count_data["flood"] == FLOOD
condition2 =  count_data["trans_reg"] == TRANSPORT_REGIME

exps_by_fsd = [[], [], [], []]

for i, fsd in enumerate([0.5, 1.0, 2.0, 4.0]):
    condition3 = count_data["fsd"] == fsd
    exps_by_fsd[i] = count_data.index[condition1 & condition2 & condition3].tolist()

print(exps_by_fsd)

#make a list of lists of matricies so that each experiment has a count data matrix
count_matricies = []
for i, list in enumerate(exps_by_fsd):
    print(list)
    exp_type_matricies = []
    for j, row_index in enumerate(list):
        print(row_index)
        count_matrix = cdf.make_count_matrix(count_data, row_index)
        exp_type_matricies.append(count_matrix)
    count_matricies.append(exp_type_matricies)

print(count_matricies)


#load experiments into appropriate lists
experiments = {
    "FSD 0.5x": count_matricies[0],
    "FSD 1x": count_matricies[1],
    "FSD 2x": count_matricies[2],
    "FSD 4x": count_matricies[3]
}

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