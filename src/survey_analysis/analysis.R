# Load packages
library(tidyverse)
library(rstudioapi)
library(haven)
library(kableExtra)
library(factoextra)
library(ggpmisc)
library(ggrepel)
library(stargazer)
library(scales)
library(dotwhisker)
library(pheatmap)

# Set up paths
current_path <- getSourceEditorContext()$path %>% dirname()

# Read data
results <- read_sav(file.path(current_path, 'results_25_06.sav'))
key <- read.csv(file.path(current_path, 'results_key.csv'), header = FALSE)

# UOA key
key_uoa <- key %>%
  slice((which(V1 == 'Q7') + 1):(which(V1 == 'Q8') - 1)) %>%
  mutate('col_name' = paste0('Q7_', V1),
         'name' = str_extract(V2, "(?<=: ).*|[^:]*$") %>% str_squish()) %>%
  select(col_name, name)

##### Subject 1: SHAPE or STEM
shape_panels <- c('Q7_5', paste0('Q7_', 14:35))
stem_panels <- c(paste0('Q7_', 2:4), paste0('Q7_', 6:13))

results <- results %>%
  mutate('shape' = apply(results %>% select(all_of(shape_panels)),
                         MARGIN = 1,
                         FUN = function (x) {ifelse(1 %in% x, 1, 0)}),
         'stem' = apply(results %>% select(all_of(stem_panels)),
                        MARGIN = 1,
                        FUN = function (x) {ifelse(1 %in% x, 1, 0)}))

results <- results %>%
  mutate('subject_1' = case_when(
    shape == 1 ~ 'shape',
    stem == 1 ~ 'stem'
  ))

# Adjust for 'main panel' people
results[results$Q28 == 93174, 'subject_1'] <- 'shape' # Evangelos Himonides
results[results$Q28 == 81207, 'subject_1'] <- 'stem' # Clinical Medicine person
results[results$Q28 == 88945, 'subject_1'] <- 'stem' # Biological Sciences person

table(results$subject_1)

##### Subject 2: Social Sciences or Humanities
social_sciences_panels <- c('Q7_5', paste0('Q7_', 14:26))
humanities_panels <- paste0('Q7_', 27:35)

results <- results %>%
  mutate('social_sciences' = apply(results %>% select(all_of(social_sciences_panels)),
                                   MARGIN = 1,
                                   FUN = function (x) {ifelse(1 %in% x, 1, 0)}),
         'humanities' = apply(results %>% select(all_of(humanities_panels)),
                              MARGIN = 1,
                              FUN = function (x) {ifelse(1 %in% x, 1, 0)}))

results <- results %>%
  mutate('subject_2' = case_when(
    social_sciences == 1 ~ 'social sciences',
    humanities == 1 ~ 'humanities'
  ))

# Manually adjust people who are both social sciences and humanities (based on Q8)
results[results$Q28 %in% c('53762', '43453', '52843', '85838'), 'subject_2'] <- 'humanities'
results[results$Q28 %in% c('50704', '31089', '5638', '93174'), 'subject_2'] <- 'social sciences'

table(results$subject_2)

##### Extract free text data
free_text <- results %>%
  filter(Q1 == 1) %>%
  select(Q28, subject_1, subject_2, Q9, Q11, Q16, Q17, Q21, Q24) %>%
  drop_na(subject_1)

write.csv(free_text, file.path(current_path, 'free_text.csv'))

##### Q3_a sector
df_q3a <- results %>%
  filter(Q2 == 1) %>%
  mutate('sector' = case_when(
    Q3_1 == 1 ~ 'University',
    Q3_2 == 1 ~ 'Research Centre',
    Q3_3 == 1 ~ 'Private Sector',
    Q3_4 == 1 ~ 'Government/Public Service',
    Q3_5 == 1 ~ 'Non-Governmental Organisation/Think Tank',
    Q3_6 == 1 ~ 'Other'
  ))

