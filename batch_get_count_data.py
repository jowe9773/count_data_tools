#batch_get_count_data.py

#import neccesary packages and modules
import pandas as pd
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
count_data_files = ff.find_files_with_name(count_dir, "fieldnotesdata")

#create an output dataframe (empty with column names)
output_df = pd.DataFrame(columns = ["exp_name", "flood", "trans_reg", "fsd",
                                            
                                    "s_dropped", "i_dropped", "l_dropped", "all_dropped",

                                    "s_fp_injam", "i_fp_injam", "l_fp_injam", "all_fp_injam",
                                    "s_cm_injam", "i_cm_injam", "l_cm_injam", "all_cm_injam",
                                    "s_ic_injam", "i_ic_injam", "l_ic_injam", "all_ic_injam",
                                    "s_tot_injam", "i_tot_injam", "l_tot_injam", "all_injam",

                                    "s_fp_ind", "i_fp_ind", "l_fp_ind", "all_fp_ind",
                                    "s_cm_ind", "i_cm_ind", "l_cm_ind", "all_cm_ind",
                                    "s_ic_ind", "i_ic_ind", "l_ic_ind", "all_ic_ind",
                                    "s_tot_ind", "i_tot_ind", "l_tot_ind", "all_ind",

                                    "all_s", "all_i", "all_l", "all_pieces",
                                    "all_fp", "all_cm", "all_ic",

                                    "remobilized_s", "remobilized_i", "remobilized_l", "remobilized_total"])

#now iterate through the filenames, return count data for that experiment and append to output dataframe
for i, filename in enumerate(count_data_files):
    out_data = cdf.load_exp_level_data(filename, experiments_summary)
    output_df = pd.concat([output_df, out_data], ignore_index=True)

print(output_df)
output_df.to_csv(out_dir + "/count_data.csv")