#plot_ranges.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from functions import FileFunctions, CountDataFunctions, PlotCountData

#initialize classes
ff = FileFunctions()
cdf = CountDataFunctions()
pcd = PlotCountData()

#choose a count data file and load in data
count_data_fn = ff.load_fn("Select count data file")
count_data = pd.read_csv(count_data_fn)


#add column that is proportion of pieces that stayed in the flume that are on the floodplain
count_data["fp_prop"] = count_data["all_fp"] / count_data["all_pieces"]


# Create the scatter plot with seaborn
sns.scatterplot(x="fsd", y="fp_prop", hue = "flood", style = "trans_reg", palette = "viridis", data = count_data)

plt.xlabel("FSD")
plt.ylabel("Proportion of Pieces on Floodplain")
plt.title("proportion of pieces on fp vs. fsd")
plt.show()