import re
import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from helpers.figure_helpers import savefigures
from mne_connectivity.viz import plot_connectivity_circle

mpl.rcParams['font.family'] = 'Graphik'
plt.rcParams["axes.labelweight"] = "light"
plt.rcParams["font.weight"] = "light"

cmap = mpl.colors.LinearSegmentedColormap.from_list("",
                                                    ['white', '#41558c', '#E89818', '#CF202A']
                                                     )

def make_inter_ax(df_for, ax, letter):
    plot_connectivity_circle(df_for.replace(0, np.nan).to_numpy(),
                             list(df_for.index), padding=5,
                             facecolor='white', node_width=12,
                             textcolor='black', node_linewidth=1,
                             linewidth=5, colormap=cmap, vmin=None,
                             vmax=None, colorbar=True,
                             title=letter,
                             fontsize_title=20,
                             node_colors=['w'], colorbar_size=0.75,
                             colorbar_pos=(.4, 0.5),# ax=ax,
                             fontsize_names=14, fontsize_colorbar=13)
    ax.set_xticks([])
    ax.set_xticklabels([])
#    ax.set_title(letter, loc='left', x=-0.05, fontsize=18, y=1.025)
    ax.set_yticks([])
    ax.set_yticklabels([])
    #    ax.set_title(letter, loc='left', x=-0.0, fontsize=100, y=1.0)
    return ax