# social sciences/humanities
table(df_q3a$sector, df_q3a$subject_2) %>%
  addmargins() %>%
  as.data.frame.matrix() %>%
  slice(6,5,4,1,2,3) %>%
  kable(booktabs = T, col.names = c('Humanities', 'Social Sciences', 'Total')) %>%
  kable_classic_2(full_width = F)

##### Q3_b position
df_q3b <- results %>%
  filter(Q2 == 1) %>%
  mutate('position' = case_when(
    Q3_b_1 == 1 ~ 'University Management',
    Q3_b_2 == 1 ~ 'Professor',
    Q3_b_3 == 1 ~ 'Reader/Assoc. Assist. Professor/Lecturer',
    Q3_b_4 == 1 ~ 'Reader/Assoc. Assist. Professor/Lecturer',
    Q3_b_5 == 1 ~ 'Reader/Assoc. Assist. Professor/Lecturer',
    Q3_b_6 == 1 ~ 'Other',
    Q3_b_7 == 1 ~ 'Other',
    Q3_b_8 == 1 ~ 'Other',
    Q3_b_9 == 1 ~ 'Other',
    Q3_b_10 == 1 ~ 'Other',
    Q3_b_11 == 1 ~ 'Other',
    Q3_b_12 == 1 ~ 'Other',
  ))

# shape/stem
table(df_q3b$position, df_q3b$subject_1) %>%
  addmargins() %>%
  as.data.frame.matrix() %>%
  arrange(desc(shape)) %>%
  slice(-1) %>%
  kable(booktabs = T, col.names = c('SHAPE', 'STEM', 'Total')) %>%
  kable_classic_2(full_width = F)

# social sciences/humanities
table(df_q3b$position, df_q3b$subject_2) %>%
  addmargins() %>%
  as.data.frame.matrix() %>%
  arrange(desc(humanities)) %>%
  slice(-1) %>%
  kable(booktabs = T, col.names = c('Humanities', 'Social Sciences', 'Total')) %>%
  kable_classic_2(full_width = F)

##### Q4 age when received phd
df_q4 <- results %>%
  filter(Q2 == 1) %>%
  mutate('age_phd' = Q4 + 1949)

ggplot(data = df_q4 %>% drop_na(subject_2),
       aes(x = age_phd, fill = subject_2)) +
  geom_histogram(position = 'dodge', binwidth = 5) +
  theme_bw() +
  labs(x = 'Year receiving PhD', y = 'Count', fill = 'Subject') +
  scale_fill_discrete(labels = c('Humanities', 'Social Sciences')) +
  scale_x_continuous(breaks = seq(1970, 2020, 5)) +
  theme(axis.title = element_text(size = 20),
        axis.text = element_text(size = 20),
        legend.title = element_text(size = 20),
        legend.text = element_text(size = 20))

ggplot(data = df_q4 %>% drop_na(subject_2),
       aes(x = age_phd)) +
  geom_histogram(binwidth = 5) +
  facet_wrap(~ subject_2, labeller = as_labeller(c('humanities' = 'Humanities', 'social sciences' = 'Social Sciences'))) +
  theme_bw() +
  labs(x = 'Year receiving PhD', y = 'Count') +
  scale_x_continuous(breaks = seq(1970, 2020, 5)) +
  theme(axis.title = element_text(size = 20),
        axis.text = element_text(size = 20),
        strip.text = element_text(size = 20))

##### Q5_6 descriptive stats
df_q56 <- df_q4 %>%
  select(age_phd, Q5, Q6, subject_2)

df_q56 <- df_q56 %>%
  mutate('gender' = case_when(
    Q5 == 1 ~ 'Female',
    Q5 == 2 ~ 'Male',
    Q5 == 4 ~ 'Prefer not to say'
  ),
         'race' = case_when(
           Q6 == 1 ~ 'Asian or Asian British',
           Q6 == 2 ~ 'Black, Black British, Caribbean or African',
           Q6 == 3 ~ 'Mixed or multiple ethnic groups',
           Q6 == 4 ~ 'White',
           Q6 == 5 ~ 'Other ethnic group')) %>%
  drop_na(subject_2)

by(df_q56$age_phd, df_q56$subject_2, mean)
mean(df_q56$age_phd)

