#import necessary packages and modules
import matplotlib.pyplot as plt
from pprint import pprint 
import matplotlib.lines as mlines
import pandas as pd
from functions import FileFunctions, CountDataFunctions, PlotCountData

#initialize classes
ff = FileFunctions()
cdf = CountDataFunctions()
pcd = PlotCountData()

# Update font sizes globally
plt.rcParams.update({
    'font.size': 24,  # General font size
    'axes.titlesize': 26,  # Title font size
    'axes.labelsize': 24,  # Axis label font size
    'xtick.labelsize': 22,  # X-tick label font size
    'ytick.labelsize': 22,  # Y-tick label font size
    'legend.fontsize': 22,  # Legend font size
})

dot_size = 5

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

# Initialize the plot
fig, ax = plt.subplots(figsize=(12, 6))

# Define colors for each FSD
fsd_colors = {
    '0.5': 'tab:blue',
    '1.0': 'tab:orange',
    '2.0': 'tab:green',
    '4.0': 'tab:purple',
}

# Initialize an offset value to separate points from different experiments
experiment_offset = 0.2  # Adjust this value for spacing between experiments

# Create a mapping for x positions based on FSD
fsd_positions = {fsd: idx for idx, fsd in enumerate(fsd_colors.keys())}

# Loop through each FSD group
for fsd, experiments in indices_by_exp_type.items():
    # Initialize a counter for x positions
    x_positions = []

    # Loop through the experiments within the current FSD
    for i, (experiment, indices) in enumerate(experiments.items()):
        # Extract the proportion of pieces on the floodplain for the given indices
        proportion_fp = (count_data['all_fp'].iloc[indices]) / count_data['all'].iloc[indices]

        # Use total pieces in the jam to determine point sizes
        point_sizes = count_data['all'].iloc[indices] * dot_size  # Scale factor for better visibility

        # Calculate x positions with an offset for this experiment
        x_pos = [fsd_positions[fsd] + (i - len(experiments) / 2) * experiment_offset] * len(proportion_fp)
        x_positions.extend(x_pos)

        # Plot the proportion of floodplain pieces as scatter points with varying sizes
        ax.scatter(
            x_pos,                    # X positions with offset
            proportion_fp,            # Y positions are the proportions of floodplain pieces
            s=point_sizes,            # Set point sizes based on the total pieces
            label=experiment,         # Use the experiment name for labeling
            color=fsd_colors[fsd],    # Color based on FSD
            alpha=0.7,                # Set transparency for better visibility
            edgecolor='black'         # Add edge color for points
        )

# Set axis labels and title
ax.set_xlabel('FSD')
ax.set_ylabel('Proportion of Pieces on Floodplain')
ax.set_title('Proportion of Jam Pieces on Floodplain by Experiment and FSD')

# Define total number of pieces (jam sizes) for the legend
jam_sizes_for_legend = [10, 100, 500]  # Example sizes; adjust based on your data

# Calculate point sizes for the legend based on these jam sizes
legend_sizes = [size * dot_size for size in jam_sizes_for_legend]  # Scale sizes

# Define labels showing the number of pieces (e.g., '10 pieces', '50 pieces', '100 pieces')
legend_labels = [f'{size} pieces' for size in jam_sizes_for_legend]

# Create custom legend handles for the jam sizes
legend_handles = [
    mlines.Line2D([], [], color='black', marker='o', linestyle='None', 
                  markersize=size ** 0.5, label=label)
    for size, label in zip(legend_sizes, legend_labels)
]

# Add the custom legend for point sizes to the plot
ax.legend(handles=legend_handles, title='Total Jam Pieces', loc='center left')

# Show grid for better readability
ax.grid(True)

# Set x-ticks with categorical labels
ax.set_xticks(list(fsd_positions.values()))  # Set ticks as numeric positions
ax.set_xticklabels(list(fsd_colors.keys()))   # Use the same categorical values for labels
ax.invert_xaxis()

# Show the plot
plt.tight_layout()
plt.show()
