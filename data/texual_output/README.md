## Textual output

A  folder to place all the output for BERT-based topic modelling on ICS data.

The folder is organised as followed:

- **main_ics**: output of topic modelling results for the main target of analysis. This include three columns: 1. Summary of Impact; 2. Underpinning research; 4. Details of the input; as well as modelling on all three columns combined. It has two subfolders.
  - **classification_results**: Topic classification results and topic probabilities.
  - **topic_model_keywords**: keywords for each model accordingly.
- **survey**: topic modelling results for the free response files.



#### File naming conventions

All files are named through the following format: [Range of rows]\_[feature of methods]\_[nature of file]\_[column].csv. Feature of methods and columns are optional suffixes. For example, all_responses_semi_supervised_keywords_1. Summary of the impact.csv are topic modelling keywords of all rows in the ics table, with semi supervised methods, and modelled using column “Summary of the impact”.

