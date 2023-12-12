#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired

from sys import argv




# Reading in file (as in parameter)
df_path = argv[1]
result_output_path = argv[2]
keyword_output_path = argv[3]
model_output_path = argv[4]

df_sample = pd.read_csv(df_path)



# Joining text

cols = ['lemmatized_1. Summary of the impact',
       'lemmatized_2. Underpinning research',
       'lemmatized_4. Details of the impact']

cols_full = [ 'cleaned_1. Summary of the impact',
       'cleaned_2. Underpinning research',
       'cleaned_4. Details of the impact']

df_sample['lemmatized_full_text'] = df_sample[cols].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
df_sample['cleaned_full_text'] = df_sample[cols_full].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)




# Reading in model-specific stopwords filtered maunally 
with open("./data/support/high_freq_words.txt", "r") as f:
    high_freq_words = f.read()
high_freq_words =  high_freq_words.split("\n")


# Filtering stopwords
def remove_high_freq(t):
    t = t.split(" ")
    t = [word for word in t if word not in high_freq_words]
    t = " ".join(t)
    return t
df_sample['lemmatized_full_text_no_high_freq'] = df_sample['lemmatized_full_text'].map(remove_high_freq)


# Creating the first batch of model
def bert_model(col, df = df_sample):
    representation_model = KeyBERTInspired()
    topic_model = BERTopic(language="english", calculate_probabilities=True, verbose=True, representation_model=representation_model)
    topics, probs = topic_model.fit_transform(list(df[col]))
    return topic_model


full_bert = bert_model('lemmatized_full_text_no_high_freq')

bert_results = df_sample[["case_id", "lemmatized_full_text_no_high_freq"]]
bert_results["BERT_topic_full"] = full_bert.topics_
bert_results["BERT_proba_full"] = [max(i) for i in full_bert.probabilities_]



# Re-model the huge cluster (those with a topic == -1, or not classified by bert)
huge_cluster = bert_results[bert_results.BERT_topic_full == -1]

huge_cluster_bert = bert_model('lemmatized_full_text_no_high_freq', huge_cluster)




bert_results_cluster = huge_cluster[["case_id"]]
bert_results_cluster["BERT_topic_full_cluster"] = [i+71 if i != -1 else -1 for i in huge_cluster_bert.topics_]
bert_results_cluster["BERT_proba_full_cluster"] = [max(i) for i in huge_cluster_bert.probabilities_]



bert_results = bert_results.merge(bert_results_cluster, how = 'left', on = "case_id", copy = False)




bert_results_cleaned = bert_results.copy()



bert_results_cleaned['BERT_proba_full'] = np.where(bert_results_cleaned['BERT_topic_full'] == -1, 
                                                           bert_results_cleaned['BERT_proba_full_cluster'], 
                                                           bert_results_cleaned['BERT_proba_full'])
bert_results_cleaned['BERT_topic_full'] = np.where(bert_results_cleaned['BERT_topic_full'] == -1, 
                                                           bert_results_cleaned['BERT_topic_full_cluster'], 
                                                           bert_results_cleaned['BERT_topic_full'])


bert_results_cleaned.drop(columns = ['BERT_topic_full_cluster','BERT_proba_full_cluster','lemmatized_full_text_no_high_freq'], inplace = True)


bert_results = bert_results.merge(bert_results_cleaned,  how = 'left', on = "case_id", copy = False)


bert_results.to_csv(result_output_path, index = False)




# Creating and writing keyword tables to file

keywords = pd.DataFrame.from_records(full_bert.get_topics()).T.reset_index()
keywords.rename({"index":"topic_id"}, axis=1, inplace = True)

keywords_cluster = pd.DataFrame.from_records(huge_cluster_bert.get_topics()).T.reset_index()
keywords_cluster.rename({"index":"topic_id"}, axis=1, inplace = True)
keywords_cluster['topic_id'] = [i+71 if i != -1 else -1 for i in keywords_cluster.topic_id]

keywords = pd.concat([keywords, keywords_cluster],ignore_index=True)


keywords.to_csv(keyword_output_path, index = False)



# Saving models
full_bert.save(model_output_path)
huge_cluster_bert.save(f"{model_output_path}_huge_cluster")







