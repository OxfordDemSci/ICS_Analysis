import os
import re
import csv
import ast
import requests
import spacy.util
import unicodedata
import numpy as np
import pandas as pd
from textblob import TextBlob
from textstat import textstat
from markdown import markdown
from bs4 import BeautifulSoup
from get_dimensions_data import get_dimensions_data, make_paper_level


def get_impact_data(raw_path):
    """ A function to get the raw ICS data"""
    print('Getting ICS Data!')

    url = "https://results2021.ref.ac.uk/impact/export-all"
    r = requests.get(url, allow_redirects=True)
    open(os.path.join(raw_path,  'raw_ref_ics_data.xlsx'), 'wb').write(r.content)

    url = "https://results2021.ref.ac.uk/impact/export-tags-all"
    r = requests.get(url, allow_redirects=True)
    open(os.path.join(raw_path,  'raw_ref_ics_tags_data.xlsx'), 'wb').write(r.content)


def get_environmental_data(raw_path):
    """ A function to get the raw environmental data"""
    print('Getting Environmental Data!')

    url = "https://results2021.ref.ac.uk/environment/export-all"
    r = requests.get(url, allow_redirects=True)
    open(os.path.join(raw_path,  'raw_ref_environment_data.xlsx'), 'wb').write(r.content)


def get_all_results(raw_path):
    """ A function to get the raw results data"""
    print('Getting Results Data!')

    url = "https://results2021.ref.ac.uk/profiles/export-all"
    r = requests.get(url, allow_redirects=True)
    open(os.path.join(raw_path,  'raw_ref_results_data.xlsx'), 'wb').write(r.content)


def get_output_data(raw_path):
    """ A function to get the raw output data"""
    print('Getting Outputs Data!')
    url = "https://results2021.ref.ac.uk/outputs/export-all"
    r = requests.get(url, allow_redirects=True)
    open(os.path.join(raw_path,  'raw_ref_outputs_data.xlsx'), 'wb').write(r.content)


def check_id_overlap(a, b):
    print('Checking ID Overlap!')
    ###Convenience function to check overlap of two lists of ids"""
    print("{} of element in B present in A".format(
        np.mean([i in a for i in b])))
    print("{} of element in A present in B".format(
        np.mean([i in b for i in a])))
    print("{} missing in A but present in B".format(
        [i for i in a if i not in b]))
    print("{} missing in B but present in A".format(
        [i for i in b if i not in a]))


def format_ids(df):
    if 'Institution UKPRN code' in df.columns:
        df = df.rename(
            columns={'Institution UKPRN code': 'inst_id'})
    if 'Institution code (UKPRN)' in df.columns:
        df = df.rename(
            columns={'Institution code (UKPRN)': 'inst_id'})
    df = df.copy()[df['inst_id'] != ' ']
    df = df.astype({'inst_id': 'int'})
    return (df)


def merge_ins_uoa(df1, df2):
    """Function to merge df2 left on df1 based on inst_id and uoa_id"""

    ## [TODO] Add further unit tests on the merge here ##
    assert all(df1['inst_id'].isin(df2['inst_id']))
    assert all(df1['uoa_id'].isin(df2['uoa_id']))

    return (df1.merge(df2, how='left', left_on=['inst_id', 'uoa_id'],
                      right_on=['inst_id', 'uoa_id']))


def clean_ics_level(raw_path, edit_path):
    ## Add stars to ICS level
    print('Cleaning ICS Level Data!')
    raw_ics = pd.read_excel(
        os.path.join(raw_path,
                     'raw_ref_ics_data.xlsx'))
    raw_ics['Title'] = raw_ics['Title'].apply(lambda val: unicodedata. \
                                              normalize('NFKD', str(val)). \
                                              encode('ascii', 'ignore').decode())
    raw_ics = format_ids(raw_ics)
    raw_ics.to_excel(os.path.join(edit_path, 'clean_ref_ics_data.xlsx'))
    return raw_ics