def make_tagged(tagged_res):
    tagged_res_l2 = pd.DataFrame(0,
                                 index=tagged_res['Tag group'].unique(),
                                 columns=tagged_res['Tag group'].unique())
    for ICS in tagged_res['REF case study identifier'].unique():
        temp = tagged_res[tagged_res['REF case study identifier'] == ICS]
        counter = 0
        for group1 in temp['Tag group']:
            for group2 in temp['Tag group']:
                if group1 != group2:
                    tagged_res_l2.at[group1, group2] += 1
    tagged_res_l2 = tagged_res_l2.rename({'Information And Computing Sciences': 'IT'}, axis=0)
    tagged_res_l2 = tagged_res_l2.rename({'Information And Computing Sciences': 'IT'}, axis=1)
    tagged_res_l2 = tagged_res_l2.rename({'Built Environment And Design': 'Urban'}, axis=0)
    tagged_res_l2 = tagged_res_l2.rename({'Built Environment And Design': 'Urban'}, axis=1)
    tagged_res_l2 = tagged_res_l2.rename({'Biological Sciences': 'Biology'}, axis=0)
    tagged_res_l2 = tagged_res_l2.rename({'Biological Sciences': 'Biology'}, axis=1)
    tagged_res_l2 = tagged_res_l2.rename({'Medical And Health Sciences': 'Health'}, axis=0)
    tagged_res_l2 = tagged_res_l2.rename({'Medical And Health Sciences': 'Health'}, axis=1)
    tagged_res_l2 = tagged_res_l2.rename({'Language, Communication And Culture': 'Language'}, axis=0)
    tagged_res_l2 = tagged_res_l2.rename({'Language, Communication And Culture': 'Language'}, axis=1)
    tagged_res_l2 = tagged_res_l2.rename({'Earth Sciences': 'Earth'}, axis=0)
    tagged_res_l2 = tagged_res_l2.rename({'Earth Sciences': 'Earth'}, axis=1)
    tagged_res_l2 = tagged_res_l2.rename({'Physical Sciences': 'Physics'}, axis=0)
    tagged_res_l2 = tagged_res_l2.rename({'Physical Sciences': 'Physics'}, axis=1)
    tagged_res_l2 = tagged_res_l2.rename({'Chemical Sciences': 'Chem'}, axis=0)
    tagged_res_l2 = tagged_res_l2.rename({'Chemical Sciences': 'Chem'}, axis=1)
    tagged_res_l2 = tagged_res_l2.rename({'Biological Sciences': 'Biology'}, axis=0)
    tagged_res_l2 = tagged_res_l2.rename({'Biological Sciences': 'Biology'}, axis=1)
    tagged_res_l2 = tagged_res_l2.rename({'Agricultural And Veterinary Sciences': 'Agriculture'}, axis=0)
    tagged_res_l2 = tagged_res_l2.rename({'Agricultural And Veterinary Sciences': 'Agriculture'}, axis=1)
    tagged_res_l2 = tagged_res_l2.rename({'History And Archaeology': 'History'}, axis=0)
    tagged_res_l2 = tagged_res_l2.rename({'History And Archaeology': 'History'}, axis=1)
    tagged_res_l2 = tagged_res_l2.rename({'Law And Legal Studies': 'Law'}, axis=0)
    tagged_res_l2 = tagged_res_l2.rename({'Law And Legal Studies': 'Law'}, axis=1)
    tagged_res_l2 = tagged_res_l2.rename({'Environmental Sciences': 'Environmental'}, axis=0)
    tagged_res_l2 = tagged_res_l2.rename({'Environmental Sciences': 'Environmental'}, axis=1)
    tagged_res_l2 = tagged_res_l2.rename({'Law And Legal Studies': 'Law'}, axis=0)
    tagged_res_l2 = tagged_res_l2.rename({'Law And Legal Studies': 'Law'}, axis=1)
    tagged_res_l2 = tagged_res_l2.rename({'Studies In Creative Arts And Writing': 'Creative'}, axis=0)
    tagged_res_l2 = tagged_res_l2.rename({'Studies In Creative Arts And Writing': 'Creative'}, axis=1)
    tagged_res_l2 = tagged_res_l2.rename({'Commerce, Management, Tourism And Services': 'Tourism'}, axis=0)
    tagged_res_l2 = tagged_res_l2.rename({'Commerce, Management, Tourism And Services': 'Tourism'}, axis=1)
    tagged_res_l2 = tagged_res_l2.rename({'Mathematical Sciences': 'Mathematics'}, axis=0)
    tagged_res_l2 = tagged_res_l2.rename({'Mathematical Sciences': 'Mathematics'}, axis=1)
    tagged_res_l2 = tagged_res_l2.rename({'Philosophy And Religious Studies': 'Religion'}, axis=0)
    tagged_res_l2 = tagged_res_l2.rename({'Philosophy And Religious Studies': 'Religion'}, axis=1)
    tagged_res_l2 = tagged_res_l2.rename({'Studies In Human Society': 'Society'}, axis=0)
    tagged_res_l2 = tagged_res_l2.rename({'Studies In Human Society': 'Society'}, axis=1)
    tagged_res_l2 = tagged_res_l2.rename({'Psychology And Cognitive Sciences': 'Psychology'}, axis=0)
    tagged_res_l2 = tagged_res_l2.rename({'Psychology And Cognitive Sciences': 'Psychology'}, axis=1)
    return tagged_res_l2

