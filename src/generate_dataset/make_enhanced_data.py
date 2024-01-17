import os
import re
import csv
import ast
import sys
import requests
import spacy.util
import subprocess
import unicodedata
import numpy as np
import pandas as pd

from pathlib import Path
from textblob import TextBlob
from textstat import textstat
from markdown import markdown
from bs4 import BeautifulSoup
from get_dimensions_data import get_dimensions_data, make_paper_level

from pathlib import Path
import requests

def log_row_count(func):
    """
    Decorator to log the number of rows in a DataFrame after applying a function.

    Args:
        func (function): A function that takes a DataFrame as its first argument
                         and returns a DataFrame.

    Returns:
        function: A wrapper function that logs the row count of the DataFrame
                  returned by the input function.
    """
    def wrapper(df, *args, **kwargs):
        # Apply the function
        result = func(df, *args, **kwargs)
        # Print the number of rows
        print(f"Number of rows after {func.__name__}: {len(result)}")
        return result
    return wrapper


def get_impact_data(raw_path):
    """
    Downloads the raw ICS data from a specified URL and saves it to a given path.

    Args:
        raw_path (Path): The directory path where the downloaded data should be saved.

    The function downloads two sets of data related to ICS:
    1. General ICS data.
    2. ICS tags data.
    Both datasets are saved as Excel files in the specified raw_path directory.
    """
    print('Getting ICS Data!')

    url = "https://results2021.ref.ac.uk/impact/export-all"
    r = requests.get(url, allow_redirects=True)
    open(raw_path / 'raw_ref_ics_data.xlsx', 'wb').write(r.content)

    url = "https://results2021.ref.ac.uk/impact/export-tags-all"
    r = requests.get(url, allow_redirects=True)
    open(raw_path / 'raw_ref_ics_tags_data.xlsx', 'wb').write(r.content)


def get_environmental_data(raw_path):
    """
    Downloads the raw environmental data from a specified URL and saves it to a given path.

    Args:
        raw_path (Path): The directory path where the downloaded data should be saved.

    The function downloads environmental data related to REF 2021 and saves it
    as an Excel file in the specified raw_path directory.
    """
    print('Getting Environmental Data!')

    url = "https://results2021.ref.ac.uk/environment/export-all"
    r = requests.get(url, allow_redirects=True)
    open(raw_path / 'raw_ref_environment_data.xlsx', 'wb').write(r.content)


def get_all_results(raw_path):
    """
    Downloads the raw results data from a specified URL and saves it to a given path.

    Args:
        raw_path (Path): The directory path where the downloaded data should be saved.

    This function downloads the REF 2021 profiles data and saves it as an Excel
    file in the specified raw_path directory.
    """
    print('Getting Results Data!')
    url = "https://results2021.ref.ac.uk/profiles/export-all"
    r = requests.get(url, allow_redirects=True)
    open(raw_path / 'raw_ref_results_data.xlsx', 'wb').write(r.content)


def get_output_data(raw_path):
    """
    Downloads the raw output data from a specified URL and saves it to a given path.

    Args:
        raw_path (Path): The directory path where the downloaded data should be saved.

    This function downloads the REF 2021 outputs data and saves it as an Excel
    file in the specified raw_path directory.
    """
    print('Getting Outputs Data!')
    url = "https://results2021.ref.ac.uk/outputs/export-all"
    r = requests.get(url, allow_redirects=True)
    open(raw_path / 'raw_ref_outputs_data.xlsx', 'wb').write(r.content)


def check_id_overlap(a, b):
    """
    Prints the overlap statistics between two lists of IDs.

    Args:
        a (list): The first list of IDs.
        b (list): The second list of IDs.

    This function calculates and prints the percentage of overlap between the two
    lists, and lists the IDs present in one list but missing in the other.
    """
    print('Checking ID Overlap!')
    print("{} of elements in B present in A".format(
        np.mean([i in a for i in b])))
    print("{} of elements in A present in B".format(
        np.mean([i in b for i in a])))
    print("{} missing in A but present in B".format(
        [i for i in a if i not in b]))
    print("{} missing in B but present in A".format(
        [i for i in b if i not in a]))


def format_ids(df):
    """
    Formats the institution IDs within a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing institution ID columns.

    Returns:
        DataFrame: The DataFrame with formatted institution IDs.

    The function renames institution ID columns for consistency, removes rows with
    missing IDs, and formats the IDs as integers. It also combines 'Unit of
    assessment number' and 'Multiple submission letter' into a single 'uoa_id'.
    """
    if 'Institution UKPRN code' in df.columns:
        df = df.rename(columns={'Institution UKPRN code': 'inst_id'})
    if 'Institution code (UKPRN)' in df.columns:
        df = df.rename(columns={'Institution code (UKPRN)': 'inst_id'})
    df = df[df['inst_id'] != ' ']
    df = df.astype({'inst_id': 'int'})
    df['uoa_id'] = df['Unit of assessment number'].astype(int).astype(
        str) + df['Multiple submission letter'].fillna('').astype(str)
    return df


