#get count data.py

#import neccesary packages and modules
from functions import FileFunctions
from functions import CountDataFunctions

#instantiate classes
ff = FileFunctions()
cdf = CountDataFunctions()


#load count data file and experiment summary file
count_data_file = ff.load_fn("Choose a count data file")

experiments_summary = ff.load_fn("Choose an experiments summary file")

out_dir = ff.load_dn("Choose an output location")

count_data = cdf.load_exp_level_data(count_data_file, experiments_summary)
print(count_data)

count_data.to_csv(out_dir + "/count_data.csv")
