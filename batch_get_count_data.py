#batch_get_count_data.py

#import neccesary packages and modules
from functions import FileFunctions
from functions import CountDataFunctions

#instantiate classes
ff = FileFunctions()
cdf = CountDataFunctions()

#load experiments summary file and choose a directory containing all of the count data files and a directory to store the output in
experiments_summary = ff.load_fn("Choose an experiments summary file")

count_dir = ff.load_dn("Choose a directory containing all of the count data files")

out_dir = ff.load_dn("Choose an output location")

#create a list of all fo the count data filepaths


