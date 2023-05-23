## Script to imput impact scores for ICSs

## Load libraries
library(tidyverse)

## Setup paths
edit_path <- "./data/edit/"
enriched_path <- "./data/enriched/"

## Read data
ics_data <- readxl::read_xlsx(paste0(
    enriched_path,
    "enriched_ref_ics_data.xlsx"
))

dep_data <- readxl::read_xlsx(paste0(
    edit_path,
    "clean_ref_dep_data.xlsx"
))

## Approach I: only use 100%

## Select all uoa_ids with a 100 in any of the four *_Impact columns

## Assign the underlying ICSs with the department level score

## Model the outcome

## Approach II: department level model

## Left join department level Impact score to the ICS dataset

## Aggregate the ICS level dataset to the department level

## Model the outcome

## Predict scores for all outcomes based on Model I or Model II

## Some diagnostics (how well do we fit)

## Use the fact that we know how many stars each Department in combination
## with our predictions to i) rank all ICSs per department, ii) assign the
## top ICS the highest available star and repeat for each next highest ICS