def make_and_clean_for(paper_level):
    for_set = set()
    for index, row in paper_level.iterrows():
        paper_fors = row['category_for']
        if paper_fors is not np.nan:
            first_level = paper_fors.split('second_level')[0]
            for_set = for_set.union(set(re.findall(r"'name': '(.*?)'", first_level)))
    df_for = pd.DataFrame(0, columns=list(for_set), index=list(for_set))
    for_list = []
    for index, row in paper_level.iterrows():
        paper_fors = row['category_for']
        if paper_fors is not np.nan:
            first_level = paper_fors.split('second_level')[0]
            for_set_row = set(re.findall(r"'name': '(.*?)'", first_level))
            for_set = for_set.union(for_set_row)
            if len(for_set_row) > 1:
                for field1 in for_set_row:
                    for field2 in for_set_row:
                        if field1 != field2:
                            df_for.at[field1, field2] += 1
                            for_list.append(str(field1) + '; ' + str(field2))
    df_for = df_for.rename({'Information and Computing Sciences': 'IT'}, axis=0)
    df_for = df_for.rename({'Information and Computing Sciences': 'IT'}, axis=1)
    df_for = df_for.rename({'Built Environment and Design': 'Urban'}, axis=0)
    df_for = df_for.rename({'Built Environment and Design': 'Urban'}, axis=1)
    df_for = df_for.rename({'Biological Sciences': 'Biology'}, axis=0)
    df_for = df_for.rename({'Biological Sciences': 'Biology'}, axis=1)
    df_for = df_for.rename({'Health Sciences': 'Health'}, axis=0)
    df_for = df_for.rename({'Health Sciences': 'Health'}, axis=1)
    df_for = df_for.rename({'Language, Communication and Culture': 'Language'}, axis=0)
    df_for = df_for.rename({'Language, Communication and Culture': 'Language'}, axis=1)
    df_for = df_for.rename({'Earth Sciences': 'Earth'}, axis=0)
    df_for = df_for.rename({'Earth Sciences': 'Earth'}, axis=1)
    df_for = df_for.rename({'Physical Sciences': 'Physics'}, axis=0)
    df_for = df_for.rename({'Physical Sciences': 'Physics'}, axis=1)
    df_for = df_for.rename({'Chemical Sciences': 'Chem'}, axis=0)
    df_for = df_for.rename({'Chemical Sciences': 'Chem'}, axis=1)
    df_for = df_for.rename({'Economics': 'Econ'}, axis=1)
    df_for = df_for.rename({'Economics': 'Econ'}, axis=1)
    df_for = df_for.rename({'Biomedical and Clinical Sciences': 'Biolomedical'}, axis=0)
    df_for = df_for.rename({'Biomedical and Clinical Sciences': 'Biolomedical'}, axis=1)
    df_for = df_for.rename({'Agricultural, Veterinary and Food Sciences': 'Agriculture'}, axis=0)
    df_for = df_for.rename({'Agricultural, Veterinary and Food Sciences': 'Agriculture'}, axis=1)
    df_for = df_for.rename({'History, Heritage and Archaeology': 'History'}, axis=0)
    df_for = df_for.rename({'History, Heritage and Archaeology': 'History'}, axis=1)
    df_for = df_for.rename({'Law and Legal Studies': 'Law'}, axis=0)
    df_for = df_for.rename({'Law and Legal Studies': 'Law'}, axis=1)
    df_for = df_for.rename({'Environmental Sciences': 'Environmental'}, axis=0)
    df_for = df_for.rename({'Environmental Sciences': 'Environmental'}, axis=1)
    df_for = df_for.rename({'Creative Arts and Writing': 'Creative'}, axis=0)
    df_for = df_for.rename({'Creative Arts and Writing': 'Creative'}, axis=1)
    df_for = df_for.rename({'Commerce, Management, Tourism and Services': 'Tourism'}, axis=0)
    df_for = df_for.rename({'Commerce, Management, Tourism and Services': 'Tourism'}, axis=1)
    df_for = df_for.rename({'Mathematical Sciences': 'Mathematics'}, axis=0)
    df_for = df_for.rename({'Mathematical Sciences': 'Mathematics'}, axis=1)
    df_for = df_for.rename({'Philosophy and Religious Studies': 'Religion'}, axis=0)
    df_for = df_for.rename({'Philosophy and Religious Studies': 'Religion'}, axis=1)
    df_for = df_for.rename({'Human Society': 'Society'}, axis=0)
    df_for = df_for.rename({'Human Society': 'Society'}, axis=1)
    return df_for, pd.DataFrame(for_list).value_counts()


