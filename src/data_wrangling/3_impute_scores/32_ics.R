# Script to input impact scores for ICSs

# Load libraries
library(tidyverse)
library(rstudioapi)
library(caret)

# Setup paths
edit_path <- reduce(1:4, ~ .x %>% dirname(), .init = getSourceEditorContext()$path) %>%
  file.path('data', 'edit')

enriched_path <- reduce(1:4, ~ .x %>% dirname(), .init = getSourceEditorContext()$path) %>%
  file.path('data', 'enriched')

# Read data
ics_data <- read.csv(file.path(enriched_path, 'enriched_ref_ics_data.csv'))
dep_data <- readxl::read_xlsx(file.path(edit_path, 'clean_ref_dep_data.xlsx'))

# Some data cleaning
ics_data$inst_id <- as.factor(ics_data$inst_id)
dep_data$inst_id <- as.factor(dep_data$inst_id)

star_cols <- endsWith(colnames(dep_data), '*_Impact')
dep_data[,star_cols] <- sapply(dep_data[,star_cols], FUN = as.numeric)

impact_type <- c('cultural', 'economic', 'environmental', 'health', 'legal', 'political', 'societal', 'technological')
ics_data[,impact_type] <- sapply(ics_data[,impact_type], FUN = function(x){x %>% as.logical() %>% as.numeric()})

random_data <- c('underpinning_research', 'references_to_the_research', 'details_of_the_impact', 'sources_to_corroborate_the_impact', 'summary_of_the_impact_topic')

# Select all uoa_ids with a 100 in any of the four *_Impact columns
dep_data <- dep_data %>%
  mutate('star_impact' = case_when(
    `4*_Impact` == 100 ~ 4,
    `3*_Impact` == 100 ~ 3,
    `2*_Impact` == 100 ~ 2,
    `1*_Impact` == 100 ~ 1
  ))

# Assign the underlying ICSs with the department level score
ics_data <- ics_data %>%
  left_join(dep_data %>% select(star_impact, inst_id, uoa_id),
            by = c('inst_id', 'uoa_id'))

# Additional ICS-level variables
# 1. total amount of funding
calculate_funding <- function(string) {
  if (string == "") {
    sum_value <- NA
  } else {
  pattern <- "(?<=: )\\s*([^:\\[\\]]+)(?=\\])"
  matches <- regmatches(string, gregexpr(pattern, string, perl = TRUE))
  sum_value <- unlist(matches) %>% as.numeric() %>% sum()
  }
  return(sum_value)
}

ics_data <- ics_data %>%
  mutate('total_funding' = lapply(ics_data$grant_funding, FUN = calculate_funding) %>% as.numeric())

# 2. number of researchers
calculate_researchers <- function(string) {
  if (string == "") {
    number <- NA
  } else {
    number <- str_count(string, pattern = '\\]')
  }
  return(number)
}

ics_data <- ics_data %>%
  mutate('n_of_researchers' = lapply(ics_data$researcher_orcids, FUN = calculate_researchers) %>% as.numeric())

# Build training and testing sets
ics_100 <- ics_data %>%
  filter(!is.na(star_impact))

set.seed(1)
id_train <- sample(ics_100$ics_id, nrow(ics_100)*0.5)

ics_train <- ics_100 %>%
  filter(ics_id %in% id_train)

ics_test <- ics_100 %>%
  filter(! ics_id %in% id_train)

# Approach 1
# inst_id and uoa_id cannot be used as predictors,
# because the dataset with 100% stars does not cover all inst_id and uoa_id
ics_100$inst_id %>% unique() %>% length()
ics_data$inst_id %>% unique() %>% length()

ics_100$uoa_id %>% unique() %>% length()
ics_data$uoa_id %>% unique() %>% length()

# Another crucial problem with Approach 1 is that most of the departments with 100% stars are three and four stars,
# hence limiting the predictive power
table(ics_100$star_impact)

# Model 1: Only use complete data
formula_1 <- 'star_impact ~ total_funding + n_of_researchers + ' %>%
  str_c(paste(impact_type, collapse = ' + ')) %>%
  as.formula()
model_1 <- lm(formula_1, data = ics_train)

# Model 1: Add (unfinished) randomly generated topic model data
formula_1_random <- deparse1(formula_1) %>%
  str_c(' + ', paste(random_data, collapse = ' + ')) %>%
  as.formula()
model_1_random <- lm(formula_1_random, data = ics_train)

# Approach II: department level model
# Calculate average stars at department level
dep_data <- dep_data %>%
  mutate('star_average' = (4*`4*_Impact` + 3*`3*_Impact` + 2*`2*_Impact` + 1*`1*_Impact`)/100)

# Aggregate the ICS level dataset to the department level
ics_department <- ics_data %>%
  group_by(inst_id, uoa_id) %>%
  summarise(across(c('total_funding', 'n_of_researchers', all_of(impact_type), all_of(random_data)),
                   ~ mean(.x, na.rm = TRUE)))

# Join the two datasets
ics_department <- ics_department %>%
  left_join(dep_data %>% select(inst_id, uoa_id, star_average),
            by = c('inst_id', 'uoa_id'))

# Model the outcome
# Model 2: Only use complete data
formula_2 <- update(formula_1, star_average ~. + inst_id + uoa_id)
model_2 <- lm(formula_2, data = ics_department)

# Model 2: Add (unfinished) randomly generated topic model data
formula_2_random <- update(formula_1_random, star_average ~. + inst_id + uoa_id)
model_2_random <- lm(formula_2_random, data = ics_department)

# Model 3: without uoa_id
model_3 <- update(model_2, .~. - uoa_id)
model_3_random <- update(model_2_random, .~. - uoa_id)

# Predict scores for all outcomes based on Model I or Model II
ics_test <- ics_test %>% drop_na(n_of_researchers)

ics_impute <- data.frame('actual' = ics_test$star_impact,
                         'impute_1' = predict(model_1, ics_test),
                         'impute_1_random' = predict(model_1_random, ics_test),
                         'impute_2' = predict(model_2, ics_test),
                         'impute_2_random' = predict(model_2_random, ics_test),
                         'impute_3' = predict(model_3, ics_test),
                         'impute_3_random' = predict(model_3_random, ics_test)) %>%
  drop_na()

## Some diagnostics (how well do we fit)
sapply(ics_impute[,2:ncol(ics_impute)],
       FUN = function(x) {RMSE(pred = x, obs = ics_impute$actual)})

plot_data <- ics_impute %>%
  pivot_longer(cols = 2:ncol(ics_impute), names_to = 'type', values_to = 'star')

ggplot(plot_data, aes(x = actual, y = star)) +
  geom_point() +
  geom_smooth(method = 'lm', se = F) +
  facet_wrap(~type, ncol = 2) +
  theme_bw() +
  labs(x = 'Actual stars', y = 'Imputed stars')

## Use the fact that we know how many stars each Department in combination
## with our predictions to i) rank all ICSs per department, ii) assign the
## top ICS the highest available star and repeat for each next highest ICS

# Problems: The number of ICSes at department level is not the least common multiple of
# impact star percentages, so not sure how to actually assign a star to each of them

ics_count <- ics_data %>%
  group_by(inst_id, uoa_id) %>%
  count() %>%
  right_join(dep_data %>% select(inst_id, uoa_id, ends_with('*_Impact')),
             by = c('inst_id', 'uoa_id'))

head(ics_count, 1)
# For instance, in this observation, 25% three stars and 75% 2 stars imply that
# there should be at least 4 ICSes, but there are only two.