by(df_q56$gender, df_q56$subject_2, function (x) {table(x) %>% prop.table() %>% round(4)})
table(df_q56$gender) %>% prop.table() %>% round(4)

by(df_q56$race, df_q56$subject_2, function (x) {table(x) %>% prop.table() %>% round(4)})
table(df_q56$race) %>% prop.table() %>% round(4)

##### Q10 Desired ICS weight
df_q10 <- results %>%
  filter(!is.na(subject_2)) %>%
  mutate(Q10 = as.numeric(Q10))

mean(df_q10$Q10[df_q10$subject_2 == 'humanities'], na.rm = TRUE) %>% round(2)
mean(df_q10$Q10[df_q10$subject_2 == 'social sciences'], na.rm = TRUE) %>% round(2)
mean(df_q10$Q10, na.rm = T) %>% round(2)

ggplot(data = df_q10, aes(x = Q10, fill = subject_2)) +
  geom_histogram(position = 'stack', binwidth = 5) +
  scale_x_continuous(breaks = seq(0,100,5)) +
  scale_fill_discrete(labels = c('Humanities', 'Social Sciences')) +
  annotate(geom = 'text', x = 70, y = 30, label = 'Humanities Average: 23.70 \n Social Sciences Average: 23.84') +
  labs(x = 'Desired ICS Weight', y = 'Count', fill = 'Subject') +
  theme_bw() +
  theme(axis.title = element_text(size = 20),
        axis.text = element_text(size = 20),
        legend.title = element_text(size = 20),
        legend.text = element_text(size = 20))

ggplot(data = df_q10, aes(x = Q10, fill = subject_2)) +
  geom_histogram(position = 'dodge', binwidth = 5) +
  scale_x_continuous(breaks = seq(0,100,5)) +
  scale_fill_discrete(labels = c('Humanities', 'Social Sciences')) +
  annotate(geom = 'text', x = 70, y = 30, label = 'Humanities Average: 23.70 \n Social Sciences Average: 23.84') +
  labs(x = 'Desired ICS Weight', y = 'Count', fill = 'Subject') +
  theme_bw() +
  theme(axis.title = element_text(size = 20),
        axis.text = element_text(size = 20),
        legend.title = element_text(size = 20),
        legend.text = element_text(size = 20))

# Regression analysis
df_q10_r <- df_q10 %>%
  filter(Q2 == 1) %>%
  left_join(df_q3b %>% select(Q28, position), by = join_by(Q28)) %>%
  mutate('gender' = case_when(
    Q5 == 1 ~ 'Female',
    Q5 == 2 ~ 'Male',
    Q5 == 4 ~ 'Prefer not to say'),
         'age_phd' = Q4 + 1949,
         'russel_group' = Q3_c %in% c(14, 21, 24, 27, 39, 43, 46, 48, 63, 68, 71, 77, 83, 87, 91, 97, 99, 104, 105, 122, 126, 145, 148, 156),
         'management' = position == 'University Management') %>%
  replace_na(list(management = FALSE))

model_q10 <- lm(Q10 ~ gender + age_phd + russel_group + management + subject_2, data = df_q10_r)
summary(model_q10)
stargazer(model_q10)

# Standardised coefficient
gender_dummy <- model.matrix(~ gender, data = df_q10_r)[,-1] %>%
  as.data.frame() %>%
  rename('genderMale' = 1, 'genderNot' = 2)

df_q10_r_s <- df_q10_r %>%
  cbind(gender_dummy) %>%
  mutate('age_phd_s' = scale(df_q10_r$age_phd)[,1],
         'Q10_s' = scale(df_q10_r$Q10)[,1])

model_q10_s <- lm(Q10_s ~ genderMale + genderNot + age_phd_s + russel_group + management + subject_2,
                  data = df_q10_r_s)

summary(model_q10_s)

plotdata_q10 <- data.frame('coef' = coef(model_q10_s),
                           confint(model_q10_s)) %>%
  rename('lower' = 2, 'upper' = 3) %>%
  rownames_to_column('var') %>%
  slice(-1, -3) %>%
  mutate('var' = as.factor(var)) %>%
  mutate('sig' = var == 'age_phd_s')