def make_L1(df_for, data_type):
    L1_for = pd.DataFrame(0, index=['Humanities', 'Social Sciences',
                                        'Natural Sciences', 'Medical Sciences',
                                     'Physical Sciences'],
                             columns=['Humanities', 'Social Sciences',
                                      'Natural Sciences', 'Medical Sciences',
                                      'Physical Sciences'])
    if data_type == 'papers':
        L1_1 = ['Creative', 'Language', 'History', 'Religion']
        L1_2 = ['Urban', 'Education', 'Economics', 'Tourism', 'Society', 'Law']
        L1_3 = ['Physics', 'Chem', 'Earth', 'Environmental', 'Biology', 'Agriculture']
        L1_4 = ['Health', 'Biolomedical', 'Psychology']
        L1_5 = ['Mathematics', 'Engineering', 'IT']
    elif data_type == 'ref_tags':
        L1_1 = ['Creative', 'Language', 'History', 'Religion']
        L1_2 = ['Urban', 'Education', 'Economics', 'Tourism', 'Society', 'Law']
        L1_3 = ['Physics', 'Chem', 'Earth', 'Environmental', 'Biology', 'Agriculture']
        L1_4 = ['Health', 'Biolomedical', 'Psychology']
        L1_5 = ['Mathematics', 'Engineering', 'IT']

    for row in df_for.index:
        for column in df_for.columns:
            if (row in L1_1) and (column in L1_1):
                L1_for.at['Humanities', 'Humanities'] += df_for.at[row, column]
            if row in L1_1 and column in L1_2:
                L1_for.at['Humanities', 'Social Sciences'] += df_for.at[row, column]
            if row in L1_1 and column in L1_3:
                L1_for.at['Humanities', 'Natural Sciences'] += df_for.at[row, column]
            if row in L1_1 and column in L1_4:
                L1_for.at['Humanities', 'Medical Sciences'] += df_for.at[row, column]
            if row in L1_1 and column in L1_5:
                L1_for.at['Humanities', 'Physical Sciences'] += df_for.at[row, column]

            if (row in L1_2) and (column in L1_1):
                L1_for.at['Social Sciences', 'Humanities'] += df_for.at[row, column]
            if row in L1_2 and column in L1_2:
                L1_for.at['Social Sciences', 'Social Sciences'] += df_for.at[row, column]
            if row in L1_2 and column in L1_3:
                L1_for.at['Social Sciences', 'Natural Sciences'] += df_for.at[row, column]
            if row in L1_2 and column in L1_4:
                L1_for.at['Social Sciences', 'Medical Sciences'] += df_for.at[row, column]
            if row in L1_2 and column in L1_5:
                L1_for.at['Social Sciences', 'Physical Sciences'] += df_for.at[row, column]


            if (row in L1_3) and (column in L1_1):
                L1_for.at['Natural Sciences', 'Humanities'] += df_for.at[row, column]
            if row in L1_3 and column in L1_2:
                L1_for.at['Natural Sciences', 'Social Sciences'] += df_for.at[row, column]
            if row in L1_3 and column in L1_3:
                L1_for.at['Natural Sciences', 'Natural Sciences'] += df_for.at[row, column]
            if row in L1_3 and column in L1_4:
                L1_for.at['Natural Sciences', 'Medical Sciences'] += df_for.at[row, column]
            if row in L1_3 and column in L1_5:
                L1_for.at['Natural Sciences', 'Physical Sciences'] += df_for.at[row, column]

            if (row in L1_4) and (column in L1_1):
                L1_for.at['Medical Sciences', 'Humanities'] += df_for.at[row, column]
            if row in L1_4 and column in L1_2:
                L1_for.at['Medical Sciences', 'Social Sciences'] += df_for.at[row, column]
            if row in L1_4 and column in L1_3:
                L1_for.at['Medical Sciences', 'Natural Sciences'] += df_for.at[row, column]
            if row in L1_4 and column in L1_4:
                L1_for.at['Medical Sciences', 'Medical Sciences'] += df_for.at[row, column]
            if row in L1_4 and column in L1_5:
                L1_for.at['Medical Sciences', 'Physical Sciences'] += df_for.at[row, column]


            if (row in L1_5) and (column in L1_1):
                L1_for.at['Physical Sciences', 'Humanities'] += df_for.at[row, column]
            if row in L1_5 and column in L1_2:
                L1_for.at['Physical Sciences', 'Social Sciences'] += df_for.at[row, column]
            if row in L1_5 and column in L1_3:
                L1_for.at['Physical Sciences', 'Natural Sciences'] += df_for.at[row, column]
            if row in L1_5 and column in L1_4:
                L1_for.at['Physical Sciences', 'Medical Sciences'] += df_for.at[row, column]
            if row in L1_5 and column in L1_5:
                L1_for.at['Physical Sciences', 'Physical Sciences'] += df_for.at[row, column]
    return L1_for


