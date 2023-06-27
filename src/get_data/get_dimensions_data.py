import os
import pandas as pd
import traceback
import pandas as pd
from google.cloud import bigquery


def load_dict(path, filename):
    df = pd.read_csv(os.path.join(path, filename))
    return df.dropna()


def make_long(input_df, df_col_name, delim=','):
    df = pd.DataFrame(columns=['Key', df_col_name])
    counter = 0
    for index, row in input_df.iterrows():
        split_rows = row['Value'].split(delim)
        for single_val in split_rows:
            df.at[counter, 'Key'] = row['Key']
            df.at[counter, df_col_name] = single_val
            counter += 1
    return df


def clean_doi_df(doi_df):
    doi_df['DOIs'] = doi_df['DOIs'].str.replace('https://doi.org/', '', regex=False)
    doi_df['DOIs'] = doi_df['DOIs'].str.replace('http://dx.doi.org/', '', regex=False)
    doi_df['DOIs'] = doi_df['DOIs'].str.replace('https://onlinelibrary.wiley.com/doi/full/', '', regex=False)
    return doi_df


def clean_title_df(titles_df):
    titles_df['DOIs'] = titles_df['DOIs'].str.replace('https://doi.org/', '', regex=False)
    return titles_df


def clean_isbns_df(isbns_df):
    isbns_df['DOIs'] = isbns_df['DOIs'].str.replace('https://doi.org/', '', regex=False)
    return titles_df


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
                    SELECT id, title.preferred, doi, abstract, book_title,
                    authors, journal.issn, journal.eissn, concepts,
                    type, date_normal, category_for, category_uoa,
                    citations_count, research_org_cities,
                    research_org_country_names, funder_orgs,
                    eisbn, isbn, journal, research_org_cities,
                    research_orgs, researcher_ids,
                    altmetrics, reference_ids,
                    citations, metrics,
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
                    SELECT id, title.preferred, doi, abstract, book_title,
                    authors, journal.issn, journal.eissn, concepts,
                    type, date_normal, category_for, category_uoa,
                    citations_count, research_org_cities,
                    research_org_country_names, funder_orgs,
                    eisbn, isbn, journal, research_org_cities,
                    research_orgs, researcher_ids,
                    altmetrics, reference_ids,
                    citations, metrics,
                    FROM `dimensions-ai.data_analytics.publications` p
                    WHERE p.isbn IN UNNEST(@isbn)""" % (query_list)
            query_job = client.query(QUERY, job_config=job_config)

        elif query_type == 'title':
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.StructQueryParameter(
                        'title',
                        bigquery.ArrayQueryParameter(
                            'preferred',
                            'STRING',
                            query_list))
                ])
            QUERY = """
                    SELECT id, title.preferred,
                    doi, abstract, book_title,
                    authors, journal.issn, journal.eissn, concepts,
                    type, date_normal, category_for, category_uoa,
                    citations_count, research_org_cities,
                    research_org_country_names, funder_orgs,
                    eisbn, isbn, journal, research_org_cities,
                    research_orgs, researcher_ids,
                    altmetrics, reference_ids,
                    citations, metrics,
                    FROM `dimensions-ai.data_analytics.publications`
                    WHERE title IN UNNEST(@title)""" % (query_list)
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


#        save_file(results, file_path)
    return results

def main():
    paper_ident_path = os.path.join(os.getcwd(), '..', '..',
                                    'data', 'paper_identifiers')
    dois = load_dict(paper_ident_path, 'dictionary_dois.csv')
    isbns = load_dict(paper_ident_path, 'dictionary_isbns.csv')
    titles = load_dict(paper_ident_path, 'dictionary_titles.csv')
    print(len(dois), len(titles), len(isbns))
    doi_df = make_long(dois, 'DOIs')
    titles_df = make_long(titles, 'Titles', ' ,')
    isbns_df = make_long(isbns, 'ISBNs')
    print(len(doi_df), len(titles_df), len(isbns_df))
    MY_PROJECT_ID = "dimensionspkp"
    client = bigquery.Client(project=MY_PROJECT_ID)
    dim_out = os.path.join(os.getcwd(), '..', '..',
                           'data', 'dimensions_returns')

    dim_doi_out_path = os.path.join(dim_out, 'doi_returns_dimensions.csv')
    doi_df = clean_doi_df(doi_df)
    dois_to_query = doi_df["DOIs"].tolist()
    doi_return = get_all_data(client, dois_to_query, 'doi')
    doi_final = pd.merge(doi_df, doi_return, how='outer', left_on='DOIs', right_on='doi')
    doi_final = doi_final.drop('DOIs', axis=1)
    doi_final.to_csv(dim_doi_out_path, index=0)
    # dim_title_out_path = os.path.join(dim_out, 'title_returns_dimensions.csv')
    # titles_df = clean_title_df(titles_df)
    # titles_to_query = titles_df["Titles"].tolist()
    ##titles_return = get_all_data(client, titles_to_query, 'title')
    # titles_final = pd.merge(titles_df, titles_return, how='outer', left_on='DOIs', right_on='doi')
    # titles_final = titles_final.drop('DOIs', axis=1)
    # titles_final.to_csv(dim_titles_out_path, index=0)
    dim_isbns_out_path = os.path.join(dim_out, 'isbns_returns_dimensions.csv')
    isbns_df = clean_isbns_df(isbns_df)
    isbns_to_query = isbns_df["ISBNs"].tolist()
    isbns_return = get_all_data(client, isbns_to_query, 'isbn')
    isbns_final = pd.merge(isbns_df, isbns_return, how='outer', left_on='ISBNs', right_on='isbn')
    isbns_final = isbns_final.drop('ISBNs', axis=1)
    isbns_final.to_csv(dim_isbns_out_path, index=0)


if __name__ == "__main__":
    main()