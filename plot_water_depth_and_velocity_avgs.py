import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerTuple
from matplotlib.lines import Line2D
from functions import FileFunctions

ff = FileFunctions()

# Set font sizes globally
plt.rcParams.update({
    'font.size': 18,         # General font size
    'axes.titlesize': 20,    # Title font size
    'axes.labelsize': 18,    # X and Y labels font size
    'xtick.labelsize': 16,   # X-axis tick labels font size
    'ytick.labelsize': 16,   # Y-axis tick labels font size
    'legend.fontsize': 16,   # Legend font size
})

# Load your CSV file
file = ff.load_fn("Choose avg data file")
df = pd.read_csv(file)

# Extract the data
categories = df['FSD'].astype(str)
avg1_instance1 = df['fp_u_mean (m/s)']
std1_instance1 = df['fp_u_st.dev (m/s)']
avg2_instance1 = df['fp_h_mean (mm)']
std2_instance1 = df['fp_h_st.dev (mm)']

avg1_instance2 = df['ch_u_mean (m/s)']
std1_instance2 = df['ch_u_st.dev (m/s)']
avg2_instance2 = df['ch_h_mean (mm)']
std2_instance2 = df['ch_h_st.dev (mm)']

# Create the figure and axis objects
fig, ax1 = plt.subplots()

# Plot Thing 1, instance 1 and instance 2 on the first y-axis
line1 = ax1.errorbar(categories, avg1_instance1, fmt='o-', label='Floodplain velocity', color='tab:blue',
             elinewidth=1, ecolor='grey')
line2 = ax1.errorbar(categories, avg1_instance2, fmt='^-', label='Channel velocity', color='tab:blue',
             elinewidth=1, ecolor='grey')
ax1.set_xlabel('Relative Tree Spacing')
ax1.set_ylabel('Mean Surface U (m/s)', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Create a second y-axis sharing the same x-axis
ax2 = ax1.twinx()

# Plot Thing 2, instance 1 and instance 2 on the second y-axis
line3 = ax2.errorbar(categories, avg2_instance1, fmt='o-', label='Floodplain depth', color='tab:orange',
             elinewidth=1, ecolor='grey')
line4 = ax2.errorbar(categories, avg2_instance2, fmt='^-', label='Channel depth', color='tab:orange',
             elinewidth=1, ecolor='grey')
ax2.set_ylabel('Mean Water Depth (mm)', color='tab:orange')
ax2.tick_params(axis='y', labelcolor='tab:orange')

# Set the x-axis labels to categorical values
plt.xticks(rotation=45)  # Rotate labels if necessary

# Add a title
plt.title('Water Depth and Surface Velocity vs. Relative Tree Spacing')

# Custom legend: one black circle and one black triangle
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=10, label='Floodplain'),
    Line2D([0], [0], marker='^', color='w', markerfacecolor='black', markersize=10, label='Channel')
]

# Display the custom legend
ax1.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0.8, 0.5))

# Show the plot
plt.tight_layout()  # Adjusts layout to fit everything nicely
plt.show()