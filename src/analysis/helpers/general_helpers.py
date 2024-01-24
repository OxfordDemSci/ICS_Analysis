import os
import ast
import json
import numpy as np
import pandas as pd

def build_paper_panels(paper_level: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, pd.Series, pd.Series]:
    """
    Build summary statistics for paper-level metrics grouped by Unit of Assessment (UoA) and Main Panel.

    Parameters:
    - paper_level (pd.DataFrame): The input DataFrame containing paper-level metrics.

    Returns:
    tuple[pd.DataFrame, pd.Series, pd.Series, pd.Series]: A tuple containing:
    - A DataFrame (`paper_panels`) with average metrics grouped by Main Panel.
    - A Series (`cited_by_uoa`) with average Times Cited grouped by UoA.
    - A Series (`altm_by_uoa`) with average Altmetric scores grouped by UoA.
    - A Series (`ratio_by_uoa`) with average Relative Ratio values grouped by UoA.
    """
    # Group by UoA and Main Panel to calculate mean metrics
    altm_by_uoa = paper_level.groupby(['Unit of assessment number'])['Average Altmetric'].mean()
    altm_by_panel = paper_level.groupby(['Main panel'])['Average Altmetric'].mean()
    altm_by_uoa.index = altm_by_uoa.index.astype(int)

    cited_by_uoa = paper_level.groupby(['Unit of assessment number'])['Average Times Cited'].mean()
    cited_by_panel = paper_level.groupby(['Main panel'])['Average Times Cited'].mean()
    cited_by_uoa.index = cited_by_uoa.index.astype(int)

    ratio_by_uoa = paper_level.groupby(['Unit of assessment number'])['Relative Ratio'].mean()
    ratio_by_panel = paper_level.groupby(['Main panel'])['Relative Ratio'].mean()
    ratio_by_uoa.index = ratio_by_uoa.index.astype(int)
    paper_panels = pd.merge(cited_by_panel,
                            altm_by_panel,
                            left_index=True,
                            right_index=True)
    paper_panels = paper_panels.reset_index()
    ratio_panels = ratio_by_panel.reset_index()
    paper_panels = pd.merge(paper_panels,
                            ratio_panels,
                            left_on = 'Main panel',
                            right_on = 'Main panel').set_index('Main panel')
    print(paper_panels)
    return paper_panels, cited_by_uoa, altm_by_uoa, ratio_by_uoa


def make_inf_var(paper_level, score_inf_path):
    """
    Calculate and save average metrics grouped by 'Key' in paper-level data.

    Parameters:
    - paper_level (pd.DataFrame): The input DataFrame containing paper-level metrics.
    - score_inf_path (str): The directory path where the calculated metrics will be saved.

    Returns:
    None

    This function calculates the mean values of 'Average Altmetric', 'Average Times Cited', and 'Relative Ratio'
    grouped by 'Key' in the input paper-level DataFrame. The results are saved as CSV files in the specified directory.
    """
    altm = pd.DataFrame(paper_level.groupby(['Key'])['Average Altmetric'].mean())
    cited = pd.DataFrame(paper_level.groupby(['Key'])['Average Times Cited'].mean())
    rel_cite = pd.DataFrame(paper_level.groupby(['Key'])['Relative Ratio'].mean())
    altm.to_csv(os.path.join(score_inf_path, 'altm_by_ics.csv'))
    cited.to_csv(os.path.join(score_inf_path, 'cited_by_ics.csv'))
    rel_cite.to_csv(os.path.join(score_inf_path, 'citation_ratio_by_ics.csv'))


def make_heat_topics():
    raw = pd.read_csv(os.path.join(os.getcwd(), '..', '..',
                                   'data', 'topic_outputs', 'production_model',
                                   'ics_data_modelling_all_full_text.csv')
                      )
    df = pd.read_excel(os.path.join(os.getcwd(), '..', '..',
                                   'data', 'raw', 'raw_ics_data.xlsx'))
    df = df[['REF impact case study identifier', 'Unit of assessment number']]
    df = pd.merge(df, raw, how ='left',
                 left_on= 'REF impact case study identifier',
                 right_on = 'case_id')
    df = df[df['topic_top1'].notnull()]
    df['Unit of assessment number'] = df['Unit of assessment number'].astype(int)
    heat = pd.DataFrame(0,
                        index = df['Unit of assessment number'].unique(),
                        columns=range(0, 72))
    for index in heat.index:
        uoa = df[df['Unit of assessment number']==index]
        for columns in range(1, 72):
            for index_uoa in uoa.index:
                if not np.isnan(uoa.at[index_uoa, 'topic_top'+str(int(columns))]):
                    topic = int(uoa.at[index_uoa, 'topic_top'+str(int(columns))])
                    if topic < 71:
                        prob = uoa.at[index_uoa, 'prob_top'+str(int(columns))]
                        if not np.isnan(uoa.at[index_uoa, 'topic_top'+str(int(columns))]):
                            heat.loc[index, topic] = heat.at[index, topic] + prob
    count = df.groupby(['Unit of assessment number'])['Unit of assessment number'].count()
    heat = heat.drop(71, axis=1)
    return heat, count

