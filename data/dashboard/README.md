# Dashboard Data

This folder contains all of the data required for the dashboard database. The sub-folders include the results from
different topic models. **We are currently using the "nn3nn7" model for the dashboard.**

This document is organised into sections corresponding to the main tables in the dashboard database and explaining where
the relevant source data can be found.

## "ics" table
The only data not included in the `./data/dashboard/` folder is the "enriched_ref_ics_data.csv" because the filesize is 
too large for GitHub. This file can be generated by running the following scripts in sequence:
1. `./src/0_get_data/01_ref.py`
2. `./1_clean_data/11_ref.py`
3. `./2_enrich_data/23_ics.py`

The output will then be saved in `./data/enriched/enriched_ref_ics_data.csv`

## "topics" table
The topics table is found in `./data/dashboard/[model_name]/topics.xlsx`. It contains columns for topic ID, group ID, 
topic name, group name, topic description, topic narrative, and topic keywords.

## "topic_groups" table
This table is found in `./data/dashboard/[model_name]/topic_groups.xlsx`. It contains group ID, group name, 
group description, and group narrative.

## "topic_weights" table
The topic weights are found in the file `./data/dashboard/[model_name]/candidate_[model_name].xlsx`. This file includes
a row for every impact case study (ics) and a column for each topic with cells that contain probabilities of an ics 
belonging to a topic. Note: the integer headers for the columns correspond to the "topic_id" column in 
`./data/dashboard/[model_name]/topics.xlsx`.

## "funder" table
The clean funder lists for every ics are found in the file `./data/dashboard/funders.xlsx`. The clean funders are found 
in the column `Funders[full name]`. This table includes the ICS ID number to link funders back to the "ics" table.  
Note: This table includes columns containing *uncleaned* funders lists from the original REF database (e.g. `Name of funders`).

