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
    
                        "jam",

                        "s_fp", "i_fp", "l_fp", "all_fp",
                        "s_cm", "i_cm", "l_cm", "all_cm",
                        "s_ic", "i_ic", "l_ic", "all_ic",
                        "s_tot", "i_tot", "l_tot", "all"])


#now iterate through the filenames, return count data for that experiment and append to output dataframe
for i, filename in enumerate(count_data_files):
    out_data = cdf.get_jams_for_exp(filename, experiments_summary)
    output_df = pd.concat([output_df, out_data], ignore_index=True)

print(output_df)
output_df.to_csv(out_dir + "/jam_count_data.csv")