def merge_ins_uoa(df1, df2, id1='inst_id', id2='uoa_id'):
    """
    Merges two DataFrames based on institution and unit of assessment IDs.

    Args:
        df1 (pd.DataFrame): The first DataFrame to merge.
        df2 (pd.DataFrame): The second DataFrame to merge.

    Returns:
        DataFrame: The merged DataFrame.

    The function performs a left merge of df2 on df1 based on 'inst_id' and
    'uoa_id'. It asserts that 'inst_id' and 'uoa_id' in df1 are present in df2.
    """
    assert all(df1[id1].isin(df2[id1]))
    assert all(df1[id2].isin(df2[id2]))

    return df1.merge(df2, how='left', on=[id1, id2])


@log_row_count
def clean_ics_level(raw_path, edit_path):
    """
    Cleans ICS level data and saves the cleaned data to a specified path.

    This function reads the raw ICS data, normalizes the text in the 'Title' column
    to ASCII, formats the IDs using the 'format_ids' function, and saves the cleaned
    data as an Excel file.

    Args:
        raw_path (Path): Path to the directory containing the raw ICS data file.
        edit_path (Path): Path to the directory where the cleaned data file will be saved.

    Returns:
        DataFrame: The cleaned ICS data.
    """
    print('Cleaning ICS Level Data!')
    raw_ics = pd.read_excel(raw_path / 'raw_ref_ics_data.xlsx')
    raw_ics['Title'] = raw_ics['Title'].apply(lambda val: unicodedata. \
                                              normalize('NFKD', str(val)). \
                                              encode('ascii', 'ignore').decode())
    raw_ics = format_ids(raw_ics)
    raw_ics.to_excel(edit_path / 'clean_ref_ics_data.xlsx')
    return raw_ics


def clean_dep_level(raw_path, edit_path):
    """
    Generates a wide scorecard at the department level and merges it with other relevant
    department level data, saving the result to a specified path.

    The function processes raw results, environment doctoral data, research income, and
    in-kind income data. It renames columns, formats IDs, calculates total doctoral degrees,
    and merges all data into a single DataFrame.

    Args:
        raw_path (Path): Path to the directory containing the raw data files.
        edit_path (Path): Path to the directory where the cleaned data file will be saved.

    The function saves the merged department level data as an Excel file in the specified
    edit_path directory.
    """
    print('Cleaning Department Level Data!')
    # Process results data
    raw_results = pd.read_excel(raw_path / 'raw_ref_results_data.xlsx', skiprows=6)
    raw_results = format_ids(raw_results)
    raw_results = raw_results.rename(
        columns={'FTE of submitted staff': 'fte',
                 '% of eligible staff submitted': 'fte_pc'})

    ## Make wide score card by institution and uoa_id
    score_types = ['4*', '3*', '2*', '1*', 'Unclassified'] # types of scores
    wide_score_card = pd.pivot(
        raw_results[['inst_id', 'uoa_id', 'Profile'] + score_types],
        index=['inst_id', 'uoa_id'], columns=['Profile'], values=score_types)
    wide_score_card.columns = wide_score_card.columns.map('_'.join)
    wide_score_card = wide_score_card.reset_index()

    # Process environmental data
    raw_env_path = raw_path / 'raw_ref_environment_data.xlsx'
    # Doctoral data
    raw_env_doctoral = pd.read_excel(raw_env_path, sheet_name="ResearchDoctoralDegreesAwarded", skiprows=4)
    raw_env_doctoral = format_ids(raw_env_doctoral)
    number_cols = [col for col in raw_env_doctoral.columns if 'Number of doctoral' in col]
    raw_env_doctoral['num_doc_degrees_total'] = raw_env_doctoral[number_cols].sum(axis=1)

    # Research income data
    raw_env_income = pd.read_excel(raw_env_path, sheet_name="ResearchIncome", skiprows=4)
    raw_env_income = format_ids(raw_env_income)
    raw_env_income = raw_env_income.\
        rename(columns = {'Average income for academic years 2013-14 to 2019-20': 'av_income',
                          'Total income for academic years 2013-14 to 2019-20': 'tot_income'})
    tot_inc = raw_env_income[raw_env_income['Income source'] == 'Total income']

    # Research income in-kind data
    raw_env_income_inkind = pd.read_excel(raw_env_path, sheet_name="ResearchIncomeInKind", skiprows=4)
    raw_env_income_inkind = format_ids(raw_env_income_inkind)
    raw_env_income_inkind = raw_env_income_inkind.rename(
        columns={'Total income for academic years 2013-14 to 2019-20': 'tot_inc_kind'})

    tot_inc_kind = raw_env_income_inkind.loc[raw_env_income_inkind['Income source']=='Total income-in-kind']

    ## Merge all dept level data together
    raw_dep = merge_ins_uoa(raw_results[['inst_id', 'uoa_id', 'fte', 'fte_pc']].drop_duplicates(),
                             wide_score_card)
    raw_dep = merge_ins_uoa(raw_dep,
                             raw_env_doctoral[['inst_id', 'uoa_id', 'num_doc_degrees_total']])
    raw_dep = merge_ins_uoa(raw_dep,
                             tot_inc[['inst_id', 'uoa_id', 'av_income', 'tot_income']])
    raw_dep = merge_ins_uoa(raw_dep,
                             tot_inc_kind[['inst_id', 'uoa_id', 'tot_inc_kind']])
    raw_dep.to_excel(edit_path / 'clean_ref_dep_data.xlsx')


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


