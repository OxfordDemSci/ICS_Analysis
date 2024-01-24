import os
import re
import numpy as np
import pandas as pd


def make_table_one(table_path):
    print('Making Table 1!')
    df_ref = pd.read_csv(os.path.join(os.getcwd(),
                                      '..',
                                      '..',
                                      'data',
                                      'final',
                                      'enhanced_ref_data.csv'),
                         usecols=['Unit of assessment name',
                                  'fte',
                                  'num_doc_degrees_total',
                                  'tot_income',
                                  'inst_id',
                                  'Main panel',
                                  'Unit of assessment number'
                                  ])
    df = pd.DataFrame(columns=['Panel',
                               'Unit of Assessment',
                               'ICS (%)',
                               'FTE',
                               'PhD Degrees',
                               'Income (£bn)'],
                      index=range(1, 35))
    for uoa in df.index:
        df_uoa = df_ref[df_ref['Unit of assessment number'] == uoa]
        df.at[uoa, 'Panel'] = df_uoa['Main panel'].mode()[0]
        df.at[uoa, 'Unit of Assessment'] = df_uoa['Unit of assessment name'].mode()[0]
        df.at[uoa, 'ICS (%)'] = np.round(len(df_uoa) / len(df_ref) * 100, 2)
        df.at[uoa, 'FTE'] = df_uoa.drop_duplicates(subset='inst_id')['fte'].sum()
        df.at[uoa, 'PhD Degrees'] = df_uoa.drop_duplicates(subset='inst_id')['num_doc_degrees_total'].sum()
        df.at[uoa, 'Income (£bn)'] = df_uoa.drop_duplicates(subset='inst_id')['tot_income'].sum()
        df.at[uoa, 'Income (£bn)'] = df.at[uoa, 'Income (£bn)'] / 1000000000
    df.index.name = 'UoA #'
    df.to_csv(os.path.join(table_path, 'table_1.csv'))


def make_table_two(table_path):
    print('Making Table 2!')
    df_ref = pd.read_csv(os.path.join(os.getcwd(),
                                      '..',
                                      '..',
                                      'data',
                                      'final',
                                      'enhanced_ref_data.csv'),
                         usecols=['cluster_id',
                                  'cluster_name',
                                  'topic_name_short',
                                  'Unit of assessment number',
                                  'topic_name_short'
                                  ]
                         )
    df = pd.DataFrame(columns=['Grand Impact Theme',
                               'ICS (#N)',
                               'Modal Topic',
                               'Modal UoA',
                               ],
                      index=range(1, 11))
    for cluster_id in df.index:
        df_cluster_id = df_ref[df_ref['cluster_id'] == cluster_id]
        df.at[cluster_id, 'ICS (#N)'] = len(df_cluster_id)
        df.at[cluster_id, 'Grand Impact Theme'] = df_cluster_id['cluster_name'].mode()[0]
        df.at[cluster_id, 'Modal Topic'] = df_cluster_id['topic_name_short'].mode()[0]
        df.at[cluster_id, 'Modal UoA'] = int(df_cluster_id['Unit of assessment number'].mode()[0])
    df.index.name = 'Theme ID'
    df.to_csv(os.path.join(table_path, 'table_2.csv'))


def make_table_four(table_path):
    print('Making Table 4!')
    df_ref = pd.read_csv(os.path.join(os.getcwd(),
                                      '..',
                                      '..',
                                      'data',
                                      'final',
                                      'enhanced_ref_data.csv'),
                         usecols=['fte',
                                  'num_doc_degrees_total',
                                  'tot_income',
                                  'Unit of assessment number',
                                  'inst_id',
                                  'Main panel',
                                  ])
    df = pd.DataFrame(columns=['Number ICS',
                               '% Total ICS',
                               'FTE',
                               'PhD Degrees',
                               'Income (£bn)'],
                      index=['A', 'B', 'C', 'D'])
    for panel in df.index:
        df_panel = df_ref[df_ref['Main panel'] == panel]
        df.at[panel, 'Number ICS'] = len(df_panel)
        df.at[panel, '% Total ICS'] = np.round(len(df_panel) /
                                               len(df_ref) * 100, 2)
        df_panel_dedup = df_panel.drop_duplicates(subset=['inst_id', 'Unit of assessment number'])
        df.at[panel, 'FTE'] = df_panel_dedup['fte'].sum()
        df.at[panel, 'PhD Degrees'] = df_panel_dedup['num_doc_degrees_total'].sum()
        df.at[panel, 'Income (£bn)'] = df_panel_dedup['tot_income'].sum()
        df.at[panel, 'Income (£bn)'] = df.at[panel, 'Income (£bn)'] / 1000000000
    df.index.name = 'Panel'
    df.to_csv(os.path.join(table_path, 'table_4.csv'))


