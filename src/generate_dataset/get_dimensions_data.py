import re
import os
import ast
import traceback
import numpy as np
import pandas as pd
from google.cloud import bigquery


def how_much_dim_matched(df, object_type):
    """
        Calculates the percentage of direct matches for a specific object type in a DataFrame.

        Parameters:
        - df (pandas.DataFrame): The DataFrame containing data to analyze.
        - object_type (str): The type of object for which the matching percentage is calculated.

        Returns:
        None

        Prints:
        - Percentage of direct matches for the specified object type in the DataFrame.
        - Number of direct matches for the specified object type in the DataFrame.
    """
    print(f'We can directly {object_type} match: ',
          round(len(df[df['id'].notnull()]) / len(df), 3))
    print(object_type + ' returns: ',
          len(df[df['id'].notnull()]))


def make_paper_level(dim_out: str) -> None:
    """
    Merge Dimensions Data into paper level and calculate citation metrics.

    Parameters:
    - dim_out (str): The path to the directory where Dimensions data is stored.

    Returns:
    None

    The function reads Dimensions data files for DOI, ISBN, and Title, performs
    merging and deduplication, calculates citation metrics, and saves the merged
    data with metrics to an Excel file.

    Example:
    >>> make_paper_level('/path/to/dimensions_data')
    Merging Dimensions Data into paper level!
    Saving merged data to '/path/to/dimensions_data/merged_dimensions.xlsx'.
    """
    doi_df = pd.read_excel(os.path.join(dim_out, 'doi_returns_dimensions.xlsx'),
                           engine='openpyxl'
                           )
    isbn_df = pd.read_excel(os.path.join(dim_out, 'isbns_returns_dimensions.xlsx'),
                            engine='openpyxl'
                            )
    title_df = pd.read_excel(os.path.join(dim_out, 'title_returns_dimensions.xlsx'),
                             engine='openpyxl'
                             )
    how_much_dim_matched(doi_df, 'DOI')
    how_much_dim_matched(isbn_df, 'ISBN')
    how_much_dim_matched(title_df, 'Title')
    merged_df = pd.concat([doi_df, isbn_df, title_df])
    merged_df = merged_df.drop_duplicates(subset=['Key', 'id'])
    merged_df = merged_df[merged_df['id'].notna()]
    merged_df = merged_df.sort_values(by='Key')
    for index in merged_df.index:
        met = merged_df['metrics'][index]
        if isinstance(met, str):
            try:
                met_dict = ast.literal_eval(met)
                if 'times_cited' in met_dict:
                    merged_df.loc[index, 'Times Cited'] = met_dict['times_cited']
                else:
                    # Handle the case when 'times_cited' key is not present in the dictionary
                    merged_df.loc[index, 'Times Cited'] = 0
            except (SyntaxError, ValueError):
                # Handle the case when 'met' is not a valid dictionary string
                merged_df.loc[index, 'Times Cited'] = 0
            try:
                met_dict = ast.literal_eval(met)
                if 'recent_citations' in met_dict:
                    merged_df.loc[index, 'Recent Citations'] = met_dict['recent_citations']
                else:
                    # Handle the case when 'times_cited' key is not present in the dictionary
                    merged_df.loc[index, 'Recent Citations'] = 0
            except (SyntaxError, ValueError):
                # Handle the case when 'met' is not a valid dictionary string
                merged_df.loc[index, 'Recent Citations'] = 0
            try:
                met_dict = ast.literal_eval(met)
                if 'field_citation_ratio' in met_dict:
                    merged_df.loc[index, 'Field Citation Ratio'] = met_dict['field_citation_ratio']
                else:
                    # Handle the case when 'times_cited' key is not present in the dictionary
                    merged_df.loc[index, 'Field Citation Ratio'] = 0
            except (SyntaxError, ValueError):
                # Handle the case when 'met' is not a valid dictionary string
                merged_df.loc[index, 'Field Citation Ratio'] = 0
            try:
                met_dict = ast.literal_eval(met)
                if 'relative_citation_ratio' in met_dict:
                    merged_df.loc[index, 'Relative Citation Ratio'] = met_dict['relative_citation_ratio']
                else:
                    # Handle the case when 'times_cited' key is not present in the dictionary
                    merged_df.loc[index, 'Relative Citation Ratio'] = 0
            except (SyntaxError, ValueError):
                # Handle the case when 'met' is not a valid dictionary string
                merged_df.loc[index, 'Relative Citation Ratio'] = 0
        else:
            merged_df.loc[index, 'Times Cited'] = 0
            merged_df.loc[index, 'Recent Citations'] = 0
            merged_df.loc[index, 'Field Citation Ratio'] = 0
            merged_df.loc[index, 'Relative Citation Ratio'] = 0
        try:
            alt = merged_df['altmetrics'][index]
            merged_df.loc[index, 'Altmetric'] = ast.literal_eval(alt)['score']
        except (SyntaxError, ValueError):
            merged_df.loc[index, 'Altmetric'] = 0
    merged_df['Times Cited'] = merged_df['Times Cited'].fillna(0)
    merged_df['Times Cited'] = merged_df['Times Cited'].astype(int)
    merged_df['Recent Citations'] = merged_df['Recent Citations'].fillna(0)
    merged_df['Recent Citations'] = merged_df['Recent Citations'].astype(int)
    merged_df['Field Citation Ratio'] = merged_df['Field Citation Ratio'].fillna(0)
    merged_df['Field Citation Ratio'] = merged_df['Field Citation Ratio'].astype(int)
    merged_df['Relative Citation Ratio'] = merged_df['Relative Citation Ratio'].fillna(0)
    merged_df['Relative Citation Ratio'] = merged_df['Relative Citation Ratio'].astype(int)
    merged_df['Altmetric'] = merged_df['Altmetric'].fillna(0)
    merged_df['Altmetric'] = merged_df['Altmetric'].astype(int)
    merged_df.to_excel(os.path.join(dim_out, 'merged_dimensions.xlsx'), index=False)