def markdown_to_text(text):
    """
    Convert Markdown-formatted text to plain text.

    Args:
        text (str): Markdown-formatted text.

    Returns:
        A string of plain text.

    """
    # Convert Markdown to HTML.
    html = markdown(text)

    # Parse HTML and return plain text.
    bs = BeautifulSoup(html, features="html.parser")
    return bs.get_text()


def get_urls(text):
    """
    Extract URLs and DOIs from Markdown-formatted text.

    Args:
        text (str): Markdown-formatted text.

    Returns:
        A tuple containing the total number of URLs found, a list of all URLs found, the number of DOI URLs found, and a list of DOI URLs.

    """
    # Find all URLs in the text using a regular expression.
    urls = re.findall(r"\[.*\]\((.*)\)", markdown_to_text(text))

    # Filter the list of URLs to only include DOI URLs.
    doi_urls = [u for u in urls if "doi.org" in u]

    # Return a tuple containing the relevant counts and lists.
    return len(urls), urls, len(doi_urls), doi_urls


def get_isbns(text):
    """
    Extract ISBNs from Markdown-formatted text.

    Args:
        text (str): Markdown-formatted text.

    Returns:
        A tuple containing the total number of ISBNs found and a list of all ISBNs found.

    """
    # Define a regular expression pattern to find ISBNs.
    pattern = r"ISBN(?:-?1[03])?:\s?([-\d ]+)"

    # Find all ISBNs in the text using the regular expression.
    isbns = re.findall(pattern, markdown_to_text(text), re.MULTILINE)

    # Return a tuple containing the relevant counts and lists.
    return len(isbns), isbns


def get_issns(text):
    """
    Extract ISSNs from Markdown-formatted text.

    Args:
        text (str): Markdown-formatted text.

    Returns:
        A tuple containing the total number of ISSNs found and a list of all ISSNs found.

    """
    # Define a regular expression pattern to find ISSNs.
    pattern = r"ISSN:?\s?([-\d ]+)"

    # Find all ISSNs in the text using the regular expression.
    issns = re.findall(pattern, markdown_to_text(text), re.MULTILINE)

    # Return a tuple containing the relevant counts and lists.
    return len(issns), issns


def prepare_spacy():
    """
    Download and load a spaCy language model for English.

    Returns:
        None

    Notes:
        This function sets a global variable `nlp` to the loaded spaCy language model, which can be used for further text processing.
    """
#    global nlp
    model_name = "en_core_web_lg"
    # Check if the spaCy language model is installed, and download it if necessary.
    if not spacy.util.is_package(model_name):
        spacy.cli.download(model_name)
    # Load the spaCy language model into a global variable.
    return spacy.load(model_name)


def count_noun_verb_phrases(text):
    """
    Count the number of noun phrases and verb phrases in a given text.

    Args:
        text (str): The text to analyze.

    Returns:
        A tuple containing the number of noun phrases and the number of verb phrases in the input text.

    """
    nlp = prepare_spacy()
    doc = nlp(markdown_to_text(text))

    # Use list comprehension and generator expression for improved efficiency
    noun_phrase_count = sum(1 for chunk in doc.noun_chunks)
    verb_phrase_count = sum(1 for token in doc if token.pos_ == "VERB")

    return noun_phrase_count, verb_phrase_count


def get_readability_scores(df):
    """
    Calculate the Flesch readability score for each section of text in a pandas DataFrame, as well as a composite score
    for the entire DataFrame.

    Args:
        df (pandas.DataFrame): A DataFrame containing text data.

    Returns:
        A DataFrame with new columns added for the Flesch readability score of each section of text, as well as a
        composite score for the entire DataFrame.

    """
    print('Calculating Readability Scores!')
    section_columns = [
        "1. Summary of the impact",
        "2. Underpinning research",
        "3. References to the research",
        "4. Details of the impact",
        "5. Sources to corroborate the impact",
    ]
    for i, s in zip(range(1, 6), section_columns):
        # Apply the textstat.flesch_reading_ease function to each cell in the current section column of the DataFrame.
        df[f"s{i}_flesch_score"] = df[s].apply(
            lambda x: textstat.flesch_reading_ease(markdown_to_text(x))
        )
    # Calculate the Flesch readability score for the entire DataFrame by concatenating the text of each section
    # and applying the textstat.flesch_reading_ease function to the concatenated text.
    df["flesch_score"] = df.apply(
        lambda x: textstat.flesch_reading_ease(
            "\n".join([x[s] for s in section_columns])
        ),
        axis=1,
    )
    # Return the DataFrame with the new columns added.
    return df