levels(plotdata_q10$var) <- c('Age Receiving PhD', 'Gender: Male', 'University Management', 'Russel Group', 'Subject: Social Sciences')

ggplot(data = plotdata_q10, aes(x = coef, y = var, colour = sig)) +
  geom_point(size = 5) +
  geom_linerange(aes(xmin = lower, xmax = upper)) +
  geom_vline(xintercept = 0, linetype = 'dotted') +
  scale_colour_manual(values = c('black', 'red')) +
  labs(x = 'Coefficient', y = 'Variable') +
  theme_bw() +
  theme(axis.title = element_text(size = 20),
        axis.text = element_text(size = 20),
        legend.position = 'none')

##### Q12 rank indicators - PCA
df_q12 <- results %>%
  filter(!is.na(subject_2)) %>%
  drop_na(starts_with('Q12_'))

# Reverse the rank to make it more interpretable
df_q12[,startsWith(colnames(df_q12), 'Q12_')] <- 11 - df_q12[,startsWith(colnames(df_q12), 'Q12_')]

key_q12 <- key %>%
  filter(startsWith(V1, 'Q12_')) %>%
  mutate('short' = str_extract(V2, "^(.*?)(?=\\()|.*"))

# Perform PCA
pca_q12 <- prcomp(df_q12 %>% select(starts_with('Q12_')), scale. = FALSE)

# Write a function for variance plot of PCs
var_plot <- function(pca_model) {
  n_of_pc <- length(pca_model$sdev)

  plot_data <- as.data.frame(pca_model$sdev) %>%
    rename('sd' = 1) %>%
    rowid_to_column(var = 'PC') %>%
    mutate('var' = sd^2)

  ggplot(data = plot_data, aes(x = PC, y = var)) +
    geom_point(size = 5, shape = 1) +
    geom_line() +
    theme_bw() +
    scale_x_continuous(breaks = seq(1,n_of_pc,1)) +
    labs(x = 'Principle Components', y = 'Variance Explained') +
    theme(axis.title = element_text(size = 20),
          axis.text = element_text(size = 20))
}

var_plot(pca_q12)

# Visualise the first two PCs
df_q12 <- df_q12 %>%
  mutate('PC1' = pca_q12$x[,'PC1'],
         'PC2' = pca_q12$x[,'PC2'])

ggplot(data = df_q12, aes(x = PC1, y = PC2, colour = subject_2)) +
  geom_point(size = 5) +
  geom_quadrant_lines(linetype = 'dotted') +
  scale_x_continuous(limits = symmetric_limits) +
  scale_y_continuous(limits = symmetric_limits) +
  scale_colour_discrete(labels = c('Humanities', 'Social Sciences')) +
  theme_minimal() +
  labs(colour = 'Subject') +
  theme(axis.title = element_text(size = 20),
        axis.text = element_text(size = 20),
        legend.title = element_text(size = 20),
        legend.text = element_text(size = 20))

t.test(data = df_q12, PC1 ~ subject_2)
t.test(data = df_q12, PC2 ~ subject_2)

# Loadings of PC1
pca_q12$rotation %>%
  as.data.frame() %>%
  select(PC1) %>%
  rownames_to_column(var = 'indicator_id') %>%
  left_join(key_q12, by = join_by(indicator_id == V1)) %>%
  arrange(PC1) %>%
  select(PC1, V2) %>%
  rename('Loading' = 1, 'Indicator' = 2) %>%
  kable(booktabs = TRUE, caption = 'PC1') %>%
  kable_classic_2(full_width = F)

# Loadings of PC2
pca_q12$rotation %>%
  as.data.frame() %>%
  select(PC2) %>%
  rownames_to_column(var = 'indicator_id') %>%
  left_join(key_q12, by = join_by(indicator_id == V1)) %>%
  arrange(PC2) %>%
  select(PC2, V2) %>%
  rename('Loading' = 1, 'Indicator' = 2) %>%
  kable(booktabs = TRUE, caption = 'PC2') %>%
  kable_classic_2(full_width = F)