# No longer used.
#def get_isbns(text):
#    """
#    Extract ISBNs from Markdown-formatted text.
#    Args:
#        text (str): Markdown-formatted text.
#    Returns:
#        A tuple containing the total number of ISBNs found and a list of all ISBNs found.
#    """
#    # Define a regular expression pattern to find ISBNs.
#    pattern = r"ISBN(?:-?1[03])?:\s?([-\d ]+)"
#    # Find all ISBNs in the text using the regular expression.
#    isbns = re.findall(pattern, markdown_to_text(text), re.MULTILINE)
#    # Return a tuple containing the relevant counts and lists.
#    return len(isbns), isbns


# No longer used.
#def get_issns(text):
#    """
#    Extract ISSNs from Markdown-formatted text.
#    Args:
#        text (str): Markdown-formatted text.
#
#    Returns:
#        A tuple containing the total number of ISSNs found and a list of all ISSNs found.
#    """
#    # Define a regular expression pattern to find ISSNs.
#    pattern = r"ISSN:?\s?([-\d ]+)"
#
#    # Find all ISSNs in the text using the regular expression.
#    issns = re.findall(pattern, markdown_to_text(text), re.MULTILINE)
#
#    # Return a tuple containing the relevant counts and lists.
#    return len(issns), issns


def prepare_spacy():
    """
    Download and load a spaCy language model for English.

    Returns:
        None

    Notes:
        This function sets a global variable `nlp` to the loaded spaCy
        language model, which can be used for further text processing.
    """
    # global nlp
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


def gen_readability_scores(df, edit_path, section_columns):
    """
    Calculate the Flesch readability score for each section of text in a pandas DataFrame, as well as a composite score
    for the entire DataFrame.

    Args:
        df (pandas.DataFrame): A DataFrame containing text data.

    Returns:
        A DataFrame with new columns added for the Flesch readability score of each section of text, as well as a
        composite score for the entire DataFrame.

    """
    output_path = edit_path / 'ics_readability.csv'

    print('Calculating Readability Scores!')
    col_names = []
    for i, s in zip(range(1, 6), section_columns):
        col_names.append(f"s{i}_flesch_score")
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
    col_names.append('flesch_score')
    col_names.append('REF impact case study identifier')

    print(f"Writing readability scores to {output_path}")

    df[col_names].to_csv(output_path, index=False)


@log_row_count
def get_readability_scores(df, edit_path):
    """
    Load readability scores that have been intermittently saved.

    Args:
        df (pandas.DataFrame): ICS-level DataFrame to which readability scores are merged.
        edit_path (Path): Path where previously generated readability scores are stored.

    Returns:
        pandas.DataFrame: Amended versions of df with readability scores.
    """
    file_path = edit_path / 'ics_readability.csv'

    print('Loading Readability Scores!')
    readability = pd.read_csv(file_path, index_col=None)

    assert len(df) == len(readability)
    assert set(df['REF impact case study identifier']) == set(readability['REF impact case study identifier'])

    return pd.merge(df, readability, on = ['REF impact case study identifier'],
                 how = 'left')


def gen_pos_features(df, edit_path, section_columns):
    """
    Calculate the number of noun phrases and verb phrases in each section of text in a pandas DataFrame.

    Args:
        df (pandas.DataFrame): A DataFrame containing text data.

    Returns:
        A DataFrame with new columns added for the number of noun phrases and verb phrases in each section of text.
    """
    output_path = edit_path / "ics_pos_features.csv"

    print('Calculating POS Features')
    col_names = []
    for i, s in zip(range(1, 6), section_columns):
        col_names.append(f"s{i}_np_count")
        col_names.append(f"s{i}_vp_count")
        # Apply the count_noun_verb_phrases function to each cell in the current section column of the DataFrame.
        df[[f"s{i}_np_count", f"s{i}_vp_count"]] = df[s].apply(
            lambda x: pd.Series(count_noun_verb_phrases(x))
        )

    col_names.append('REF impact case study identifier')

    print(f"Writing pos features to {output_path}")

    df[col_names].to_csv(output_path, index=False)


