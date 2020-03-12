# Split one csv file into multiple
import pandas as pd
import sys, os
from sys import argv

if len(argv) < 3:
    print("Usage: python3 split_csv.py path/to/output/ CSV_NAME.csv")
    sys.exit()

for arg in argv[2:]:
    if arg[-4:] != ".csv":
        print("Usage: python3 split_csv.py path/to/output/ CSV_NAME.csv")
        sys.exit()
    curr_df = pd.read_csv(arg)
    sections_gb = curr_df.groupby('Section')
    sections_list = [sections_gb.get_group(x) for x in sections_gb.groups]
    for x in sections_list:
        x.to_csv(argv[1] + x['Section'].iloc[0] + ".csv", index=False)

# To prefix files in terminal afterwards run
# for f in *; do mv "$f" "PREFIX_$f"; done