pca_q12_tt <- pca_q12
rownames(pca_q12_tt$rotation) <- str_extract(key_q12$V2, "^(.*?)(?=\\()|.*")
fviz_pca_var(pca_q12_tt,
             col.var = 'contrib',
             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),
             labelsize = 6,
             repel = TRUE) +
  labs(x = 'PC1', y = 'PC2', colour = 'Contribution', title = '') +
  theme(axis.title = element_text(size = 20),
        axis.text = element_text(size = 20),
        legend.text = element_text(size = 20),
        legend.title = element_text(size = 20))

# Project UOA to PCA
uoa_pc_q12 <- data.frame('PC1' = vector(length = length(shape_panels)),
                         'PC2' = vector(length = length(shape_panels)),
                         'uoa' = shape_panels) %>%
  left_join(key_uoa, by = join_by(uoa == col_name)) %>%
  mutate('subject_2' = case_when(
    uoa %in% humanities_panels ~ 'humanities',
    uoa %in% social_sciences_panels ~ 'social sciences'
  ))

for (i in seq_along(shape_panels)) {
  uoa_pc_q12[i, 'PC1'] <- df_q12$PC1[df_q12[,shape_panels[i]] == 1] %>% mean(na.rm = T)
  uoa_pc_q12[i, 'PC2'] <- df_q12$PC2[df_q12[,shape_panels[i]] == 1] %>% mean(na.rm = T)
}

ggplot(data = uoa_pc_q12, aes(x = PC1, y = PC2, colour = subject_2, label = name)) +
  geom_point(size = 5) +
  geom_text_repel(size = 6) +
  geom_quadrant_lines(linetype = "dotted") +
  scale_x_continuous(limits = symmetric_limits) +
  scale_y_continuous(limits = symmetric_limits) +
  scale_colour_discrete(labels = c('Humanities', 'Social Sciences')) +
  labs(colour = 'Subject') +
  theme_minimal() +
  theme(axis.title = element_text(size = 20),
        axis.text = element_text(size = 20),
        legend.text = element_text(size = 20),
        legend.title = element_text(size = 20))

# Heat map
for (j in seq_along(key_q12$V1)) {
  for (i in seq_along(shape_panels)) {
    uoa_pc_q12[i, key_q12$V1[j]] <- df_q12 %>%
      filter(.[,shape_panels[i]] == 1) %>%
      select(key_q12$V1[j]) %>%
      unlist(recursive = FALSE) %>%
      mean(na.rm = TRUE)
  }
}

pheatmap(uoa_pc_q12 %>%
           select(starts_with('Q12_')) %>%
           rename_with(~key_q12$short, .cols = everything()),
         labels_row = uoa_pc_q12$name,
         scale = "column")

##### Q20 trends - PCA
key_q20 <- key %>%
  filter(startsWith(V1, 'Q20_'))

# Transform to long format
df_q20 <- results %>%
  filter(!is.na(subject_2)) %>%
  pivot_longer(cols = starts_with('Q20_'),
               names_to = 'q20_item',
               values_to = 'q20_value') %>%
  filter(q20_value == 1) %>%
  suppressWarnings()

# Transform to wide format
df_q20 <- df_q20 %>%
  mutate('q20_value' = str_extract(q20_item, "\\d+$") %>% as.numeric(),
         'q20_item' = str_extract(q20_item, "^Q20_\\d+")) %>%
  pivot_wider(id_cols = Q28,
              names_from = q20_item,
              values_from = q20_value)

df_q20 <- df_q20 %>%
  left_join(results %>% select(subject_2, Q28, starts_with('Q7_')), by = join_by(Q28)) %>%
  drop_na(subject_2)

# Perform PCA
pca_q20 <- prcomp(df_q20 %>% select(starts_with('Q20_')), scale. = FALSE)

# Variance plot
var_plot(pca_q20)

# Individual plot
df_q20 <- df_q20 %>%
  mutate('PC1' = pca_q20$x[,'PC1'],
         'PC2' = pca_q20$x[,'PC2'])