def get_pos_features(df):
    """
    Calculate the number of noun phrases and verb phrases in each section of text in a pandas DataFrame.

    Args:
        df (pandas.DataFrame): A DataFrame containing text data.

    Returns:
        A DataFrame with new columns added for the number of noun phrases and verb phrases in each section of text.
    """
    print('Calculating POS Features')
    section_columns = [
        "1. Summary of the impact",
        "2. Underpinning research",
        "3. References to the research",
        "4. Details of the impact",
        "5. Sources to corroborate the impact",
    ]
    for i, s in zip(range(1, 6), section_columns):
        # Apply the count_noun_verb_phrases function to each cell in the current section column of the DataFrame.
        df[[f"s{i}_np_count", f"s{i}_vp_count"]] = df[s].apply(
            lambda x: pd.Series(count_noun_verb_phrases(x))
        )
    # Return the DataFrame with the new columns added.
    return df


def get_sentiment_score(text):
    """
    Get the sentiment polarity score of a text using TextBlob.

    Args:
        text (str): A string of text to analyze.

    Returns:
        A float representing the sentiment polarity score of the input text, in the range [-1.0, 1.0].
        A score of -1.0 indicates extremely negative sentiment, a score of 1.0 indicates extremely positive sentiment,
        and a score of 0.0 indicates neutral sentiment.

    Raises:
        Nothing.

    Example:
        N/A
    """
    # Convert the input Markdown text to plain text using the markdown_to_text function.
    plain_text = markdown_to_text(text)

    # Create a TextBlob object from the plain text.
    blob = TextBlob(plain_text)

    # Get the sentiment polarity score of the TextBlob object.
    sentiment_score = blob.sentiment_assessments.polarity

    # Return the sentiment polarity score.
    return sentiment_score


def get_sentiment_scores(df):
    """
    Calculate the sentiment score for each section of text in a pandas DataFrame, as well as the overall sentiment score
    for the entire DataFrame.

    Args:
        df (pandas.DataFrame): A DataFrame containing text data.

    Returns:
        A DataFrame with new columns added for the sentiment score of each section of text, as well as the overall
        sentiment score of the DataFrame.

    """
    print('Calculating Sentiment Scores!')
    section_columns = [
        "1. Summary of the impact",
        "2. Underpinning research",
        "3. References to the research",
        "4. Details of the impact",
        "5. Sources to corroborate the impact",
    ]
    # Calculate the sentiment score for each section of text in the DataFrame.
    for i, s in zip(range(1, 6), section_columns):
        df[f"s{i}_sentiment_score"] = df[s].apply(
            lambda x: get_sentiment_score(x)
        )
    # Calculate the overall sentiment score for the DataFrame by concatenating the text from each section and applying
    # the get_sentiment_score function.
    df["sentiment_score"] = df.apply(
        lambda x: get_sentiment_score("\n".join([x[s] for s in section_columns])),
        axis=1,
    )
    # Return the DataFrame with the new columns added.
    return df


    #   - df: DataFrame object, the pickled DataFrame
    df = pandas.read_pickle(
        root_dir.joinpath("data", "merged", "merged_ref_data_exc_output.pkl")
    )

    # Load extra data from a toml file and create a new Pandas DataFrame
    #   - extra_data: dict, the dictionary of extra data
    print('Loading extra country and funder data')
    extra_data = toml.load(
        root_dir.joinpath("src", "clean_data", "extra_data", "ics_country_funder.toml")
    )
    #   - df_extra: DataFrame object, the new DataFrame created from the dictionary
    df_extra = pandas.DataFrame(extra_data["impact case study"])

    print('Merge data')
    # Merge the original DataFrame with the new one based on a common identifier
    #   - df: DataFrame object, the merged DataFrame
    df = pandas.merge(df, df_extra, how="left", on="REF impact case study identifier")
    print('Calculate readability scores')
    df = get_readability_scores(df)
    print('Get part-of-speech features')
    df = get_pos_features(df)
    print('Get sentiment scores')
    df = get_sentiment_scores(df)
    return df