def load_dict(path, filename, fields):
    """
    Load a DataFrame with specific fields from a CSV file.

    Parameters:
    - path (str): The directory path where the CSV file is located.
    - filename (str): The name of the CSV file to be loaded.
    - fields (List[str]): A list of column names to be loaded from the CSV file.

    Returns:
    pd.DataFrame: A DataFrame containing the specified fields from the CSV file.

    Example:
    >>> fields_to_load = ['column1', 'column2', 'column3']
    >>> loaded_data = load_dict('/path/to/data', 'example_data.csv', fields_to_load)
    """
    return pd.read_csv(os.path.join(path, filename),
                       index_col = 0,
                       usecols = fields)


def make_long(input_df: pd.DataFrame,
              df_col_name: str,
              delim: str = '\n') -> pd.DataFrame:
    """
    Transform a DataFrame with multiline values into a long-format DataFrame.

    Parameters:
    - input_df (pd.DataFrame): The input df containing the data to be transformed.
    - df_col_name (str): Name of column in input df containing multiline values.
    - delim (str, optional): The delimiter used to split multiline values into rows.

    Returns:
    pd.DataFrame: A long-format df with columns 'Key' and the specified 'df_col_name'.
    """
    df = pd.DataFrame(columns=['Key', df_col_name])
    counter = 0
    for index, row in input_df.iterrows():
        if row[df_col_name] is not np.nan:
            split_rows = re.split(r'\n', row[df_col_name])
            for single_val in split_rows:
                df.at[counter, 'Key'] = index
                df.at[counter, df_col_name] = single_val.strip()
                counter += 1
    return df


def chunker(seq, size):
    """ Helper function to chunk a list into parts"""
    return (seq[pos:pos + size] for pos in range(0,
                                                 len(seq),
                                                 size))


def get_data_from_lists(query_list, client, query_type):
    """
    A helper function to get rows of data
    from an input list of various paper IDs.

    :param query_list: list of items to query
    :param client: google query client
    :param query_type: object type to query
    :return: a GBC iterator containing all data
    """
    try:
        if query_type == 'doi':
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ArrayQueryParameter("doi", "STRING", query_list),
                ]
            )
            QUERY = """
                    SELECT id,
                    abstract,
                    altmetrics,
                    authors,
                    book_title,
                    category_for,
                    category_uoa,
                    citations,
                    citations_count,
                    concepts,
                    date_normal,
                    doi,
                    eisbn,
                    funder_orgs,
                    isbn,
                    journal,
                    journal.eissn,
                    journal.issn,
                    metrics,
                    open_access_categories_v2,
                    reference_ids,
                    research_org_cities,
                    research_org_countries,
                    research_orgs,
                    researcher_ids,
                    title.preferred,
                    type,
                    FROM `dimensions-ai.data_analytics.publications` p
                    WHERE p.doi IN UNNEST(@doi)""" % (query_list)
            query_job = client.query(QUERY, job_config=job_config)

        elif query_type == 'isbn':
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ArrayQueryParameter("isbn", "STRING", query_list),
                ]
            )
            QUERY = """
                    SELECT id,
                    abstract,
                    altmetrics,
                    authors,
                    book_title,
                    category_for,
                    category_uoa,
                    citations,
                    citations_count,
                    concepts,
                    date_normal,
                    doi,
                    eisbn,
                    funder_orgs,
                    isbn,
                    journal,
                    journal.eissn,
                    journal.issn,
                    metrics,
                    open_access_categories_v2,
                    reference_ids,
                    research_org_cities,
                    research_org_countries,
                    research_orgs,
                    researcher_ids,
                    title.preferred,
                    type,
                    FROM `dimensions-ai.data_analytics.publications` p
                    WHERE p.isbn IN UNNEST(@isbn)""" % (query_list)
            query_job = client.query(QUERY, job_config=job_config)

        elif query_type == 'title':
            QUERY = """
                    SELECT id,
                    abstract,
                    altmetrics,
                    authors,
                    book_title,
                    category_for,
                    category_uoa,
                    citations,
                    citations_count,
                    concepts,
                    date_normal,
                    doi,
                    eisbn,
                    funder_orgs,
                    isbn,
                    journal,
                    journal.eissn,
                    journal.issn,
                    metrics,
                    open_access_categories_v2,
                    reference_ids,
                    research_org_cities,
                    research_org_countries,
                    research_orgs,
                    researcher_ids,
                    title.preferred,
                    type,
                    FROM `dimensions-ai.data_analytics.publications`
                    WHERE title.preferred IN UNNEST(@title)
                    """
            query_params = [
                bigquery.ArrayQueryParameter("title", "STRING", query_list)
            ]
            job_config = bigquery.QueryJobConfig(
                query_parameters=query_params
            )
            query_job = client.query(QUERY, job_config=job_config)
        rows = query_job.result()
        return rows

    except Exception as e:
        print(traceback.format_exc())