ggplot(data = df_q20, aes(x = PC1, y = PC2, colour = subject_2)) +
  geom_point(size = 5) +
  geom_quadrant_lines(linetype = 'dotted') +
  scale_x_continuous(limits = symmetric_limits) +
  scale_y_continuous(limits = symmetric_limits) +
  scale_colour_discrete(labels = c('Humanities', 'Social Sciences')) +
  theme_minimal() +
  labs(colour = 'Subject') +
  theme(axis.title = element_text(size = 20),
        axis.text = element_text(size = 20),
        legend.title = element_text(size = 20),
        legend.text = element_text(size = 20))

t.test(data = df_q20, PC1 ~ subject_2)
t.test(data = df_q20, PC2 ~ subject_2)

# Loadings of PC1
pca_q20$rotation %>%
  as.data.frame() %>%
  select(PC1) %>%
  rownames_to_column(var = 'indicator_id') %>%
  left_join(key_q20, by = join_by(indicator_id == V1)) %>%
  arrange(PC1) %>%
  select(PC1, V2) %>%
  rename('Loading' = 1, 'Indicator' = 2) %>%
  kable(booktabs = TRUE, caption = 'PC1') %>%
  kable_classic_2(full_width = F)

# Loadings of PC2
pca_q20$rotation %>%
  as.data.frame() %>%
  select(PC2) %>%
  rownames_to_column(var = 'indicator_id') %>%
  left_join(key_q20, by = join_by(indicator_id == V1)) %>%
  arrange(PC2) %>%
  select(PC2, V2) %>%
  rename('Loading' = 1, 'Indicator' = 2) %>%
  kable(booktabs = TRUE, caption = 'PC2') %>%
  kable_classic_2(full_width = F)

pca_q20_tt <- pca_q20
rownames(pca_q20_tt$rotation) <- str_extract_all(key_q20$V2, "\\b([A-Z]{2,})\\b") %>%
  lapply(FUN = function (x) {paste0(x, collapse = ' ')})
fviz_pca_var(pca_q20_tt,
             col.var = 'contrib',
             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),
             labelsize = 5,
             repel = TRUE) +
  labs(x = 'PC1', y = 'PC2', colour = 'Contribution', title = '') +
  theme(axis.title = element_text(size = 20),
        axis.text = element_text(size = 20),
        legend.text = element_text(size = 20),
        legend.title = element_text(size = 20))

# Project UOA to PCA
uoa_pc_q20 <- data.frame('PC1' = vector(length = length(shape_panels)),
                         'PC2' = vector(length = length(shape_panels)),
                         'uoa' = shape_panels) %>%
  left_join(key_uoa, by = join_by(uoa == col_name)) %>%
  mutate('subject_2' = case_when(
    uoa %in% humanities_panels ~ 'humanities',
    uoa %in% social_sciences_panels ~ 'social sciences'
  ))

for (i in seq_along(shape_panels)) {
  uoa_pc_q20[i, 'PC1'] <- df_q20$PC1[df_q20[,shape_panels[i]] == 1] %>% mean(na.rm = T)
  uoa_pc_q20[i, 'PC2'] <- df_q20$PC2[df_q20[,shape_panels[i]] == 1] %>% mean(na.rm = T)
}

ggplot(data = uoa_pc_q20, aes(x = PC1, y = PC2, colour = subject_2, label = name)) +
  geom_point(size = 5) +
  geom_text_repel(size = 6) +
  geom_quadrant_lines(linetype = "dotted") +
  scale_x_continuous(limits = symmetric_limits) +
  scale_y_continuous(limits = symmetric_limits) +
  scale_colour_discrete(labels = c('Humanities', 'Social Sciences')) +
  labs(colour = 'Subject') +
  theme_minimal() +
  theme(axis.title = element_text(size = 20),
        axis.text = element_text(size = 20),
        legend.text = element_text(size = 20),
        legend.title = element_text(size = 20))

### Q22 audience - PCA
key_q22 <- key %>%
  filter(startsWith(V1, 'Q22_'))

