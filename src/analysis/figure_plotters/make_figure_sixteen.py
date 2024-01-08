import re
import os
import warnings
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import gender_guesser.detector as gender
from helpers.figure_helpers import savefigures
d = gender.Detector()
warnings.filterwarnings('ignore')
mpl.rcParams['font.family'] = 'Graphik-Light'
plt.rcParams["axes.labelweight"] = "light"
plt.rcParams["font.weight"] = "light"


def make_figure_sixteen():
    print('\n******************************************************')
    print('***************** Making Figure 16! ********************')
    print('********************************************************')
    import gender_guesser.detector as gender
    d = gender.Detector()
    funder_level = pd.DataFrame(columns=['Panel',
                                         'UoA',
                                         'ICS_uid',
                                         'pub_uid',
                                         'funder'])
    dim_out = os.path.join(os.getcwd(), '..', '..',
                           'data', 'dimensions_returns')
    paper_level = pd.read_excel(os.path.join(dim_out, 'merged_dimensions.xlsx'))

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
    grid_lookup = pd.read_csv(os.path.join(os.getcwd(),
                                           '..',
                                           '..',
                                           'data',
                                           'manual',
                                           'grid',
                                           'grid_lookup.csv')
                              )
    paper_level = pd.merge(paper_level,
                           df[['Main panel',
                               'Unit of assessment number',
                               'REF impact case study identifier']],
                           how='left',
                           left_on='Key',
                           right_on='REF impact case study identifier')
    counter = 0
    for index, row in paper_level.iterrows():
        funder_raw = row['funder_orgs']
        funder_list = re.findall("'(.*?)'", funder_raw)  # .split(' ')
        for funder in funder_list:
            funder_level.at[counter, 'Panel'] = row['Main panel']
            funder_level.at[counter, 'UoA'] = int(row['Unit of assessment number'])
            funder_level.at[counter, 'ICS_uid'] = row['Key']
            funder_level.at[counter, 'pub_uid'] = row['id']
            funder_level.at[counter, 'funder'] = funder
            counter += 1
    funder_level = pd.merge(funder_level,
                            grid_lookup,
                            how='left',
                            left_on='funder',
                            right_on='grid')
    d = gender.Detector()
    funder_level_C = funder_level[funder_level['Panel'] == 'C']
    funder_counts_C = funder_level_C['name'].value_counts()
    funder_counts_C = funder_counts_C[funder_counts_C.index.str.len() > 0]
    funder_level_D = funder_level[funder_level['Panel'] == 'D']
    funder_counts_D = funder_level_D['name'].value_counts()
    funder_counts_D = funder_counts_D[funder_counts_D.index.str.len() > 0]
    funder_level_4 = funder_level[funder_level['UoA'] == 4]
    funder_counts_4 = funder_level_4['name'].value_counts()
    funder_counts_4 = funder_counts_4[funder_counts_4.index.str.len() > 0]
    counter = 0
    ICS_funder_level = pd.DataFrame(columns=['REF impact case study identifier',
                                             'funder'])
    pattern = r'\[[^\]]*\]'
    for index, row in df.iterrows():
        if row['funders_extracted'] is not np.nan:
            funders = re.sub(pattern, '', row['funders_extracted'])
            funder_row = funders.split(';')
            for funder in funder_row:
                funder = re.sub(r'\[.*?\]', '',
                                funder).strip()
                ICS_funder_level.at[counter,
                'REF impact case study identifier'] = row[
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
    ICS_funder_level_C = ICS_funder_level[ICS_funder_level['Main panel'] == 'C']
    ICS_funder_level_D = ICS_funder_level[ICS_funder_level['Main panel'] == 'D']
    ICS_funder_level_4 = ICS_funder_level[ICS_funder_level['Unit of assessment number'] == 4.0]

    ICS_funder_level_C = ICS_funder_level_C['funder'].value_counts()
    ICS_funder_level_C = ICS_funder_level_C[ICS_funder_level_C.index.str.len() > 1]
    ICS_funder_level_D = ICS_funder_level_D['funder'].value_counts()
    ICS_funder_level_D = ICS_funder_level_D[ICS_funder_level_D.index.str.len() > 1]
    ICS_funder_level_4 = ICS_funder_level_4['funder'].value_counts()
    ICS_funder_level_4 = ICS_funder_level_4[ICS_funder_level_4.index.str.len() > 1]

    ba_rgb2 = ['#41558c', '#E89818', '#CF202A']
    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(16, 12))
    bar1 = ax1.barh(funder_counts_4[0:5].sort_values().index,
                    funder_counts_4[0:5].sort_values(), edgecolor='k', color=ba_rgb2[0],
                    height=0.5, alpha=1)
    bar2 = ax2.barh(funder_counts_C[0:5].sort_values().index,
                    funder_counts_C[0:5].sort_values(), edgecolor='k', color=ba_rgb2[1],
                    height=0.5, alpha=1)
    bar3 = ax3.barh(funder_counts_D[0:5].sort_values().index,
                    funder_counts_D[0:5].sort_values(), edgecolor='k', color=ba_rgb2[2],
                    height=0.5, alpha=1)

    bar4 = ax4.barh(ICS_funder_level_4[0:5].sort_values().index,
                    ICS_funder_level_4[0:5].sort_values(), edgecolor='k', color=ba_rgb2[0],
                    height=0.5, alpha=1)
    bar5 = ax5.barh(ICS_funder_level_C[0:5].sort_values().index,
                    ICS_funder_level_C[0:5].sort_values(), edgecolor='k', color=ba_rgb2[1],
                    height=0.5, alpha=1)
    bar6 = ax6.barh(ICS_funder_level_D[0:5].sort_values().index,
                    ICS_funder_level_D[0:5].sort_values(), edgecolor='k', color=ba_rgb2[2],
                    height=0.5, alpha=1)

    ax1.bar_label(bar1, fontsize=16, padding=5)
    ax2.bar_label(bar2, fontsize=16, padding=5)
    ax3.bar_label(bar3, fontsize=16, padding=5)
    ax4.bar_label(bar4, fontsize=16, padding=5)
    ax5.bar_label(bar5, fontsize=16, padding=5)
    ax6.bar_label(bar6, fontsize=16, padding=5)
    for ax in [ax1, ax2, ax3, ax4, ax5, ax6]:
        ax.tick_params(axis='both', which='minor', labelsize=14)
        ax.tick_params(axis='both', which='major', labelsize=14)
    ax1.set_title('a.', loc='left', fontsize=21, fontweight='bold', y=0.98)
    ax2.set_title('b.', loc='left', fontsize=21, fontweight='bold', y=0.98)
    ax3.set_title('c.', loc='left', fontsize=21, fontweight='bold', y=0.98)
    ax4.set_title('d.', loc='left', fontsize=21, fontweight='bold', y=0.98)
    ax5.set_title('e.', loc='left', fontsize=21, fontweight='bold', y=0.98)
    ax6.set_title('f.', loc='left', fontsize=21, fontweight='bold', y=0.98)
    ax4.set_xlabel('Instances of Funding\n       (UoA 4)      ', fontsize=18)
    ax5.set_xlabel('Instances of Funding\n      (Panel C)     ', fontsize=18)
    ax6.set_xlabel('Instances of Funding \n      (Panel D)     ', fontsize=18)
    ax1.set_ylabel('Paper Funders', fontsize=20)
    ax4.set_ylabel('ICS Funders', fontsize=20)
    sns.despine(offset=10, trim=True)
    plt.tight_layout()
    fig_path = os.path.join(os.getcwd(), '..', '..', 'figures')
    filename = 'figure_16'
    savefigures(plt, fig_path, filename)

    print('ALl Data: ', ICS_funder_level['funder'].value_counts()[0:10])
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
    all_funder_path = os.path.join('..', '..', 'tables', 'UKRI_funders.csv')
    print('Saving all funder data to: ', all_funder_path)
    comb.to_csv(all_funder_path)

    selected_funders = ['ESRC', 'EPSRC', 'AHRC', 'MRC', 'Innovate UK', 'NERC', 'BBSRC']
    UKRI = comb.loc[selected_funders, :]
    UKRI_funder_path = os.path.join('..','..','tables', 'UKRI_funders_only.csv')
    print('Percent of acknowledgements to UKRI organisations: \n', UKRI.sum())
    print('Percent of each UKRI org for each field: \n', UKRI / UKRI.sum() * 100)
    print('Saving URKI funder table to: ', UKRI_funder_path)
    UKRI.to_csv(UKRI_funder_path)
