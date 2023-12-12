# make_enhanced_data.py

This script is designed to generate a dataframe containing all relevant covariates for the ICS project.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python
- `./src/requirements.txt`

## How to Run the Script

To run the script, use the following command:

```bash
python make_enhanced_data.py
```

### Options/Flags
The script supports the following flags:

-f: Force overwrite of existing files.
-tom: Rerun topic modeling analysis.
-tm: Rerun text-mining processes.
-bq: Rerun analysis of collected dimensions data (do not re-collect data if already present)
-bqf: Rerun analysis of collected dimensions data (do re-collect data if already present)

### Basic usage

In principle, the script assumes the following files to be present, these cannot be generated within the script and the script can *not* be succesfully compiled without them:


- `./data/manual/funders_countries/funders_countries_lookup.xlsx` - a file describing funders' geographic locations.
- `./data/manual/topic_lookup/topic_lookup.csv` - a file describing topics.

The below files are expected to be present unless the `-tom` and `-tm` flags are used, in which case they are generated and force overwritten:
- `./data/edit/ics_pos_features.csv` - number of verbs and nouns per ICS
- `./data/edit/ics_readability.csv` - readability score per ICS
- `./data/edit/ics_sentiment_scores.csv` - sentiment score per ICS

The below files are expected to be present unless the `-bq` flag is used, in which case they are generated:
- `./data/dimensions_returns/merged_dimensions.xlsx`

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
