# Load packages
library(tidyverse)
library(haven)
library(rstudioapi)
library(ggmap)

##### Map Q3_c
# Set up paths
current_path <- getSourceEditorContext()$path %>% dirname()
extra_path <- reduce(1:2, ~ .x %>% dirname(), .init = current_path) %>%
  file.path('data_wrangling', '2_enrich_data', 'extra_data')
edit_path <- reduce(1:3, ~ .x %>% dirname(), .init = current_path) %>%
  file.path('data', 'edit')

# Read data
results <- read_sav(file.path(current_path, 'results_25_06.sav'))
key <- read.csv(file.path(current_path, 'results_key.csv'), header = FALSE)
postcode <- read.csv(file.path(extra_path, 'ukprn_postcode.csv'))
ics_data <- readxl::read_excel(file.path(edit_path, 'clean_ref_ics_data.xlsx'))

# Some data cleaning
ics_data$inst_id <- as.factor(ics_data$inst_id)
postcode$Institution.UKPRN.code <- as.factor(postcode$Institution.UKPRN.code)
results$Q3_c <- as.factor(results$Q3_c)

# Extract institutions keys
key_inst <- key %>%
  slice((which(key$V1 == 'Q3_c') + 1):(which(key$V1 == 'Q4') - 1)) %>%
  rename('response_code' = 1, 'name' = 2)

# Merge a dataframe containing response code, institution name, UKPRN and post code
key_inst <- key_inst %>%
  left_join(ics_data %>% select(inst_id, 'Institution name') %>% distinct(),
            by = join_by(name == 'Institution name')) %>%
  left_join(postcode,
            by = join_by(inst_id == 'Institution.UKPRN.code')) %>%
  rename('post_code' = 'Post.Code')

# Manual correction of institution post codes
key_inst[key_inst$response_code == 127, 'post_code'] <- 'EH9 3JG' # SRUC
key_inst[key_inst$response_code == 65, 'post_code'] <- 'NW1 4RY' # Institute of Zoology

# Add longitudes and latitudes
# Please provide your own Google Map API, stored in the file 'google_api.R' and named 'api_key'
source(file.path(current_path, 'google_api.R'))
register_google(api_key)

key_inst <- key_inst %>%
  drop_na(post_code) %>%
  mutate(geocode(post_code))

# Build csv for mapping
map_all <- results %>%
  filter(Q2 == 1) %>%
  select(Q3_c) %>%
  group_by(Q3_c) %>%
  count() %>%
  rename('response_code' = 'Q3_c') %>%
  left_join(key_inst, by = 'response_code') %>%
  drop_na(post_code)

write.csv(map_all, file.path(current_path, 'map', 'map_all.csv'))

map_shape <- results %>%
  filter(Q2 == 1 & subject_1 == 'shape') %>%
  select(Q3_c) %>%
  group_by(Q3_c) %>%
  count() %>%
  rename('response_code' = 'Q3_c') %>%
  left_join(key_inst, by = 'response_code') %>%
  drop_na(post_code)

write.csv(map_shape, file.path(current_path, 'map', 'map_shape.csv'))