def add_postcodes(df, sup_path):
    print('Add some postcodes!')
    postcodes = pd.read_csv(os.path.join(sup_path, 'ukprn_postcode.csv'))
    df = pd.merge(df, postcodes, how='left', on='inst_id')
    df['inst_postcode_district'] = df['Post Code'].apply(lambda x: x.split(' ')[0])
    df['inst_postcode_area'] = df['inst_postcode_district'].apply(lambda x: x[0:re.search(r"\d", x).start()])
    return df


def add_url(df):
    field = 'REF impact case study identifier'
    df['ics_url'] = df[field].apply(lambda x: 'https://results2021.ref.ac.uk/impact/' + x + '?page=1')
    return df


def get_paths(data_path):
    raw_path = os.path.join(data_path, 'raw')
    edit_path = os.path.join(data_path, 'edit')
    sup_path = os.path.join(data_path, 'supplementary')
    manual_path = os.path.join(data_path, 'manual')
    final_path = os.path.join(data_path, 'final')
    topic_path = os.path.join(data_path, 'topic_model')
    dim_path = os.path.join(data_path, 'dimensions_returns')
    return (raw_path, edit_path, sup_path, manual_path,
            final_path, topic_path, dim_path)


def make_countries_file(manual_path):
    df = pd.read_excel(os.path.join(manual_path,
                                    'funder_countries',
                                    'funders_countries_lookup.xlsx'),
                       sheet_name='funders_countries_lookup',
                       engine='openpyxl'
                       )
    for var in ['suggested_Countries[alpha-3]_change',
                'suggested_Countries[union]_change',
                'suggested_Countries[region]_change']:
        df[var] = df[var].str.strip()

    df['countries_extracted'] = np.where(df['suggested_Countries[alpha-3]_change'].isnull(),
                                         df['Countries[alpha-3]'],
                                         df['suggested_Countries[alpha-3]_change'])
    df['union_extracted'] = np.where(df['suggested_Countries[union]_change'].isnull(),
                                     df['Countries[union]'],
                                     df['suggested_Countries[union]_change'])
    df['region_extracted'] = np.where(df['suggested_Countries[region]_change'].isnull(),
                                      df['Countries[region]'],
                                      df['suggested_Countries[region]_change'])
    df = df[df['countries_extracted'].notnull()]
    df = df[['REF impact case study identifier',
             'countries_extracted',
             'region_extracted',
             'union_extracted']]
    return df


def load_country(df, manual_path):
    print('Loading clean country data')
    country = make_countries_file(manual_path)
    return pd.merge(df, country, how='left', on='REF impact case study identifier')


def make_funder_file(manual_path):
    df = pd.read_excel(os.path.join(manual_path,
                                    'funder_countries',
                                    'funders_countries_lookup.xlsx'),
                       sheet_name='funders_countries_lookup',
                       engine='openpyxl'
                       )
    var = 'suggested_CountriesFunders[full name]_change'
    df = df[['REF impact case study identifier',
             var]]
    df[var] = df[var].str.strip()
    df[var] = np.where(df[var].str.len() < 2 | df[var].isnull(), np.nan, df[var])
    df = df[df[var].notnull()]
    df = df.rename({var: 'funders_extracted'}, axis=1)
    df['funders_extracted'] = df['funders_extracted'].str.replace('EURC', 'EC')
    df['funders_extracted'] = df['funders_extracted'].str.replace('NIHCR', 'NIHR')
    df['funders_extracted'] = df['funders_extracted'].str.replace('LHT', 'LT')
    df['funders_extracted'] = df['funders_extracted'].str.replace('WCT', 'WT')
    return df[['REF impact case study identifier', 'funders_extracted']]