# Transform to long format
df_q22 <- results %>%
  filter(!is.na(subject_2)) %>%
  pivot_longer(cols = starts_with('Q22_'),
               names_to = 'q22_item',
               values_to = 'q22_value') %>%
  filter(q22_value == 1) %>%
  suppressWarnings()

# Transform to wide format
df_q22 <- df_q22 %>%
  mutate('q22_value' = str_extract(q22_item, "\\d+$") %>% as.numeric(),
         'q22_item' = str_extract(q22_item, "^Q22_\\d+")) %>%
  pivot_wider(id_cols = Q28,
              names_from = q22_item,
              values_from = q22_value)

df_q22 <- df_q22 %>%
  left_join(results %>% select(subject_2, Q28, starts_with('Q7_')), by = join_by(Q28)) %>%
  drop_na(subject_2)

# Perform PCA
pca_q22 <- prcomp(df_q22 %>% select(starts_with('Q22_')), scale. = FALSE)

# Variance plot
var_plot(pca_q22)

# Individual plot
df_q22 <- df_q22 %>%
  mutate('PC1' = pca_q22$x[,'PC1'],
         'PC2' = pca_q22$x[,'PC2'])

ggplot(data = df_q22, aes(x = PC1, y = PC2, colour = subject_2)) +
  geom_point(size = 5) +
  geom_quadrant_lines(linetype = 'dotted') +
  scale_x_continuous(limits = symmetric_limits) +
  scale_y_continuous(limits = symmetric_limits) +
  scale_colour_discrete(labels = c('Humanities', 'Social Sciences')) +
  theme_minimal() +
  labs(colour = 'Subject') +
  theme(axis.title = element_text(size = 20),
        axis.text = element_text(size = 20),
        legend.title = element_text(size = 20),
        legend.text = element_text(size = 20))

t.test(data = df_q22, PC1 ~ subject_2)
t.test(data = df_q22, PC2 ~ subject_2)

# Loadings of PC1
pca_q22$rotation %>%
  as.data.frame() %>%
  select(PC1) %>%
  rownames_to_column(var = 'indicator_id') %>%
  left_join(key_q22, by = join_by(indicator_id == V1)) %>%
  arrange(PC1) %>%
  select(PC1, V2) %>%
  rename('Loading' = 1, 'Indicator' = 2) %>%
  kable(booktabs = TRUE, caption = 'PC1') %>%
  kable_classic_2(full_width = F)

# Loadings of PC2
pca_q22$rotation %>%
  as.data.frame() %>%
  select(PC2) %>%
  rownames_to_column(var = 'indicator_id') %>%
  left_join(key_q22, by = join_by(indicator_id == V1)) %>%
  arrange(PC2) %>%
  select(PC2, V2) %>%
  rename('Loading' = 1, 'Indicator' = 2) %>%
  kable(booktabs = TRUE, caption = 'PC2') %>%
  kable_classic_2(full_width = F)

pca_q22_tt <- pca_q22
rownames(pca_q22_tt$rotation) <- str_extract_all(key_q22$V2, "\\b([A-Z]{2,})\\b") %>%
  lapply(FUN = function (x) {paste0(x, collapse = ' ')})
fviz_pca_var(pca_q22_tt,
             col.var = 'contrib',
             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),
             labelsize = 6,
             repel = TRUE) +
  labs(x = 'PC1', y = 'PC2', colour = 'Contribution', title = '') +
  theme(axis.title = element_text(size = 20),
        axis.text = element_text(size = 20),
        legend.text = element_text(size = 20),
        legend.title = element_text(size = 20))

# Project UOA to PCA
uoa_pc_q22 <- data.frame('PC1' = vector(length = length(shape_panels)),
                         'PC2' = vector(length = length(shape_panels)),
                         'uoa' = shape_panels) %>%
  left_join(key_uoa, by = join_by(uoa == col_name)) %>%
  mutate('subject_2' = case_when(
    uoa %in% humanities_panels ~ 'humanities',
    uoa %in% social_sciences_panels ~ 'social sciences'
  ))

