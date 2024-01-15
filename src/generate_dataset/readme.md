# make_enhanced_data.py

`make_enhanced_data.py` is a Python script for generating a comprehensive dataframe with all necessary covariates for the ICS project.

## Prerequisites

Ensure the following are installed before running the script:

- Python 3.x
- Dependencies listed in `./src/requirements.txt`

## Installation

Install required packages:

```bash
pip install -r ./src/requirements.txt
```

## Usage
### Running the Script

```bash
python make_enhanced_data.py [options]
```

### Options
-`f`: Force overwrite of existing files.
-`tom`: Rerun topic modeling analysis.
-`tm`: Rerun text-mining processes.
-`bq`: Rerun analysis of collected dimensions data (without re-collecting data).
-`bqf`: Rerun analysis and re-collect dimensions data (requires a Big Query API token).

### Input Files


The script expects certain files to be present. Unless specified by the flags `-tom`, `-tm`, and `-bq`, these files are not auto-generated:

- `./data/manual/funders_countries/funders_countries_lookup.xlsx` - Funders' geographic locations.
- `./data/manual/topic_lookup/topic_lookup.csv` - Topics descriptions.
- `./data/edit/ics_pos_features.csv` - Verbs and nouns count per ICS. (unless `-tm` flag is used)
- `./data/edit/ics_readability.csv` - Readability score per ICS. (unless `-tm` flag is used)
- `./data/edit/ics_sentiment_scores.csv` - Sentiment score per ICS. (unless `-tm` flag is used)
- `./data/dimensions_returns/merged_dimensions.xlsx` - Dimensions data. (unless `-bq` flag is used)

Use `-bqf` if you want to force re-collection of the data as well, this likely requires a Big Query API token.

Assuming the above requirements are satisfied, basic usage is as follows:

Write final file to default path at `./data/final/enhanced_ref_data.csv` if it does *not* yet exist:

```bash
python make_enhanced_data.py
```

Force write final file to default path at `./data/final/enhanced_ref_data.csv` even if it already exists:

```bash
python make_enhanced_data.py -f
```

Force write final file to a specified path `[path].csv`:

```bash
python make_enhanced_data.py -f -[path].csv
```

Write final file to default path and re-estimate text mining variables:

```bash
python make_enhanced_data.py -tm
```

Write final file to default path and re-estimate topic model variables:

```bash
python make_enhanced_data.py -tom
```

Write final file to default path and re-analyze dimensions data:

```bash
python make_enhanced_data.py -bq
```