def load_funder(df, manual_path):
    print('Loading clean funder data')
    funder = make_funder_file(manual_path)
    return pd.merge(df, funder, how='left', on='REF impact case study identifier')


def load_dept_vars(df, edit_path):

    print('Loading department variables')

    dept_vars = pd.read_excel(os.path.join(edit_path,
                                           'clean_ref_dep_data.xlsx'),
                              engine='openpyxl')

    dept_vars['ICS_GPA'] = (pd.to_numeric(dept_vars['4*_Impact'], errors='coerce')*4 +
                            pd.to_numeric(dept_vars['3*_Impact'], errors='coerce')*3 +
                            pd.to_numeric(dept_vars['2*_Impact'], errors='coerce')*2 +
                            pd.to_numeric(dept_vars['1*_Impact'], errors='coerce'))/100
    dept_vars['Environment_GPA'] = (pd.to_numeric(dept_vars['4*_Environment'], errors='coerce')*4 +
                                    pd.to_numeric(dept_vars['4*_Environment'], errors='coerce')*3 +
                                    pd.to_numeric(dept_vars['4*_Environment'], errors='coerce')*2 +
                                    pd.to_numeric(dept_vars['4*_Environment'], errors='coerce'))/100
    dept_vars['Output_GPA'] = (pd.to_numeric(dept_vars['4*_Outputs'], errors='coerce')*4 +
                               pd.to_numeric(dept_vars['3*_Outputs'], errors='coerce')*3 +
                               pd.to_numeric(dept_vars['2*_Outputs'], errors='coerce')*2 +
                               pd.to_numeric(dept_vars['1*_Outputs'], errors='coerce'))/100
    dept_vars['Overall_GPA'] = (pd.to_numeric(dept_vars['2*_Overall'], errors='coerce')*4 +
                                pd.to_numeric(dept_vars['2*_Overall'], errors='coerce')*3 +
                                pd.to_numeric(dept_vars['2*_Overall'], errors='coerce')*2 +
                                pd.to_numeric(dept_vars['2*_Overall'], errors='coerce'))/100
    dept_vars = dept_vars[['inst_id',
                           'uoa_id',
                           'fte',
                           'num_doc_degrees_total',
                           'av_income',
                           'tot_income',
                           'tot_inc_kind',
                           'ICS_GPA',
                           'Environment_GPA',
                           'Output_GPA',
                           'Overall_GPA']]
    dept_vars['uoa_id'] = dept_vars['uoa_id'].str.replace('A', '')
    dept_vars['uoa_id'] = dept_vars['uoa_id'].str.replace('B', '')
    dept_vars['uoa_id'] = dept_vars['uoa_id'].astype(int)
    df['Unit of assessment number'] = df['Unit of assessment number'].astype(int)
    return pd.merge(df, dept_vars, how='left',
                    left_on=['inst_id', 'Unit of assessment number'],
                    right_on=['inst_id', 'uoa_id'],
                    ).drop('uoa_id', axis=1)

def load_topic_data(df, manual_path, topic_path):
    print('Loading topic data')
    vars = ['REF impact case study identifier',
            'BERT_topic',
            'BERT_prob',
            'BERT_topic_terms',
            'BERT_topic_term_1',
            'BERT_topic_term_2',
            'BERT_topic_term_3',
            'BERT_topic_term_4',
            'BERT_topic_term_5',
            'BERT_topic_term_6',
            'BERT_topic_term_7',
            'BERT_topic_term_8',
            'BERT_topic_term_9',
            'BERT_topic_term_10',
            'max_prob']
    topic_model = pd.read_excel(os.path.join(topic_path, 'nn3_threshold0.01_reduced.xlsx'),
                                usecols=vars,
                                sheet_name='Sheet1',
                                index_col=None
                                )
    topic_lookup = pd.read_csv(os.path.join(manual_path, 'topic_lookup', 'topic_lookup.csv'),
                               index_col=None)
    topic_lookup = topic_lookup.rename({'description': 'topic_description',
                                        'narrative': 'topic_narrative',
                                        'keywords': 'topic_keywords'}, axis=1)
    df = pd.merge(df, topic_model, how='left', on='REF impact case study identifier')
    df = pd.merge(df, topic_lookup, how='left', left_on='BERT_topic', right_on='topic_id')
    df['cluster_id'] = df['cluster_id'].astype('int', errors='ignore')
    df['topic_id'] = df['topic_id'].astype('int', errors='ignore')

    return df