@log_row_count
def get_pos_features(df, edit_path):
    """
    Load pos features that have been intermittently saved.

    Args:
        df (pandas.DataFrame): ICS-level DataFrame to which pos features are merged.
        edit_path (Path): Path where previously generated pos features are stored.

    Returns:
        pandas.DataFrame: Amended versions of df with pos features.
    """
    file_path = edit_path / 'ics_pos_features.csv'
    print('Loading pos features!')
    pos_features = pd.read_csv(file_path, index_col=None)
    assert len(df) == len(pos_features)
    key = 'REF impact case study identifier'
    assert set(df[key]) == set(pos_features[key])
    return pd.merge(df,
                    pos_features, on=[key],
                    how='left')


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
    """
    # Convert the input Markdown text to plain text using the markdown_to_text function.
    plain_text = markdown_to_text(text)
    # Create a TextBlob object from the plain text.
    blob = TextBlob(plain_text)
    # Get the sentiment polarity score of the TextBlob object.
    sentiment_score = blob.sentiment_assessments.polarity
    # Return the sentiment polarity score.
    return sentiment_score


def gen_sentiment_scores(df, edit_path, section_columns):
    """
    Calculate the sentiment score for each section of text
    in a pandas DataFrame, as well as the overall sentiment
    scorefor the entire DataFrame.

    Args:
        df (pandas.DataFrame): A DataFrame containing text data.

    Returns:
        A DataFrame with new columns added for the sentiment score
        of each section of text, as well as the overall sentiment
        score of the DataFrame.

    """
    output_path = edit_path / "ics_sentiment_scores.csv"

    print('Calculating Sentiment Scores!')
    col_names = []

    # Calculate the sentiment score for each section
    # of text in the DataFrame.
    for i, s in zip(range(1, 6), section_columns):
        col_names.append(f"s{i}_sentiment_score")

        df[f"s{i}_sentiment_score"] = df[s].apply(
            lambda x: get_sentiment_score(x)
        )
    # Calculate the overall sentiment score for the DataFrame
    # by concatenating the text from each section and applying
    # the get_sentiment_score function.
    df["sentiment_score"] = df.apply(
        lambda x: get_sentiment_score("\n".join([x[s] for s in section_columns])),
        axis=1,
    )
    col_names.append("sentiment_score")
    col_names.append("REF impact case study identifier")
    print(f"Writing sentiment scores to {output_path}")
    df[col_names].to_csv(output_path, index=False)


@log_row_count
def get_sentiment_scores(df, edit_path):
    """
    Load sentiment scores that have been intermittently saved.

    Args:
        df (pandas.DataFrame): ICS-level DataFrame to which sentiment scores are merged.
        edit_path (Path): Path where previously generated sentiment scores are stored.

    Returns:
        pandas.DataFrame: Amended versions of df with sentiment scores.
    """
    file_path = edit_path / 'ics_sentiment_scores.csv'
    print('Loading sentiment scores!')
    sentiment_scores = pd.read_csv(file_path, index_col=None)
    assert len(df) == len(sentiment_scores)
    key = 'REF impact case study identifier'
    assert set(df[key]) == set(sentiment_scores[key])
    return pd.merge(df,
                    sentiment_scores,
                    on=[key],
                    how='left')


@log_row_count
def add_postcodes(df, sup_path):
    """
    Adds postcode information to the DataFrame.

    This function merges the given DataFrame with postcode data based on the 'inst_id' column.
    It also extracts and adds postcode district and area to the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to which postcode information will be added.
        sup_path (Path): Path to the directory containing the supplementary data file.

    Returns:
        DataFrame: The DataFrame with added postcode information.
    """
    print('Add some postcodes!')
    postcodes = pd.read_csv(sup_path / 'ukprn_postcode.csv')
    df = pd.merge(df, postcodes, how='left', on='inst_id')
    dist = 'inst_postcode_district'
    area = 'inst_postcode_area'
    df[dist] = df['Post Code'].apply(lambda x: x.split(' ')[0])
    df[area] = df[dist].apply(lambda x: x[0:re.search(r"\d", x).start()])
    return df


@log_row_count
def add_url(df):
    """
    Adds URLs to the DataFrame based on REF impact case study identifiers.

    Args:
        df (pd.DataFrame): The DataFrame to which URLs will be added.

    Returns:
        DataFrame: The DataFrame with added URLs.
    """
    field = 'REF impact case study identifier'
    base = 'https://results2021.ref.ac.uk/impact/'
    df['ics_url'] = df[field].apply(lambda x: base + x + '?page=1')
    return df


def get_paths(data_path):
    """
    Generates paths for various data categories based on a base data path.

    Args:
        data_path (str): The base path for data storage.

    Returns:
        tuple: Paths for raw, edit, supplementary, manual, final, topic model,
               and dimensions return data.
    """
    data_path = Path(data_path)
    raw_path = data_path / 'raw'
    edit_path = data_path / 'edit'
    sup_path = data_path / 'supplementary'
    manual_path = data_path / 'manual'
    final_path = data_path / 'final'
    topic_path = data_path / 'topic_model'
    dim_path = data_path / 'dimensions_returns'
    return (raw_path, edit_path, sup_path, manual_path,
            final_path, topic_path, dim_path)


def make_region_country_list(regions, country_groups):
    """
    Returns countries from region(s) provided

    Args:
        regions (str): Semicolon separated string of region names
        country_groups(pandas dataframe): Lookup table mapping region names to lists of country ISO-3 codes

    Returns:
        str: Semicolon-separated string of country ISO-3 codes
    """

    result = float('NaN')
    if isinstance(regions, str):
        region_list = regions.split('; ')
        i_country_groups = country_groups['Union/region'].isin(region_list)
        country_list = list(set(country_groups[i_country_groups]['ISO3 codes']))
        result = '; '.join(sorted(country_list))
    return(result)


def clean_country_strings(countries):
    """
    Clean semicolon-separated string of country iso-3 codes by sorting, removing duplicates, and dopping nan

    Args:
         countries (str): semicolon-separated string of country iso-3 codes

    Returns:
        str: cleaned semicolon-separted string of country iso-3 codes
    """

    result = float('NaN')
    if isinstance(countries, str):
        countries_list = list(sorted(set(countries.split('; '))))
        countries_list = [x for x in countries_list if 'nan' not in x]
        result = '; '.join(countries_list)
    return(result)


def make_countries_file(manual_path):
    """
    Creates a DataFrame with countries data from an Excel file.

    This function reads an Excel file containing funder countries data, processes
    various columns to extract or replace values, and selects specific columns for output.

    Args:
        manual_path (Path): Path to the manual data directory containing the Excel file.

    Returns:
        DataFrame: A DataFrame containing processed countries data with columns for
                   REF impact case study identifier, countries extracted, region extracted,
                   and union extracted.
    """
    df = pd.read_excel(os.path.join(manual_path,
                                    'funder_countries',
                                    'funders_countries_lookup.xlsx'),
                       sheet_name='funders_countries_lookup',
                       engine='openpyxl'
                       )
    country_groups = pd.read_excel(os.path.join(manual_path,
                                    'funder_countries',
                                    'funders_countries_lookup.xlsx'),
                       sheet_name='country_groups',
                       engine='openpyxl'
                       )
    for var in ['suggested_Countries[alpha-3]_change',
                'suggested_union_change',
                'suggested_Countries[union]_change',
                'suggested_region_change',
                'suggested_Countries[region]_change']:
        df[var] = df[var].str.strip()

    # regions
    df['region_extracted'] = np.where(df['suggested_region_change'].isnull(),
                                      df['region'],
                                      df['suggested_region_change'])
    df['countries_region_extracted'] = \
        [make_region_country_list(regions=x, country_groups=country_groups) for x in list(df['region_extracted'])]

    # unions
    df['union_extracted'] = np.where(df['suggested_union_change'].isnull(),
                                     df['union'],
                                     df['suggested_union_change'])
    df['countries_union_extracted'] = \
        [make_region_country_list(regions=x, country_groups=country_groups) for x in list(df['union_extracted'])]

    # named countries
    df['countries_specific_extracted'] = np.where(df['suggested_Countries[alpha-3]_change'].isnull(),
                                         df['Countries[alpha-3]'],
                                         df['suggested_Countries[alpha-3]_change'])

    # combine all countries
    cols_to_combine = ['countries_specific_extracted', 'countries_union_extracted', 'countries_region_extracted']
    df['countries_extracted'] = df[cols_to_combine].apply(lambda row: '; '.join(row.values.astype('str')), axis=1)

    # clean country columns
    df['countries_extracted'] = df['countries_extracted'].apply(clean_country_strings)
    df['countries_specific_extracted'] = df['countries_specific_extracted'].apply(clean_country_strings)
    df['countries_union_extracted'] = df['countries_union_extracted'].apply(clean_country_strings)
    df['countries_region_extracted'] = df['countries_region_extracted'].apply(clean_country_strings)

    # df = df[df['countries_extracted'].notnull()]
    df = df.dropna(subset=['countries_extracted', 'union_extracted', 'region_extracted'], how='all')
    return df[['REF impact case study identifier',
               'countries_specific_extracted',
               'region_extracted',
               'countries_region_extracted',
               'union_extracted',
               'countries_union_extracted',
               'countries_extracted']]


@log_row_count
def load_country(df, manual_path):
    """
    Loads and merges country data with a given DataFrame.

    Args:
        df (DataFrame): The DataFrame to be merged with country data.
        manual_path (Path): Path to the manual data directory.

    Returns:
        DataFrame: The original DataFrame merged with country data on
                   'REF impact case study identifier'.
    """
    print('Loading clean country data')
    country = make_countries_file(manual_path)
    return pd.merge(df, country, how='left', on='REF impact case study identifier')


def make_funder_file(manual_path):
    """
    Creates a DataFrame with funder data from an Excel file.

    This function reads an Excel file containing funder data, cleans and processes
    specific columns, and selects columns for output.

    Args:
        manual_path (Path): Path to the manual data directory containing the Excel file.

    Returns:
        DataFrame: A DataFrame containing processed funder data with columns for
                   REF impact case study identifier and funders extracted.
    """
    df = pd.read_excel(os.path.join(manual_path, 'funder_countries', 'funders_countries_lookup.xlsx'),
                       sheet_name='funders_countries_lookup', engine='openpyxl')

    var = 'suggested_CountriesFunders[full name]_change'
    df = df[['REF impact case study identifier', var]]
    df[var] = df[var].str.strip()
    df[var] = np.where(df[var].str.len() < 2 | df[var].isnull(), np.nan, df[var])
    df = df[df[var].notnull()]
    df = df.rename({var: 'funders_extracted'}, axis=1)
    df['funders_extracted'] = df['funders_extracted'].str.replace('EURC', 'EC')
    df['funders_extracted'] = df['funders_extracted'].str.replace('NIHCR', 'NIHR')
    df['funders_extracted'] = df['funders_extracted'].str.replace('LHT', 'LT')
    df['funders_extracted'] = df['funders_extracted'].str.replace('WCT', 'WT')
    return df[['REF impact case study identifier', 'funders_extracted']]


@log_row_count
def load_funder(df, manual_path):
    """
    Loads and merges funder data with a given DataFrame.

    This function fetches funder data using the 'make_funder_file' function and merges
    it with the provided DataFrame on the 'REF impact case study identifier'.

    Args:
        df (DataFrame): The DataFrame to be merged with funder data.
        manual_path (Path): Path to the manual data directory.

    Returns:
        DataFrame: The original DataFrame merged with funder data.
    """
    print('Loading clean funder data')
    funder = make_funder_file(manual_path)
    return pd.merge(df, funder, how='left', on='REF impact case study identifier')


@log_row_count
def load_dept_vars(df, edit_path):
    """
    Loads and merges departmental variables with a given DataFrame.

    This function reads departmental data from an Excel file and calculates various GPA
    metrics. It then merges these metrics with the provided DataFrame based on institution
    and unit of assessment IDs.

    Args:
        df (DataFrame): The DataFrame to be enriched with departmental variables.
        edit_path (Path): Path to the directory containing the cleaned departmental data file.

    Returns:
        DataFrame: The original DataFrame merged with departmental variables.
    """
    print('Loading department variables')
    dept_vars = pd.read_excel(edit_path / 'clean_ref_dep_data.xlsx', engine='openpyxl')

    # Calculate GPA metrics
    dept_vars['ICS_GPA'] = (pd.to_numeric(dept_vars['4*_Impact'], errors='coerce') * 4 +
                            pd.to_numeric(dept_vars['3*_Impact'], errors='coerce') * 3 +
                            pd.to_numeric(dept_vars['2*_Impact'], errors='coerce') * 2 +
                            pd.to_numeric(dept_vars['1*_Impact'], errors='coerce')) / 100
    dept_vars['Environment_GPA'] = (pd.to_numeric(dept_vars['4*_Environment'], errors='coerce') * 4 +
                                    pd.to_numeric(dept_vars['3*_Environment'], errors='coerce') * 3 +
                                    pd.to_numeric(dept_vars['2*_Environment'], errors='coerce') * 2 +
                                    pd.to_numeric(dept_vars['1*_Environment'], errors='coerce')) / 100
    dept_vars['Output_GPA'] = (pd.to_numeric(dept_vars['4*_Outputs'], errors='coerce') * 4 +
                               pd.to_numeric(dept_vars['3*_Outputs'], errors='coerce') * 3 +
                               pd.to_numeric(dept_vars['2*_Outputs'], errors='coerce') * 2 +
                               pd.to_numeric(dept_vars['1*_Outputs'], errors='coerce')) / 100
    dept_vars['Overall_GPA'] = (pd.to_numeric(dept_vars['4*_Overall'], errors='coerce') * 4 +
                                pd.to_numeric(dept_vars['3*_Overall'], errors='coerce') * 3 +
                                pd.to_numeric(dept_vars['2*_Overall'], errors='coerce') * 2 +
                                pd.to_numeric(dept_vars['1*_Overall'], errors='coerce')) / 100

    # Select required columns
    dept_vars = dept_vars[['inst_id', 'uoa_id', 'fte', 'num_doc_degrees_total', 'av_income', 'tot_income',
                           'tot_inc_kind', 'ICS_GPA', 'Environment_GPA', 'Output_GPA', 'Overall_GPA']]

    return pd.merge(df, dept_vars, how='left', left_on=['inst_id', 'uoa_id'], right_on=['inst_id', 'uoa_id']).drop('uoa_id', axis=1)


@log_row_count
def load_topic_data(df, manual_path, topic_path):
    """
    Loads and merges topic modeling data with a given DataFrame.

    This function reads topic modeling data from an Excel file and merges it with the
    provided DataFrame. It also merges topic reassignment and lookup data if available.

    Args:
        df (DataFrame): The DataFrame to be enriched with topic modeling data.
        manual_path (Path): Path to the directory containing manual topic data.
        topic_path (Path): Path to the directory containing the topic model data file.

    Returns:
        DataFrame: The original DataFrame merged with topic modeling data.
    """
    print('Loading topic data')
    topic_model_path = topic_path / 'nn3_threshold0.01_reduced.xlsx'

    if not topic_model_path.exists():
        print(f"File not found: {topic_model_path}")
        print("WARNING: Not including topic model data columns.")
        print("Returning original file")
        return df


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

    topic_model = pd.read_excel(topic_model_path, usecols=vars, sheet_name='Sheet1', index_col=None)

    # Attempt to load additional topic data
    try:
        topic_assignment = pd.read_csv(manual_path / 'topic_lookup' / 'topic_reassignment.csv',
                                       index_col=None)
    except FileNotFoundError:
        print(f"{manual_path / 'topic_lookup' / 'topic_reassignment.csv'} not found!")
        print("WARNING: Not including topic reassignment data.")

    try:
        topic_lookup = pd.read_csv(manual_path / 'topic_lookup' / 'topic_lookup.csv',
                                   index_col=None,
                                   encoding='cp1252'
                                   )
    except FileNotFoundError:
        print(f"{manual_path / 'topic_lookup' / 'topic_lookup.csv'} not found!")
        print("WARNING: Not including topic lookup data.")
        return df

    topic_lookup = topic_lookup.rename({'description': 'topic_description', 'narrative': 'topic_narrative'}, axis=1)

    try:
        assert set(df['REF impact case study identifier']) == set(topic_model['REF impact case study identifier'])
    except AssertionError:
        print("AssertionError: not all ICSs have an associated topic")

    df = pd.merge(df, topic_model, how='left', on='REF impact case study identifier')
    df = pd.merge(df, topic_assignment, how='left', on='REF impact case study identifier')
    df = pd.merge(df, topic_lookup, how='left', left_on='final_topic', right_on='topic_id')
    df['cluster_id'] = df['cluster_id'].astype('int', errors='ignore')
    df['topic_id'] = df['topic_id'].astype('int', errors='ignore')

    return df


@log_row_count
def make_and_load_tags(df, raw_path, edit_path):
    """
    Loads, processes, and merges tag data with a given DataFrame.

    This function reads tag data from an Excel file, processes it into a CSV file,
    and then merges it with the provided DataFrame.

    Args:
        df (DataFrame): The DataFrame to be enriched with tag data.
        raw_path (Path): Path to the directory containing the raw tag data file.
        edit_path (Path): Path to the directory where the processed tag data will be saved.

    Returns:
        DataFrame: The original DataFrame merged with processed tag data.
    """
    print('Loading and merging tags!')
    tags = pd.read_excel(raw_path / 'raw_ref_ics_tags_data.xlsx',
                         sheet_name='Sheet1',
                         skiprows=4,
                         usecols=['REF case study identifier',
                                  'Tag type',
                                  'Tag identifier',
                                  'Tag value',
                                  'Tag group']
                         )
    tags = tags[tags['REF case study identifier'].notnull()]

    # Process tags into a CSV file
    with open(edit_path / 'clean_ref_ics_tags_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['REF case study identifier',
                         'Underpinning research subject tag values',
                         'Underpinning research subject tag group',
                         'UK Region tag values',
                         'UK Region tag group'])

        # Tag processing logic
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

    tags = pd.read_csv(edit_path / 'clean_ref_ics_tags_data.csv')
    return pd.merge(df,
                    tags,
                    how='left',
                    left_on='REF impact case study identifier',
                    right_on='REF case study identifier').drop('REF case study identifier', axis=1)


@log_row_count
def load_scientometric_data(df, dim_path):
    """
    Loads, processes, and merges scientometric data with a given DataFrame.

    This function reads tag data from an Excel file, processes it into a CSV file,
    and then merges it with the provided DataFrame.

    Args:
        df (DataFrame): The DataFrame to be enriched with tag data.
        dim_path (Path): Path to the directory containing the dimensions data.

    Returns:
        DataFrame: The original DataFrame merged with processed dimensions data.
    """
    print("Loading scientometric data")
    file_path = dim_path / 'merged_dimensions.xlsx'
    if not file_path.exists():
        print(f"File not found: {file_path}")
        print("WARNING: Not including scientometric data columns.")
        print("Returning original file")
        return df

    dim_df = pd.read_excel(file_path)
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
            for key, value in {'dimensions_id': 'id',
                               'title_preferred': 'preferred',
                               'doi':'doi',
                               'issn': 'issn',
                               'eissn': 'eissn',
                               'Field of Research': 'category_for',
                               'Unit of Assessment': 'category_uoa',
                               'type': 'type',
                               'date': 'date_normal',
                               'Times Cited': 'Times Cited',
                               'Recent Citations':'Recent Citations',
                               'Field Citation Ratio': 'Field Citation Ratio',
                               'Relative Citation Ratio': 'Relative Citation Ratio',
                               'Altmetric': 'Altmetric',
                               'Abstract': 'abstract',
                               'Authors': 'authors',
                               'Funding': 'funder_orgs',
                               'Open Access': 'open_access_categories_v2',
                               'Researcher Cities': 'research_org_cities',
                               'Researcher Countries': 'research_org_countries'
                               }.items():
                try:
                    mydict[paper][key] = ics_df.at[index, value]
                except ValueError:
                    pass
            try:
                mydict[paper]['journal'] = ast.literal_eval(ics_df.at[index, 'journal'])['title']
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
    """
    Loads and returns the project ID from a file

    Args:
        path (Path): Path to the directory containing the file.
        filename (str): Name of file to read.

    Returns:
        str: Stripped first line.
    """
    with open(path / filename, "r") as file:
        return file.readline().strip()


if __name__ == "__main__":
    # This will get the directory where the script is located
    current_file = Path(__file__).resolve()
    project_root = current_file.parent
    while not (project_root / '.git').exists():
        project_root = project_root.parent

    data_path = project_root / 'data'

    (raw_path, edit_path, sup_path,
     manual_path, final_path, topic_path,
     dim_path) = get_paths(data_path)

    csv_out = [arg for arg in sys.argv if '.csv' in arg]

    if csv_out:
        output_path = csv_out[0]
        print(f"Will write final dataset to provided path: {output_path}")
        write = True
    else:
        output_path = final_path / 'enhanced_ref_data.csv'
        if not (final_path / 'enhanced_ref_data.csv').exists():
            ## Standard output file does not exist yet
            print(f"Will write final dataset to default path: {output_path}")
            write = True
        else:
            ## Path not provided but output file already exists
            if ('-f' in sys.argv):
                print(f"WARNING: Will force overwrite dataset at default path: {output_path}")
                write = True
            else:
                print("WARNING: Not overwriting final dataset as file already exists.\n" +
                        "Use -f to force overwrite or provide a custom path.\n" +
                        "Only intermittent files will be generated and saved.")
                write = False

    if not os.path.exists(raw_path):
        os.makedirs(raw_path, exist_ok=True)
    if not (raw_path / 'raw_ref_environment_data.xlsx').exists():
        get_environmental_data(raw_path)
    if not ((raw_path / 'raw_ref_ics_tags_data.xlsx').exists() and\
        (raw_path / 'raw_ref_ics_data.xlsx').exists()):
        get_impact_data(raw_path)
    if not (raw_path / 'raw_ref_results_data.xlsx').exists():
        get_all_results(raw_path)
    if not (raw_path / 'raw_ref_outputs_data.xlsx').exists():
        get_output_data(raw_path)

    clean_dep_level(raw_path, edit_path)
    df = clean_ics_level(raw_path, edit_path)
    df = load_dept_vars(df, edit_path)
    df = add_postcodes(df, sup_path)
    df = add_url(df)
    df = load_country(df, manual_path)
    df = load_funder(df, manual_path)
    df = make_and_load_tags(df, raw_path, edit_path)
    if '-bq' in sys.argv:
        ## Generate new dimensions data
        print("Generating new Dimensions data... This will take some time.")
        my_project_id = return_dim_id(project_root / 'assets',
                                      'dimensions_project_id.txt')
        if not ((dim_path / 'doi_returns_dimensions.xlsx').exists() and\
                (dim_path / 'isbns_returns_dimensions.xlsx').exists() and\
                (dim_path / 'title_returns_dimensions.xlsx').exists()):
            get_dimensions_data(manual_path, dim_path, my_project_id)
        else:
            if '-bqf' in sys.argv:
                print('Getting new Dimensions data')
                get_dimensions_data(manual_path, dim_path, my_project_id)
            else:
                print("Dimensions data already found, skipping collection " +
                      "(use -bqf to force new collection)." +
                      " Just generating paper level data from the dimensions data.")
        make_paper_level(dim_path)

    df = load_scientometric_data(df, dim_path)

    if '-top' in sys.argv:
        ## Generate new topic model
        print("Generating new topic model... This will take some time.")
        bert_script_path = project_root / 'topic_modelling' / 'bert.py'
        run_args = [
            edit_path / 'clean_ref_ics_data.xlsx',
            topic_path]

        run_command = ["python3", bert_script_path] + run_args
        subprocess.run(run_command)

        print("Reducing topic model... This will take some time.")
        reduce_script_path = project_root / 'topic_modelling' / 'bert_reduce.py'
        reduce_args = [
            topic_path,
            'nn3_threshold0.01']

        reduce_command = ["python3", bert_script_path] + reduce_args
        subprocess.run(reduce_command)

    df = load_topic_data(df, manual_path, topic_path)

    if '-tm' in sys.argv:
        print("Generating new text-mining data... This will take some time.")
        section_columns = [
            "1. Summary of the impact",
            "2. Underpinning research",
            "3. References to the research",
            "4. Details of the impact",
            "5. Sources to corroborate the impact"]

        gen_readability_scores(df, edit_path, section_columns)
        gen_pos_features(df, edit_path, section_columns)
        gen_sentiment_scores(df, edit_path, section_columns)

    df = get_readability_scores(df, edit_path)
    df = get_pos_features(df, edit_path)
    df = get_sentiment_scores(df, edit_path)

    if write:
        df.to_csv(output_path, index=False)
