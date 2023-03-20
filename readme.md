# ICS Analysis

A repository to analyse the Impact Case Studies submitted to the Research Excellence Framework, 2021.

Investigators: Douglas Leasure, Melinda C. Mills, Charles Rahal, Sander Wagner, Mark Verhagen and Bo Zhao

Research Support: Hamza Shams, Bradley Smith, Michelle Thorpe.

### Data pipeline

There are three levels of aggregation at which the data is structured.
- Submission: the level of the actual evaluated submission
- ICS: the case studies underlying each submission 
- Output: the output underlying each ICS

The general structure of the data pipeline is as follows:
1. Collect data from various sources. All tables written into the `data/raw/` folder.
2. Generate tables for the submission, ICS, and underlying output level that contains identifiers linking the three tables and all relevant variables that reside at the table's level of aggregation. Includes feature extraction. All tables written into the `data/edit/` folder.
3. Aggregation of tables across levels (e.g. ICS to submission). All tables written into the `data/edit/` folder.
4. Compiling of a final table for each level of aggregation containing features at the set level of aggregation, as well as summarized features from other levels of aggregation. All tables written into the `data/final/` folder.

General data folder structure is as follows:

`data/raw/`: contains data fetched from various sources.
`data/edit/`: contains wrangled versions of the data contained in `data/raw/`.
`data/final/`: contains final analysis versions of the data.

#### Collect data

Data is fetched from various places through the following scripts contained in the `src/get_data/` folder:

`get_ref_data.py`: fetches data from the REF website.

`get_output_data.py`: tbd

`get_3rd_party_data.py`: tbd

#### Generate aggregation level-specific tables

Data is wrangled and stored, and features are extracted such that we have complete aggregation level specific tables through the following scripts contained in the `src/clean_data/` folder:

`split_ref_ics_dept.py`: splits the data fetcehd from `get_ref_data.py` into a table at the submission level and a table at the ICS level including identifiers.

`models.py`: extracts features at the ICS level.


#### Summarize tables across levels of aggregation

Data is summarized from one level of aggregation to another through the following scripts contained in the `src/agg_data/` folder:

`ics_to_sub.py`: aggregates ICS level data to the submission level.

#### Compile final analysis tables

Data is compiled across aggregation levels into a single, aggregation level specific table containing all relevant features for analysis through the following scripts contained in the `src/merge_data/` folder:

`merge_sub.py`: combines data at the submission level with aggregate data from the ICS and output level.