def make_keywords(four_star):
    merged_path = os.path.join(os.getcwd(), '..', '..', 'data', 'merged')
    asset_path = os.path.join(os.getcwd(), '..', '..', 'assets')
    df = pd.read_csv(os.path.join(merged_path, 'merged_ref_data_exc_output.csv'), index_col=0)
    with open(os.path.join(asset_path, 'keyword_dictionary.json')) as json_file:
        keyword_dict = json.load(json_file)
    if four_star is True:
        df = df[(df['3*_Impact'] == '0.0') &
                (df['2*_Impact']=='0.0') &
                (df['1*_Impact'] == '0.0') &
                (df['Unclassified_Impact']=='0.0')]
        file_suffix ='four_star'
    elif four_star is False:
        file_suffix='all_star'
    df = df[(df['Main panel'] == 'D') |
            (df['Main panel'] == 'C') |
            (df['Unit of assessment number'] == '4.0')]
    freetext = ['1. Summary of the impact',
                '2. Underpinning research',
                '3. References to the research',
                '4. Details of the impact',
                '5. Sources to corroborate the impact']
    df = df[freetext]
    df = df.apply(lambda x: x.astype(str).str.lower())
    for key, value in keyword_dict.items():
        temp_df = df[df.apply(lambda r: any([kw in r[0] for kw in value]),
                              axis=1)]
        newkey = key.replace("\n", "")
        print(f'Number ICS found for {newkey}: ', len(temp_df))



def how_much_dim_matched(df, object_type):
    """
    Calculate and print the proportion of direct matches for a specific object type.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing data for matching.
    - object_type (str): The type of object for which matching is performed.

    Returns:
    None

    This function calculates the proportion of direct matches for a specified object type
    by dividing the count of non-null 'id' values by the total number of rows in the DataFrame.
    The result is printed as a rounded percentage along with the count of non-null 'id' values.
    """
    print(f'We can directly {object_type} match: ',
          round(len(df[df['id'].notnull()]) / len(df), 3))
    print(object_type + ' returns: ',
          len(df[df['id'].notnull()]))


def return_paper_level(dim_out):
    """
    Return a DataFrame representing paper-level data by merging Dimensions and raw data.

    Parameters:
    - dim_out (str): The directory path containing Dimensions returns CSV files.

    Returns:
    pd.DataFrame: A merged DataFrame containing paper-level data with additional metrics.

    This function reads Dimensions returns for DOIs and ISBNs, checks the direct match proportions,
    and merges them with raw data using the 'Key' and 'REF impact case study identifier' columns.
    Additional metrics like 'Average Times Cited', 'Relative Ratio', and 'Average Altmetric' are extracted
    from the 'metrics' and 'altmetrics' columns and added to the resulting DataFrame.
    """
    doi_df = pd.read_csv(os.path.join(dim_out,
                                      'doi_returns_dimensions.csv'))
    isbn_df = pd.read_csv(os.path.join(dim_out,
                                       'isbns_returns_dimensions.csv'))
    raw_df = pd.read_excel(os.path.join(os.getcwd(),
                                        '..',
                                        '..',
                                        'data',
                                        'raw',
                                        'raw_ics_data.xlsx'))
    how_much_dim_matched(doi_df, 'DOI')
    how_much_dim_matched(isbn_df, 'ISBN')
    merged_df = pd.concat([doi_df, isbn_df])
    merged_df = merged_df.drop_duplicates(subset=['Key', 'id'])
    merged_df = merged_df[merged_df['id'].notna()]
    merged_df = merged_df.sort_values(by='Key')
    paper_level = pd.merge(merged_df, raw_df,
                       how = 'inner',
                       left_on = 'Key',
                       right_on = 'REF impact case study identifier'
                       )
    for index in paper_level.index:
        met = paper_level['metrics'][index]
        paper_level.loc[index,
                        'Average Times Cited'] = ast.literal_eval(met)['times_cited']
        paper_level.loc[index,
                        'Relative Ratio'] = ast.literal_eval(met)['relative_citation_ratio']
        alt = paper_level['altmetrics'][index]
        paper_level.loc[index,
                        'Average Altmetric'] = ast.literal_eval(alt)['score']
    paper_level['Average Times Cited'] = paper_level['Average Times Cited'].astype(int)
    paper_level['Average Altmetric'] = paper_level['Average Altmetric'].fillna(0)
    paper_level['Average Altmetric'] = paper_level['Average Altmetric'].astype(int)
    paper_level['Relative Ratio'] = paper_level['Relative Ratio'].fillna(0)
    paper_level['Relative Ratio'] = paper_level['Relative Ratio'].astype(int)
    return paper_level
