#get_jam_lvl_count_data.py

#load necessary packages and modules
import pandas as pd
import numpy as np
from functions import FileFunctions
from functions import CountDataFunctions


#instantiate classes
ff = FileFunctions()
cdf = CountDataFunctions()




if __name__ == "__main__":
    #load a single count data file
    count_data_file = ff.load_fn("Choose a count data file")
    exps_summary = ff.load_fn("Choose an experiments summary file")


    jam_counts_for_exp = cdf.get_jams_for_exp(count_data_file, exps_summary)

    print(jam_counts_for_exp)
