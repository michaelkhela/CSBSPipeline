# CSBS Raw Score → Standard Score Converter

Script that converts CSBS raw composite scores to standard scores for the following outputs  
**csbs_SSSocial**, **csbs_SSSpeech**, **csbs_SSSymbolic**, **csbs_SSTotal**

**Author**  
Michael Khela (ch242188) — 05.29.2025

**Important**  
The norms table was transcribed from the official document and saved as `csbs_norms.xlsx` in the `inputs` folder.  
Please do not edit that file.

## What this does

* Reads a de-identified CSBS CSV
* Reads all sheets from the CSBS norms workbook without treating row zero as a header
* Promotes row zero to headers so that each sheet has columns `ss` and age in months
* Maps each raw composite score to its standard score using age-specific single values or ranges
* Outputs a new CSV with the original IDs and ages plus four SS columns

## Inputs

* `inputs/csbs_deid.csv`  
  Expected columns  
  * `studyid`  
  * `ageinmonths`  
  * `csbs_socialcomposite`  
  * `csbs_speechcomposite`  
  * `csbs_symboliccomposite`  
  * `csbs_total_score`
* `inputs/csbs_norms.xlsx`  
  Workbook with sheets named `social`, `speech`, `symbolic`, `total`  
  Each sheet  
  * Row zero contains ages in months across columns one onward  
  * Column zero contains the `ss` values  
  * Body cells contain integers or ranges like `12-15`

## Outputs

* `outputs/CSBS_deid_ss.csv`  
  Same subjects with added columns  
  * `csbs_SSSocial`  
  * `csbs_SSSpeech`  
  * `csbs_SSSymbolic`  
  * `csbs_SSTotal`

## Requirements

* Python 3.9 or newer
* Packages  
  ```bash
  pip install pandas numpy python-docx
