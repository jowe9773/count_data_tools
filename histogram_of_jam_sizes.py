#import necessary packages and modules
import matplotlib.pyplot as plt
import pandas as pd
from functions import FileFunctions

#initialize classes
ff = FileFunctions()

#choose a count data file
jam_count_data_fn = ff.load_fn("Select count data file")

count_data = pd.read_csv(jam_count_data_fn)

# Extract all jam sizes
all_jam_sizes = count_data["all"]

# Plot histogram of all jam sizes
plt.figure(figsize=(10, 6))
plt.hist(all_jam_sizes, bins=100, color='blue', alpha=0.7, edgecolor='black')

# Add labels and title
plt.title("Histogram of All Jam Sizes Across Experiments")
plt.xlabel("Jam Size")
plt.ylabel("Frequency")

# Show plot
plt.show()