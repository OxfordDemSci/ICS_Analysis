#!/usr/bin/env python
# coding: utf-8


import pandas as pd
from text_helpers import *

from sys import argv

from nltk import ngrams
import csv


df_path = argv[1]
output_file = argv[2]

ics_df = pd.read_excel(df_path)

# filter out SHAPE only
ics_df_sample = ics_df[(ics_df['Main panel'] == 'C')|(ics_df['Main panel'] == 'D')|(ics_df['Unit of assessment number'] == 4)]



ics_df_sample[['Unit of assessment number']].to_csv("unit_of_assessment.csv", index = False)


columns_needed = ['REF impact case study identifier', 'Main panel',	'Unit of assessment number', 'Summary impact type' 
                  ,'1. Summary of the impact',	'2. Underpinning research', '3. References to the research',
                  '4. Details of the impact', '5. Sources to corroborate the impact']

columns_for_analysis = ['1. Summary of the impact',	'2. Underpinning research', '3. References to the research',
                  '4. Details of the impact', '5. Sources to corroborate the impact']

ics_df = ics_df[columns_needed]
ics_df['case_id'] = ics_df['REF impact case study identifier']


ics_df_non_SHAPE = ics_df[(ics_df['Main panel'] != 'C')&(ics_df['Main panel'] != 'D')&(ics_df['Unit of assessment number'] != 4)]


# Filtering stopwords
stopwords = make_stopwords("./data/support")


# Clean but not lemmatize 
ics_df_sample = generate_cleaned_text_and_count(ics_df_sample, columns_for_analysis, clean_text, None, "cleaned_", False)

# Clean and lemmatize
ics_df_sample = generate_cleaned_text_and_count(ics_df_sample, columns_for_analysis, clean_and_lemmatize, "./data", "lemmatized_new_sample_")


ics_df_sample.to_csv(output_file + ".csv", index = False)


ics_df_non_SHAPE = generate_cleaned_text_and_count(ics_df_non_SHAPE, columns_for_analysis,clean_and_lemmatize, "./data", "lemmatized_new_")



ics_df_non_SHAPE.to_csv(output_file + "_non_SHAPE.csv", index = False)


ics_df = pd.concat([ics_df_sample, ics_df_non_SHAPE], ignore_index=True)
ics_df.to_csv(output_file + "_full.csv", index = False)



# Generating n-grams 
def generate_ngrams(df, path):
    for i in range(2,5):
        for col in columns_for_analysis:
            text = list(df['lemmatized_'+col])
            n_grams = [ngrams(sequence=nltk.word_tokenize(t), n = i) for t in text]
            # save n_grams to csv
            with open(f'{path}/sample_{col}_{i}grams.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['n_gram'])
                for ngram in n_grams:
                    for gram in ngram:
                        writer.writerow(gram)
            print(f"{col} {i} gram finished")
    return


#generate_ngrams(ics_df_sample, "./data/ngrams")