for (i in seq_along(shape_panels)) {
  uoa_pc_q22[i, 'PC1'] <- df_q22$PC1[df_q22[,shape_panels[i]] == 1] %>% mean(na.rm = T)
  uoa_pc_q22[i, 'PC2'] <- df_q22$PC2[df_q22[,shape_panels[i]] == 1] %>% mean(na.rm = T)
}

ggplot(data = uoa_pc_q22, aes(x = PC1, y = PC2, colour = subject_2, label = name)) +
  geom_point(size = 5) +
  geom_text_repel(size = 6) +
  geom_quadrant_lines(linetype = "dotted") +
  scale_x_continuous(limits = symmetric_limits) +
  scale_y_continuous(limits = symmetric_limits) +
  scale_colour_discrete(labels = c('Humanities', 'Social Sciences')) +
  labs(colour = 'Subject') +
  theme_minimal() +
  theme(axis.title = element_text(size = 20),
        axis.text = element_text(size = 20),
        legend.text = element_text(size = 20),
        legend.title = element_text(size = 20))

##### Q18 ICS influence
uoa_q18 <- data.frame('Q18' = vector(length = length(shape_panels)),
                      'uoa' = shape_panels) %>%
  left_join(key_uoa, by = join_by(uoa == col_name)) %>%
  mutate('subject_2' = case_when(
    uoa %in% humanities_panels ~ 'humanities',
    uoa %in% social_sciences_panels ~ 'social sciences'
  ))

for (i in seq_along(shape_panels)) {
  uoa_q18[i, 'Q18'] <- results$Q18[(results[,shape_panels[i]] == 1)[,1]] %>% mean(na.rm = T)
}

results %>%
  group_by(subject_2) %>%
  summarise(mean(Q18, na.rm = T))
mean(results$Q18[!is.na(results$subject_2)], na.rm = T)

ggplot(data = uoa_q18, aes(x = reorder(name, Q18, decreasing = TRUE), y = Q18, fill = subject_2)) +
  geom_col(width = 0.5) +
  scale_fill_discrete(labels = c('Humanities', 'Social Sciences')) +
  scale_y_continuous(limits = c(4,7), oob = rescale_none) +
  coord_flip() +
  labs(x = 'UOA', y = 'Impact Assessment Changes Research in Discipline', fill = 'Subject') +
  theme_bw() +
  theme(axis.title = element_text(size = 20),
        axis.text = element_text(size = 15),
        legend.text = element_text(size = 20),
        legend.title = element_text(size = 20))

##### Q19 interdisciplinary
uoa_q19 <- data.frame('Q19' = vector(length = length(shape_panels)),
                      'uoa' = shape_panels) %>%
  left_join(key_uoa, by = join_by(uoa == col_name)) %>%
  mutate('subject_2' = case_when(
    uoa %in% humanities_panels ~ 'humanities',
    uoa %in% social_sciences_panels ~ 'social sciences'
  ))

df_q19 <- results %>%
   mutate(Q19 = as.numeric(Q19))

for (i in seq_along(shape_panels)) {
  uoa_q19[i, 'Q19'] <- df_q19$Q19[(df_q19[,shape_panels[i]] == 1)[,1]] %>% mean(na.rm = T)
}

df_q19 %>%
  group_by(subject_2) %>%
  summarise(mean(Q19, na.rm = T))
mean(df_q19$Q19[!is.na(df_q19$subject_2)], na.rm = T)

ggplot(data = uoa_q19, aes(x = reorder(name, Q19, decreasing = TRUE), y = Q19, fill = subject_2)) +
  geom_col(width = 0.5) +
  scale_fill_discrete(labels = c('Humanities', 'Social Sciences')) +
  scale_y_continuous() +
  coord_flip() +
  labs(x = 'UOA', y = 'Percentage of Interdisciplinary ICS', fill = 'Subject') +
  theme_bw() +
  theme(axis.title = element_text(size = 20),
        axis.text = element_text(size = 15),
        legend.text = element_text(size = 20),
        legend.title = element_text(size = 20))