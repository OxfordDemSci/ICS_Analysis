import numpy as np
import pandas as pd
from nltk.probability import FreqDist
from collections import defaultdict
from nltk.tokenize import word_tokenize
import re
import os
from matplotlib import colors
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.stem.snowball import SnowballStemmer


def set_diag(self, values):
    n = min(len(self.index), len(self.columns))
    self.values[[np.arange(n)] * 2] = values


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap


def get_wordnet_pos(word):
    '''tags parts of speech to tokens
    Expects a string and outputs the string and
    its part of speech'''

    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)


def word_lemmatizer(text):
    '''lemamtizes the tokens based on their part of speech'''
    lemmatizer = WordNetLemmatizer()
    text = lemmatizer.lemmatize(text, get_wordnet_pos(text))
    return text


def reflection_tokenizer(text):
    # @TODO pass in support_path
    stop_list = pd.read_csv(os.path.join(os.getcwd(),# '..', '..', 
                                         'data', 'support',
                                         'custom_stopwords.txt'))
    custom_stop = stop_list['words'].to_list()
    stop = nltk.corpus.stopwords.words('english')
    for word in custom_stop:
        stop.append(word)

    text = re.sub(r'[\W_]+', ' ', text)  # keeps alphanumeric characters
    text = re.sub(r'\d+', '', text)  # removes numbers
    text = text.lower()
    tokens = [word for word in word_tokenize(text)]
    tokens = [word for word in tokens if len(word) >= 3]
    # removes smaller than 3 character
    tokens = [word_lemmatizer(w) for w in tokens]
    tokens = [s for s in tokens if s not in stop]
    return tokens


def make_stopwords(support_path):
    stop_list = pd.read_csv(os.path.join(support_path,
                                         'custom_stopwords.txt'))
    custom_stop = stop_list['words'].to_list()
    stop = nltk.corpus.stopwords.words('english')
    for word in custom_stop:
        stop.append(word)
    return stop


def make_lemmas(df, field, table_path, intermed_path):
    # @TODO should be wrapped outside of pandas to apply
    if os.path.exists(os.path.join(intermed_path, 'data_with_lemmas.csv')) is False:
        print('Lemmas dont exist, lets make them!')
        df['lemmatized_' + field] = df[field].apply(reflection_tokenizer)
        df['lemmatized_' + field] = df['lemmatized_' + field].agg(lambda x: ', '.join(map(str, x)))
        df['lemmatized_' + field] = df['lemmatized_' + field].str.replace(',', '')
        count = df['lemmatized_' + field].apply(lambda x: pd.value_counts(x.split(" ")))
        count = count.sum(axis=0)
        count.sort_values(ascending=False).to_csv(os.path.join(table_path,
                                                               'wordcounts',
                                                               'lemmatized_' + field + '.csv'),
                                                  header=True)
        df.to_csv(os.path.join(intermed_path, 'data_with_lemmas.csv'))
    else:
        print('Computed lemmas already! Unless nothing substantively changed, lets load them in!')
        df = pd.read_csv(os.path.join(intermed_path, 'data_with_lemmas.csv'))
    return df


def freq_dist(df, language, fieldname):
    sentences = '\n'.join(df[fieldname].astype(str).str.lower().tolist())
    en_stemmer = SnowballStemmer(language)
    words = word_tokenize(sentences, language=language)
    counts = FreqDist(en_stemmer.stem(w) for w in words if w.isalnum())
    df_fdist = pd.DataFrame.from_dict(counts, orient='index', columns=['count'])
    df_fdist = df_fdist.sort_values(by='count', ascending=False)
    df_fdist['count'] = (df_fdist['count'] / df_fdist['count'].sum()) * 100
    df_fdist.index = df_fdist.index.str.title() + ': ' + \
                     df_fdist['count'].round(1).astype(str) + '%'
    return df_fdist, df[fieldname].astype(str).str.lower().tolist()


def co_occurrence(sentences, window_size):
    d = defaultdict(int)
    vocab = set()
    for text in sentences:
        # preprocessing (use tokenizer instead)
        text = text.lower().split()
        # iterate over sentences
        for i in range(len(text)):
            token = text[i]
            vocab.add(token)  # add to vocab
            next_token = text[i + 1: i + 1 + window_size]
            for t in next_token:
                key = tuple(sorted([t, token]))
                d[key] += 1

    # formulate the dictionary into dataframe
    vocab = sorted(vocab)  # sort vocab
    df = pd.DataFrame(data=np.zeros((len(vocab), len(vocab)), dtype=np.int16),
                      index=vocab,
                      columns=vocab)
    for key, value in d.items():
        df.at[key[0], key[1]] = value
        df.at[key[1], key[0]] = value
    return df


def clean_free_text(s):
    s = re.sub(r'http\S+', '', s)
    s = s.replace("Summary of the impact", "")
    s = s.replace("indicative maximum 100 words", "")
    s = s.replace("Underpinning research", "")
    s = s.replace("indicative maximum 500 words", "")
    s = s.replace("References to the research", "")
    s = s.replace("indicative maximum of six references", "")
    s = s.replace("Details of the impact", "")
    s = s.replace("indicative maximum 750 words", "")
    s = s.replace("Sources to corroborate the impact ", "")
    return s.strip()


def text_combiner(df):
    df['Text_Combined'] = df['1. Summary of the impact'].astype(str) + \
                          df['2. Underpinning research'].astype(str) + \
                          df['3. References to the research'].astype(str) +\
                          df['4. Details of the impact'].astype(str) +\
                          df['5. Sources to corroborate the impact'].astype(str)
    df['Text_Combined'] = df['Text_Combined'].apply(clean_free_text)
    return df
