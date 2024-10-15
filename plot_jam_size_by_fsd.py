import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import pandas as pd
from functions import FileFunctions, CountDataFunctions, PlotCountData

# Initialize classes
ff = FileFunctions()
cdf = CountDataFunctions()
pcd = PlotCountData()

# Load count data file
jam_count_data_fn = ff.load_fn("Select count data file")
count_data = pd.read_csv(jam_count_data_fn)
print(count_data)

# Choose constant parameter for each plot (FLOOD stays the same)
FLOOD = "H"

# Define FSD values
fsds = [0.5, 1.0, 2.0, 4.0]

# Store trials and indices by experiment type with trans_reg included
trials_by_exp_type = {}
indices_by_exp_type = {}

for i, fsd in enumerate(fsds):
    condition1 = count_data["flood"] == FLOOD
    condition3 = count_data["fsd"] == fsd

    # Separate trials where trans_reg == "U" and "S"
    condition_U = count_data["trans_reg"] == "U"
    condition_S = count_data["trans_reg"] == "S"
    
    # Store trials separately for "U" and "S"
    trials_U = count_data["exp_name"][condition1 & condition3 & condition_U].unique().tolist()
    trials_S = count_data["exp_name"][condition1 & condition3 & condition_S].unique().tolist()
    trials_by_exp_type[f"{fsd}_U"] = trials_U
    trials_by_exp_type[f"{fsd}_S"] = trials_S

    # Store indices for "U" and "S"
    indices_by_exp_type[f"{fsd}_U"] = {}
    indices_by_exp_type[f"{fsd}_S"] = {}

    for trial in trials_U:
        trial_condition = count_data["exp_name"] == trial
        indices = count_data.index[condition1 & condition3 & condition_U & trial_condition].tolist()
        indices_by_exp_type[f"{fsd}_U"][trial] = indices

    for trial in trials_S:
        trial_condition = count_data["exp_name"] == trial
        indices = count_data.index[condition1 & condition3 & condition_S & trial_condition].tolist()
        indices_by_exp_type[f"{fsd}_S"][trial] = indices

# Initialize plot
fig, ax = plt.subplots(figsize=(12, 6))

# Define colors for each FSD
fsd_colors = {
    '0.5': 'tab:blue',
    '1.0': 'tab:orange',
    '2.0': 'tab:green',
    '4.0': 'tab:red',
}

# Set x-axis offset for S experiments
x_offset_S = 0.3  # Adjust this for spacing between U and S experiments
experiment_offset = 0.1  # For spacing between different experiments

# Map x positions based on FSD
fsd_positions = {fsd: idx for idx, fsd in enumerate(fsd_colors.keys())}

# Loop through FSD and trans_reg groupings
for fsd in fsds:
    for trans_reg, marker, x_shift in zip(["U", "S"], ['o', '^'], [0, x_offset_S]):  # Shift S to the right
        experiments = indices_by_exp_type.get(f"{fsd}_{trans_reg}", {})

        for i, (experiment, indices) in enumerate(experiments.items()):
            # Extract jam sizes and calculate point sizes (linear scaling)
            jam_sizes = count_data['all'].iloc[indices]
            raw_point_sizes = count_data['all_fp'].iloc[indices] / count_data['all'].iloc[indices]
            point_sizes = raw_point_sizes * 100  # Linear scaling (adjust multiplier as needed)

            # Calculate x positions with offset for S experiments
            x_pos = [fsd_positions[str(fsd)] + (i - len(experiments) / 2) * experiment_offset + x_shift] * len(jam_sizes)

            # Plot data with different markers based on trans_reg
            ax.scatter(
                x_pos,              # X positions
                jam_sizes,          # Y positions (jam sizes)
                s=point_sizes,      # Point sizes with linear scaling
                label=experiment,   # Experiment name
                color=fsd_colors[str(fsd)],  # Color based on FSD
                marker=marker,      # Marker based on trans_reg ("U" = circle, "S" = triangle)
                alpha=0.7,          # Transparency
                edgecolor='black'   # Edge color for points
            )

# Set axis labels and title
ax.set_xlabel('FSD')
ax.set_ylabel('Jam Size')
ax.set_title('Jam Size by Experiment, FSD, and Transport Regime')

# Custom legend for point sizes (adjust if needed)
proportions = [0.1, 0.5, 0.9]
legend_sizes = [p * 100 for p in proportions]  # Linear scaling for legend
legend_labels = [f'{p:.1f}' for p in proportions]

legend_handles = [mlines.Line2D([], [], color='black', marker='o', linestyle='None', markersize=size ** 0.5, label=label)
                  for size, label in zip(legend_sizes, legend_labels)]
ax.legend(handles=legend_handles, title='Proportion of jam pieces on floodplain', loc='upper right')

# Grid and x-tick adjustments
ax.grid(True)
ax.set_xticks(list(fsd_positions.values()))
ax.set_xticklabels(list(fsd_colors.keys()))

plt.tight_layout()
plt.show()