def make_and_load_tags(df, raw_path, edit_path):
    print('Loading and merging tags!')
    tags = pd.read_excel(os.path.join(raw_path, 'raw_ref_ics_tags_data.xlsx'),
                         sheet_name='Sheet1',
                         skiprows=4,
                         usecols=['REF case study identifier',
                                  'Tag type',
                                  'Tag identifier',
                                  'Tag value',
                                  'Tag group']
                         )
    tags = tags[tags['REF case study identifier'].notnull()]
    with open(os.path.join(edit_path, 'clean_ref_ics_tags_data.csv'), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['REF case study identifier',
                         'Underpinning research subject tag values',
                         'Underpinning research subject tag group',
                         'UK Region tag values',
                         'UK Region tag group'])
        for ics in tags['REF case study identifier'].unique():
            temp = tags[tags['REF case study identifier'] == ics]
            research = temp[temp['Tag type'] == 'Underpinning research subject']
            res_tag_value = []
            for tag in research['Tag value']:
                res_tag_value.append(tag)
            res_tag_group = []
            for tag in research['Tag group']:
                res_tag_group.append(tag)
            region = temp[temp['Tag type'] == 'UK Region']
            reg_tag_value = []
            for tag in region['Tag value']:
                reg_tag_value.append(tag)
            reg_tag_group = []
            for tag in region['Tag group']:
                reg_tag_group.append(tag)
            writer.writerow([ics,
                             res_tag_value, res_tag_group,
                             reg_tag_value, reg_tag_group]
                            )
    tags = pd.read_csv(os.path.join(edit_path, 'clean_ref_ics_tags_data.csv'))
    df = pd.merge(df, tags, how='left',
                  left_on='REF impact case study identifier',
                  right_on='REF case study identifier').drop('REF case study identifier', axis=1)
    return df



