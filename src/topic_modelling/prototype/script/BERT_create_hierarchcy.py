#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 15:25:43 2023

@author: lindali
"""

import pandas as pd
import numpy as np
from bertopic import BERTopic
from scipy.cluster import hierarchy as sch

from sys import argv
from sklearn.metrics.pairwise import cosine_similarity


# Loading data
model_path = argv[1]
huge_cluster_path = argv[2]
original_df_path = argv[3]
huge_cluster_df_path = argv[4]


full_bert = BERTopic.load(model_path)
huge_cluster_bert = BERTopic.load(huge_cluster_path)
df = pd.read_csv(original_df_path)
huge_cluster_df = pd.read_csv(huge_cluster_df_path)


# Get hierarchy
linkage_function = lambda x: sch.linkage(x, 'single', optimal_ordering=True)
full_hierarchical = full_bert.hierarchical_topics(df['lemmatized_full_text_no_high_freq'])
full_hierarchical.to_csv("SHAPE_bert_model_hierarchy.csv", index = False)

cluster_hierarchical = huge_cluster_bert.hierarchical_topics(huge_cluster_df['lemmatized_full_text_no_high_freq'])
cluster_hierarchical.to_csv("SHAPE_huge_cluster_bert_model_hierarchy.csv", index = False)

# Create distance matrix
def get_distance_matrix(bert_model):
    distance_matrix = cosine_similarity(np.array(bert_model.topic_embeddings_)[1:, :])
    labels = (full_bert.get_topic_info().sort_values("Topic", ascending=True).Name)[1:]
    distance = pd.DataFrame(distance_matrix, columns = labels).set_index(labels)
    return distance


distance_full = get_distance_matrix(full_bert)
distance_cluster = get_distance_matrix(huge_cluster_bert)

distance_full.to_csv("SHAPE_bert_model_without_huge_cluster_distance_matrix.csv")
distance_cluster.to_csv("SHAPE_bert_model_huge_cluster_distance_matrix.csv")





