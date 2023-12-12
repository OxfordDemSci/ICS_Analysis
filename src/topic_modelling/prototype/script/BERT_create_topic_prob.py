#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 15:25:43 2023

@author: lindali
"""

import pandas as pd
import numpy as np
from bertopic import BERTopic

from sys import argv


# Loading data
model_path = argv[1]
huge_cluster_path = argv[2]
original_df_path = argv[3]
topic_prob_save_to = argv[4]

full_bert = BERTopic.load(model_path)
huge_cluster_bert = BERTopic.load(huge_cluster_path)
df = pd.read_csv(original_df_path)


# Get top X topic probilities of a model for each textual row
def get_top_prob(model, top_n):
    all_probs = []
    for row in model.probabilities_:
        topics = list(range(len(set(full_bert.topics_)))-1)
        prob_dict = {k:v for k,v in zip(topics, list(row))}
        prob_dict = dict(sorted(prob_dict.items(), key=lambda item: item[1], reverse=True)[:top_n])
        if model == huge_cluster_bert:
            prob = [(k+71, v) if k!=-1 else (k,v) for k, v in prob_dict.items()]
        else:
            prob = [(k,v) for k, v in prob_dict.items()]
        prob = [item for sublist in prob for item in sublist]
                
        prob_keys = ["topic_top", "prob_top"] * top_n
        prob_keys_id = np.repeat(list(range(1,top_n+1)),2)
        prob_keys = [str(i)+str(j) for i,j in zip(prob_keys,prob_keys_id)]
        
        prob = {k:v for k,v in zip(prob_keys, prob)}
        all_probs.append(prob)
    
    return all_probs



full_bert_prob = get_top_prob(full_bert,71)
cluster_prob = get_top_prob(huge_cluster_bert,71)

# Replacing -1 topics with huge cluster results
minus_ones = [i for i, e in enumerate(full_bert.topics_) if e == -1]
len(minus_ones)
for (index, replacement) in zip(minus_ones, cluster_prob):
    full_bert_prob[index] = replacement

bert_results_topic_prob = pd.DataFrame.from_records(full_bert_prob)
bert_results_topic_prob['case_id'] =  df[["case_id"]]

bert_results_topic_prob.to_csv(topic_prob_save_to, index = False)