def load_scientometric_data(df, dim_path):
    dim_df = pd.read_excel(os.path.join(dim_path, 'merged_dimensions.xlsx'))
    merger = pd.DataFrame(columns=['REF impact case study identifier',
                                   'scientometric_data'])
    index = 0
    for ics in dim_df['Key'].unique():
        counter = 0
        mydict = {}
        ics_df = dim_df[dim_df['Key'] == ics]
        for index in ics_df.index:
            paper = 'Research_' + str(counter)
            mydict[paper] = {}
            try:
                mydict[paper]['dimensions_id'] = ics_df.at[index, 'id']
            except ValueError:
                pass
            try:
                mydict[paper]['title_preferred'] = ics_df.at[index, 'preferred']
            except ValueError:
                pass
            try:
                mydict[paper]['doi'] = ics_df.at[index, 'doi']
            except ValueError:
                pass
            try:
                mydict[paper]['issn'] = ics_df.at[index, 'issn']
            except ValueError:
                pass
            try:
                mydict[paper]['eissn'] = ics_df.at[index, 'eissn']
            except ValueError:
                pass
            try:
                mydict[paper]['type'] = ics_df.at[index, 'type']
            except ValueError:
                pass
            try:
                mydict[paper]['date'] = ics_df.at[index, 'date_normal']
            except ValueError:
                pass
            try:
                mydict[paper]['journal'] = ast.literal_eval(ics_df.at[index, 'journal'])['title']
            except ValueError:
                pass
            try:
                mydict[paper]['Times Cited'] = ics_df.at[index, 'Times Cited']
            except ValueError:
                pass
            try:
                mydict[paper]['Recent Citations'] = ics_df.at[index, 'Recent Citations']
            except ValueError:
                pass
            try:
                mydict[paper]['Field Citation Ratio'] = ics_df.at[index, 'Field Citation Ratio']
            except ValueError:
                pass
            try:
                mydict[paper]['Relative Citation Ratio'] = ics_df.at[index, 'Relative Citation Ratio']
            except ValueError:
                pass
            try:
                mydict[paper]['Altmetric'] = ics_df.at[index, 'Altmetric']
            except ValueError:
                pass
            try:
                mydict[paper]['Abstract'] = ics_df.at[index, 'abstract']
            except ValueError:
                pass
            try:
                mydict[paper]['Authors'] = ics_df.at[index, 'authors']
            except ValueError:
                pass
            try:
                mydict[paper]['Funding'] = ics_df.at[index, 'funder_orgs']
            except ValueError:
                pass
            try:
                mydict[paper]['Concepts,'] = ics_df.at[index, 'concepts']
            except ValueError:
                pass
            try:
                paper_fors = ics_df.at[index, 'category_for']
                if paper_fors is not np.nan:
                    first_level = paper_fors.split('second_level')[0]
                    first_for_set_row = re.findall(r"'name': '(.*?)'", first_level)
                    second_level = paper_fors.split('second_level')[1]
                    second_for_set_row = re.findall(r"'name': '(.*?)'", second_level)
                    mydict[paper]['L1_ANZSRC_FoR'] = first_for_set_row
                    mydict[paper]['L2_ANZSRC_FoR'] = second_for_set_row
            except ValueError:
                pass
            try:
                paper_uoas = ics_df.at[index, 'category_uoa']
                if paper_uoas is not np.nan:
                    uoas = paper_uoas.split('second_level')[0]
                    uoas = re.findall(r"'name': '(.*?)'", uoas)
                    mydict[paper]['Category_UoA'] = uoas
            except ValueError:
                pass
            counter += 1
        merger.at[index, 'REF impact case study identifier'] = ics
        merger.at[index, 'scientometric_data'] = mydict
        index += 1
    return pd.merge(df, merger, how='left', on='REF impact case study identifier')


def return_dim_id(path, filename):
    with open(os.path.join(path, filename), "r") as file:
        return file.readline().strip()


def main():
    data_path = os.path.join(os.getcwd(), '..', '..', 'data')
    my_project_id = return_dim_id(os.path.join(os.getcwd(), '..', '..', 'assets'),
                                  'dimensions_project_id.txt')
    (raw_path, edit_path, sup_path,
     manual_path, final_path, topic_path,
     dim_path) = get_paths(data_path)
    get_environmental_data(raw_path)
    get_impact_data(raw_path)
    get_all_results(raw_path)
    get_output_data(raw_path)
    if (os.path.exists(os.path.join(dim_path, 'doi_returns_dimensions.xlsx')) is False) and\
       (os.path.exists(os.path.join(dim_path, 'isbns_returns_dimensions.xlsx')) is False) and\
       (os.path.exists(os.path.join(dim_path, 'title_returns_dimensions.xlsx')) is False):
        get_dimensions_data(manual_path, dim_path, my_project_id)
    make_paper_level(dim_path)
    df = clean_ics_level(raw_path, edit_path)
    df = get_readability_scores(df)
    df = get_pos_features(df)
    df = get_sentiment_scores(df)
    df = add_postcodes(df, sup_path)
    df = add_url(df)
    df = load_country(df, manual_path)
    df = load_funder(df, manual_path)
    df = load_scientometric_data(df, dim_path)
    df = load_dept_vars(df, edit_path)
    df = load_topic_data(df, manual_path, topic_path)
    df = make_and_load_tags(df, raw_path, edit_path)
    df.to_csv(os.path.join(final_path, 'enhanced_ref_data.csv'), index=False)


if __name__ == "__main__":
    main()