def plot_circle(df, title, figure_path, filename):
    fig, ax1 = plt.subplots(1, 1, figsize=(9, 9),
                            subplot_kw=dict(polar=True))
    plot_connectivity_circle(df.replace(0, np.nan).to_numpy(),
                             list(df.index),
                             padding=5,
                             facecolor='white',
                             node_width=12,
                             textcolor='black',
                             node_linewidth=1,
                             linewidth=3,
                             colormap=cmap, vmin=None,
                             vmax=None,
                             colorbar=True,
                             title=title,
                             ax=ax1,
                             fontsize_title=20,
                             node_colors=['w'],
                             colorbar_size=0.75,
                             colorbar_pos=(.4, 0.5),
                             fontsize_names=14,
                             fontsize_colorbar=13)
    savefigures(plt, figure_path, filename)



def make_figure_eighteen():
    print('\n*****************************************************')
    print('***************** Making Figure 18! *******************')
    print('*******************************************************')
    mpl.rcParams['font.family'] = 'Graphik'
    plt.rcParams["axes.labelweight"] = "light"
    plt.rcParams["font.weight"] = "light"

    dim_out = os.path.join(os.getcwd(), '..', '..',
                           'data', 'dimensions_returns')
    df = pd.read_csv(os.path.join(os.getcwd(),
                                  '..',
                                  '..',
                                  'data',
                                  'final',
                                  'enhanced_ref_data.csv'),
                     usecols=['REF impact case study identifier',
                              'Main panel',
                              'Unit of assessment number']
                     )
    df['Unit of assessment number'] = df['Unit of assessment number'].astype(int)
    paper_level = pd.read_excel(os.path.join(dim_out,
                                             'merged_dimensions.xlsx'))
    paper_level = pd.merge(paper_level,
                           df[['Main panel',
                               'Unit of assessment number',
                               'REF impact case study identifier']],
                           how='left',
                           left_on='Key',
                           right_on='REF impact case study identifier'
                           )

    df_for_SOCSCI, for_list_SOCSCI = make_and_clean_for(paper_level[(paper_level['Main panel'] == 'C') |
                                                                    (paper_level['Unit of assessment number'] == 4)])
    df_for_HUM, for_list_HUM = make_and_clean_for(paper_level[(paper_level['Main panel'] == 'D')])

    tagged_res = pd.read_excel(os.path.join(os.getcwd(),
                                            '..',
                                            '..',
                                            'data',
                                            'raw',
                                            'raw_ref_ics_tags_data.xlsx'),
                               sheet_name='Sheet1',
                               skiprows=4,
                               usecols=['REF case study identifier',
                                        'Main panel',
                                        'Unit of assessment number',
                                        'Tag type',
                                        'Tag identifier',
                                        'Tag value',
                                        'Tag group']
                               )

    tagged_res = tagged_res[tagged_res['Tag type'] == 'Underpinning research subject']
    tagged_res_l2_C4 = make_tagged(tagged_res[(tagged_res['Main panel'] == 'C') |
                                              (tagged_res['Unit of assessment number'] == 4)])
    tagged_res_l2_D = make_tagged(tagged_res[(tagged_res['Main panel'] == 'D')])

    L1_for_papers_SOCSCI = make_L1(df_for_SOCSCI, 'papers')
    L1_for_papers_HUM = make_L1(df_for_HUM, 'papers')
    L1_for_tags_SOCSCI = make_L1(tagged_res_l2_C4, 'ref_tags')
    L1_for_tags_HUM = make_L1(tagged_res_l2_D, 'ref_tags')
    figure_path = os.path.join(os.getcwd(), '..', '..', 'figures')

    plot_circle(L1_for_papers_SOCSCI, 'a.', figure_path, 'figure_18a')
    plot_circle(L1_for_papers_HUM, 'b.', figure_path, 'figure_18b')
    plot_circle(L1_for_tags_SOCSCI, 'c.', figure_path, 'figure_18c')
    plot_circle(L1_for_tags_HUM, 'd.', figure_path, 'figure_18d')
