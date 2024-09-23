#plotting_count_data.py

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
condition1 = count_data["flood"] == FLOOD
condition2 =  count_data["trans_reg"] == TRANSPORT_REGIME

exps_by_fsd = [[], [], [], []]

for i, fsd in enumerate([0.5, 1.0, 2.0, 4.0]):
    condition3 = count_data["fsd"] == fsd
    exps_by_fsd[i] = count_data.index[condition1 & condition2 & condition3].tolist()

print(exps_by_fsd)

#make a list of lists of matricies so that each experiment has a count data matrix
count_matricies = []
for i, lis in enumerate(exps_by_fsd):
    print(lis)
    exp_type_matricies = []
    for j, row_index in enumerate(lis):
        print(row_index)
        count_matrix = pcd.make_count_matrix(count_data, row_index)
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

pcd.plot_heatmaps(experiments)
