#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import torch
import nltk
import re
import pickle as pkl
from collections import defaultdict, Counter
from html import unescape
from sys import argv

from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired




file_path = argv[1]
file_name = argv[2]
category_col = argv[3]

categories_remap = {'Cultural':1,
 'Economic':2,
 'Environmental':3,
 'Health':4,
 'Legal':5,
 'Political':6,
 'Societal':7,
 'Technological':8}


df_sample = pd.read_csv(file_path)
categories = df_sample[category_col].map(categories_remap)


#print(df_sample.head(5))

cols = [ 'lemmatized_1. Summary of the impact',
       'lemmatized_2. Underpinning research',
       'lemmatized_4. Details of the impact']


df_sample['lemmatized_full_text'] = df_sample[cols].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
cols.append('lemmatized_full_text')



with open("./data/support/high_freq_words.txt", "r") as f:
    high_freq_words = f.read()
high_freq_words =  high_freq_words.split("\n")



def remove_high_freq(t):
    t = t.split(" ")
    t = [word for word in t if word not in high_freq_words]
    t = " ".join(t)
    return t

for col in cols:
    df_sample[col+"_no_high_freq"] = df_sample[col].map(remove_high_freq)




cols_for_analysis = [i+"_no_high_freq" for i in cols]

def bert_model_semi_supervised(col, df = df_sample):
    representation_model = KeyBERTInspired()
    topic_model = BERTopic(language="english", calculate_probabilities=True, verbose=True, representation_model=representation_model)
    topics, probs = topic_model.fit_transform(list(df_sample[col]), y=categories)
    return topic_model


col_models = []
for col in cols_for_analysis:
    model = bert_model_semi_supervised(col)
    col_models.append(model)





bert_results = df_sample[["case_id"]]
for i, model in enumerate(col_models):
    col_name = cols_for_analysis[i].split("_")[1]
    bert_results["BERT_topic_"+col_name] = model.topics_
    bert_results["BERT_proba_"+col_name] = [max(i) for i in model.probabilities_]
    model.save(f"./models/{file_name}_original_"+col_name)



bert_results.to_csv(f"ics_data_{file_name}.csv", index = False)



for i, model in enumerate(col_models):
    col_name = cols_for_analysis[i].split("_")[1]
    keywords = pd.DataFrame.from_records(model.get_topics()).T.reset_index()
    keywords.rename({"index":"topic_id"}, axis=1, inplace = True)
    keywords.to_csv(f"./models/{file_name}_keywords_"+col_name+".csv", index = False)






