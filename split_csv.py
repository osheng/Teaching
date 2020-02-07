import pandas as pd
import sys, os
from sys import argv
print(len(argv))
if len(argv) < 3:
    print("Usage: python3 split_csv.py path/ CSV_NAME.csv")
    sys.exit()

if argv[2][-4:] != ".csv":
    print("Usage: python3 split_csv.py path/ CSV_NAME.csv")
    print(2)
    sys.exit()

argv2 = argv[1] if argv[1][-1] == "/" else argv[2] + "/"

for arg in argv[2:]:
    curr_df = pd.read_csv(arg)
    sections_gb = curr_df.groupby('Section')
    sections_list = [sections_gb.get_group(x) for x in sections_gb.groups]
    for x in sections_list:
        x.to_csv(argv[1] + x['Section'].iloc[0] + ".csv", index=False)
