#plot_bar_charts_simple.py

#import neccesary packages and modules
import pandas as pd
from functions import FileFunctions, CountDataFunctions, PlotCountData

#initialize classes
ff = FileFunctions()
cdf = CountDataFunctions()
pcd = PlotCountData()

#choose a count data file
count_data_fn = ff.load_fn("Select count data file")

count_data = pd.read_csv(count_data_fn)
print(count_data)

#Choose parameters you would like to remain the same across all experiments that you will plot (comment out the parameter you would like to change):
FLOOD = "H"
TRANSPORT_REGIME = "U"
FSD = 1.0
condition1 = count_data["flood"] == FLOOD
condition2 =  count_data["trans_reg"] == TRANSPORT_REGIME

exps_by_fsd = [[], [], [], []]

for i, fsd in enumerate([0.5, 1.0, 2.0, 4.0]):
    condition3 = count_data["fsd"] == fsd
    exps_by_fsd[i] = count_data.index[condition1 & condition2 & condition3].tolist()

print(exps_by_fsd)