def make_table_five(table_path):
    print('Making Table 5!')
    df = pd.read_csv(os.path.join(os.getcwd(),
                                  '..',
                                  '..',
                                  'data',
                                  'final',
                                  'enhanced_ref_data.csv'),
                     usecols=['Unit of assessment number',
                              'countries_extracted',
                              'Main panel'])
    country_list=[]
    for index, row in df.iterrows():
        countries = row['countries_extracted']
        if countries is not np.nan:
            countries = countries.split(';')
            for country in countries:
                if ((country != 'TWN')
                        and (country != 'ESH')
                        and (country != 'GRL')
                        and (country != 'FLK')):
                    country_list.append(country.strip())
    df1 = pd.DataFrame(country_list)[0].value_counts()
    df1 = df1.sort_values(ascending=False)
    iso_list = df1[0:10].index.to_list()
    df['countries_extracted'] = df['countries_extracted'].fillna('')
    df2 = pd.DataFrame(index=iso_list,
                       columns=['Panel A',
                                'UoA 4',
                                'Panel B',
                                'Panel C',
                                'Panel D'])
    for iso in iso_list:
        df2.at[iso, 'Panel A'] = (len(df[(df['Main panel'] == 'A') &
                                         (df['countries_extracted'].str.contains(iso))])/
                                  len(df[(df['Main panel'] == 'A')]))
        df2.at[iso, 'Panel B'] = (len(df[(df['Main panel'] == 'B') &
                                         (df['countries_extracted'].str.contains(iso))])/
                                  len(df[(df['Main panel'] == 'B')]))
        df2.at[iso, 'Panel C'] = (len(df[(df['Main panel'] == 'C') &
                                         (df['countries_extracted'].str.contains(iso))])/
                                  len(df[(df['Main panel'] == 'C')]))
        df2.at[iso, 'Panel D'] = (len(df[(df['Main panel'] == 'D') &
                                         (df['countries_extracted'].str.contains(iso))])/
                                  len(df[(df['Main panel'] == 'D')]))
        df2.at[iso, 'UoA 4'] = (len(df[(df['Unit of assessment number'] == 4.0) &
                                       (df['countries_extracted'].str.contains(iso))])/
                                len(df[(df['Unit of assessment number'] == 4.0)]))
    df2 = df2.astype(float).round(4)*100
    df2.to_csv(os.path.join(table_path, 'table_5.csv'))


def make_table_six(tables_path):
    print('Making Table 6!')
    df = pd.read_csv(os.path.join(os.getcwd(),
                                  '..',
                                  '..',
                                  'data',
                                  'final',
                                  'enhanced_ref_data.csv'),
                     usecols=['Main panel',
                              'Unit of assessment number',
                              'REF impact case study identifier',
                              'funders_extracted'])
    df['Unit of assessment number'] = df['Unit of assessment number'].astype(int)
    ICS_funder_level = pd.DataFrame(columns=['REF impact case study identifier',
                                             'funder'])
    counter = 0
    pattern = r'\[[^\]]*\]'
    for index, row in df.iterrows():
        if row['funders_extracted'] is not np.nan:
            funders = re.sub(pattern, '', row['funders_extracted'])
            funder_row = funders.split(';')
            for funder in funder_row:
                funder = re.sub(r'\[.*?\]', '',
                                funder).strip()
                ICS_funder_level.at[counter, 'REF impact case study identifier'] = row[
                    'REF impact case study identifier']
                ICS_funder_level.at[counter, 'funder'] = funder
                counter += 1
    ICS_funder_level = ICS_funder_level.drop_duplicates(subset=['funder',
                                                                'REF impact case study identifier'],
                                                        keep='first')
    ICS_funder_level['funder'] = ICS_funder_level['funder'].str.replace('European Commission', 'EC')
    ICS_funder_level['funder'] = ICS_funder_level['funder'].str.replace('British Academy', 'BA')
    ICS_funder_level['funder'] = ICS_funder_level['funder'].str.replace('Wellcome Trust', 'WT')
    ICS_funder_level['funder'] = ICS_funder_level['funder'].str.replace('Leverhulme Trust', 'LT')
    ICS_funder_level['funder'] = ICS_funder_level['funder'].str.replace('Arts Council England', 'ACE')
    ICS_funder_level['funder'] = ICS_funder_level['funder'].str.replace(
        'Biotechnology and Biological Sciences Research Council', 'BBSRC')
    ICS_funder_level['funder'] = ICS_funder_level['funder'].str.replace('Natural Environment Research Council', 'NERC')
    df = df[['Main panel', 'Unit of assessment number',
             'REF impact case study identifier']]
    ICS_funder_level = pd.merge(ICS_funder_level, df[['Main panel',
                                                      'Unit of assessment number',
                                                      'REF impact case study identifier']],
                                how='left', on='REF impact case study identifier')

    ICS_funder_level = ICS_funder_level[ICS_funder_level['funder'].notnull()]
    ALL = ICS_funder_level['funder'].value_counts() / len(ICS_funder_level) * 100

    UOA4 = ICS_funder_level[ICS_funder_level['Unit of assessment number'] == 4]['funder'].value_counts() / len(
        ICS_funder_level[ICS_funder_level['Unit of assessment number'] == 4.0]) * 100

    PANELA = ICS_funder_level[ICS_funder_level['Main panel'] == 'A']['funder'].value_counts() / len(
        ICS_funder_level[ICS_funder_level['Main panel'] == 'A']) * 100

    PANELB = ICS_funder_level[ICS_funder_level['Main panel'] == 'B']['funder'].value_counts() / len(
        ICS_funder_level[ICS_funder_level['Main panel'] == 'B']) * 100

    PANELC = ICS_funder_level[ICS_funder_level['Main panel'] == 'C']['funder'].value_counts() / len(
        ICS_funder_level[ICS_funder_level['Main panel'] == 'C']) * 100

    PANELD = ICS_funder_level[ICS_funder_level['Main panel'] == 'D']['funder'].value_counts() / len(
        ICS_funder_level[ICS_funder_level['Main panel'] == 'D']) * 100

    comb = pd.concat([ALL, PANELA, PANELB, UOA4, PANELC, PANELD], axis=1)
    comb.columns = ['All', 'Panel A', 'Panel B', 'UoA4', 'Panel C', 'Panel D']
    comb = comb.sort_values(by='All', ascending=False)
    comb = comb.round(2)
    all_funder_path = os.path.join(tables_path, 'table_6.csv')
    comb.to_csv(all_funder_path)
