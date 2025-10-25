# Script created to convert Raw CSBS scores to SS for csbs_SSSocial, csbs_SSSpeech, csbs_SSSymbolic, csbs_SSTotal
# Created by Michael Khela (ch242188) on 5.29.25
# To make the code run easier, a reference table was created from the norm.docx. It can be found in the inputs folder! PLEASE DO NOT EDIT

# Import necessary libraries
import os
import pandas as pd
import numpy as np
from docx import Document

# Input necessary filepaths for the script to work
root = "/Users/michaelkhela/Desktop/everything/Working/Projects/CSBS"
csbs_csv  = os.path.join(root, "inputs", "csbs_deid.csv")
norm_xlsx = os.path.join(root, "inputs", "csbs_norms.xlsx")
output_dir = os.path.join(root, "outputs")

# Read CSBS csv and create it as a df
csbs_data = pd.read_csv(csbs_csv)

# Read every sheet without inferring headers so row 0 remains data
raw_norms = pd.read_excel(norm_xlsx, sheet_name=None, header=None)

# Promote row 0 into the column names, convert 'ss' to int, store back
norms_dict = {}
for sheet_name, df in raw_norms.items():
    # build the new header: first entry is 'ss', then the ages from row 0, cols 1 onwards
    age_list = df.iloc[0, 1:].astype(int).tolist()  
    new_cols = ['ss'] + age_list                    

    body = df.iloc[1:].copy()    # drop the old header row
    body.columns = new_cols      # assign new column names
    body['ss'] = body['ss'].astype(int)
    norms_dict[sheet_name] = body

# Cleans the csbs data
raw_cols = [c for c in csbs_data.columns 
            if c.endswith('composite') or c == 'csbs_total_score']
keep_cols = ['studyid', 'ageinmonths'] + raw_cols

mask = (csbs_data['ageinmonths'] != 0) & (csbs_data['ageinmonths'] != 2)
csbs_cleaned = csbs_data.loc[mask, keep_cols].copy()

#  Converts one raw→SS 
def raw_to_ss(raw, age, norms_df):
    if pd.isnull(raw) or pd.isnull(age):
        return np.nan

    age = int(age)
    if age not in norms_df.columns:
        return np.nan

    for _, row in norms_df.iterrows():
        ss_val    = row['ss']
        raw_range = row[age]
        if pd.isnull(raw_range):
            continue

        txt = str(raw_range).strip()
        if '-' in txt:
            lo, hi = txt.split('-', 1)
            if int(lo) <= raw <= int(hi):
                return ss_val
        else:
            if raw == int(txt):
                return ss_val
    return np.nan

# Build a mapping raw_col → sheet_name
sheet_mapping = {
    'csbs_socialcomposite': 'social',
    'csbs_speechcomposite': 'speech',
    'csbs_symboliccomposite': 'symbolic',
    'csbs_total_score': 'total'
}
ss_name_map = {
    'csbs_socialcomposite':   'csbs_SSSocial',
    'csbs_speechcomposite':   'csbs_SSSpeech',
    'csbs_symboliccomposite': 'csbs_SSSymbolic',
    'csbs_total_score':       'csbs_SSTotal'
}

# Loop over every raw score
for raw_col, sheet in sheet_mapping.items():
    ss_col   = ss_name_map[raw_col]    
    norms_df = norms_dict[sheet]

    csbs_cleaned[ss_col] = csbs_cleaned.apply(
        lambda r: raw_to_ss(r[raw_col], r['ageinmonths'], norms_df),
        axis=1
    )

# Define your output filename
out_fname = "CSBS_deid_ss.csv"
out_path  = os.path.join(output_dir, out_fname)

# Write to a csv
csbs_cleaned.to_csv(out_path, index=False)