def get_all_data(client, query_list, query_type):
    """ Helper function to get all data from iterative queries"""
    results = get_data_from_lists(query_list,
                                  client,
                                  query_type).to_dataframe()
    return results


def get_dimensions_data(paper_ident_path: str,
                        dim_out: str,
                        my_project_id: str) -> None:
    """
    Retrieve Dimensions Data based on paper identifiers and save the results.

    Parameters:
    - paper_ident_path (str): The path to the directory containing paper identifiers.
    - dim_out (str): The path to the directory where Dimensions data will be stored.
    - my_project_id (str): The Google Cloud project ID for the BigQuery client.

    Returns:
    None

    The function loads paper identifiers, extracts DOIs, ISBNs, and Titles,
    queries Dimensions data using the extracted identifiers, and saves the results
    to Excel files.

    Example:
    >>> get_dimensions_data('/path/to/paper_identifiers',
                            '/path/to/dimensions_data',
                            'my_project_id')
    Getting Dimensions Data!
    ...
    Data saved to '/path/to/dimensions_data/doi_returns_dimensions.xlsx'.
    Data saved to '/path/to/dimensions_data/isbns_returns_dimensions.xlsx'.
    Data saved to '/path/to/dimensions_data/title_returns_dimensions.xlsx'.
    """
    print('Getting Dimensions Data!')
    fields = ['REF impact case study identifier',
              'DOIs_suggested', 'ISBNs_suggested', 'Titles_suggested']
    df = load_dict(os.path.join(paper_ident_path, 'paper_identifiers'),
                   'underpinning_research.csv', fields)
    doi_df = make_long(df, 'DOIs_suggested')
    titles_df = make_long(df, 'Titles_suggested')
    isbns_df = make_long(df, 'ISBNs_suggested')
    client = bigquery.Client(project=my_project_id)

    dois_to_query = doi_df["DOIs_suggested"].tolist()
    doi_return = get_all_data(client, dois_to_query, 'doi')
    # if multiple returns per DOI, drop
    doi_return = doi_return.drop_duplicates(subset=['doi'], keep=False)
    doi_final = pd.merge(doi_df, doi_return, how='outer', left_on='DOIs_suggested', right_on='doi')
    doi_final = doi_final.rename({'DOIs_suggested': 'doi_raw'}, axis=1)
    dim_doi_out_path = os.path.join(dim_out, 'doi_returns_dimensions.xlsx')
    doi_final.to_excel(dim_doi_out_path, index=False)

    dim_isbns_out_path = os.path.join(dim_out, 'isbns_returns_dimensions.xlsx')
    isbns_to_query = isbns_df["ISBNs_suggested"].tolist()
    isbns_return = get_all_data(client, isbns_to_query, 'isbn')
    # if multiple returns per ISBN, drop
    isbns_return = isbns_return.drop_duplicates(subset=['isbn'], keep=False)
    isbns_final = pd.merge(isbns_df, isbns_return, how='outer', left_on='ISBNs_suggested', right_on='isbn')
    isbns_final = isbns_final.rename({'ISBNs_suggested': 'isbn_raw'}, axis=1)
    isbns_final.to_excel(dim_isbns_out_path, index=False)

    dim_title_out_path = os.path.join(dim_out, 'title_returns_dimensions.xlsx')
    titles_to_query = titles_df["Titles_suggested"].tolist()
    titles_return = get_all_data(client, titles_to_query, 'title')
    # if multiple returns per Title, drop
    titles_return = titles_return.drop_duplicates(subset=['preferred'], keep=False)
    titles_final = pd.merge(titles_df, titles_return, how='outer', left_on='Titles_suggested', right_on='preferred')
    titles_final = titles_final.rename({'Titles_suggested': 'titles_raw'}, axis=1)
    titles_final.to_excel(dim_title_out_path, index=False)
