import re
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.colors
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from helpers.figure_helpers import savefigures

mpl.rcParams['font.family'] = 'Graphik'
plt.rcParams["axes.labelweight"] = "light"
plt.rcParams["font.weight"] = "light"
mpl.rcParams['font.family'] = 'Graphik'
new_rc_params = {'text.usetex': False,
"svg.fonttype": 'none'
}
mpl.rcParams.update(new_rc_params)
dim_out = os.path.join(os.getcwd(), '..', '..',
                       'data', 'dimensions_returns')


def make_tagged(tagged_res):
    tagged_res_l2 = pd.DataFrame(0,
                                 index=tagged_res['Tag group'].unique(),
                                 columns=tagged_res['Tag group'].unique())
    for_list = []
    for ICS in tagged_res['REF case study identifier'].unique():
        temp = tagged_res[tagged_res['REF case study identifier'] == ICS]
        counter = 0
        for group1 in temp['Tag group']:
            for group2 in temp['Tag group']:
                if group1 != group2:
                    tagged_res_l2.at[group1, group2] += 1
                    for_list.append(str(group1) + '; ' + str(group2))
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
    return tagged_res_l2, pd.DataFrame(for_list).value_counts()

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


def make_figure_seventeen():
    print('\n******************************************************')
    print('***************** Making Figure 17! ********************')
    print('********************************************************')
    figure_path = os.path.join(os.getcwd(),
                               '..',
                               '..',
                               'figures')
    df = pd.read_csv(os.path.join(os.getcwd(),
                                  '..',
                                  '..',
                                  'data',
                                  'final',
                                  'enhanced_ref_data.csv'
                                  ),
                     usecols=['Main panel',
                              'Unit of assessment number',
                              'REF impact case study identifier']
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

    df_for_SOCSCI, for_list_SOCSCI = make_and_clean_for(
        paper_level[(paper_level['Main panel'] =='C') |
                    (paper_level['Unit of assessment number'] == 4)])

    print('The five most common multi-disciplinarity areas in the '
          'Social Sciences from Underpinning Research at the article level are: ' +
          # Note the skip-indexing because a & b = b & a due to symmetry
          str(for_list_SOCSCI.index[0][0]) + ' (' + str(for_list_SOCSCI[0]) + '), ' +
          str(for_list_SOCSCI.index[2][0]) + ' (' + str(for_list_SOCSCI[2]) + '), ' +
          str(for_list_SOCSCI.index[4][0]) + ' (' + str(for_list_SOCSCI[4]) + '), ' +
          str(for_list_SOCSCI.index[6][0]) + ' (' + str(for_list_SOCSCI[6]) + '), ' +
          str(for_list_SOCSCI.index[8][0]) + ' (' + str(for_list_SOCSCI[8]) + ').')

    df_for_HUM, for_list_HUM = make_and_clean_for(
        paper_level[
            (paper_level['Main panel'] == 'D')]
    )

    print('The five most common multi-disciplinarity areas in the '
          'Humanities from Underpinning Research at the article level are: ' +
          # Note the skip-indexing because a & b = b & a due to symmetry
          str(for_list_HUM.index[0][0]) + ' (' + str(for_list_HUM[0]) + '), ' +
          str(for_list_HUM.index[2][0]) + ' (' + str(for_list_HUM[2]) + '), ' +
          str(for_list_HUM.index[4][0]) + ' (' + str(for_list_HUM[4]) + '), ' +
          str(for_list_HUM.index[6][0]) + ' (' + str(for_list_HUM[6]) + '), ' +
          str(for_list_HUM.index[8][0]) + ' (' + str(for_list_HUM[8]) + ').')

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

    tagged_res = tagged_res[tagged_res['Tag type']=='Underpinning research subject']
    tagged_res_l2_C4, tagged_list_C4 = make_tagged(tagged_res[(tagged_res['Main panel'] == 'C') |
                                                              (tagged_res['Unit of assessment number'] == 4.0)])
    print('The five most common multi-disciplinarity areas in the '
          'Social Sciences from REF tags are: ' +
          # Note the skip-indexing because a & b = b & a due to symmetry
          str(tagged_list_C4.index[0][0]) + ' (' + str(tagged_list_C4[0]) + '), ' +
          str(tagged_list_C4.index[2][0]) + ' (' + str(tagged_list_C4[2]) + '), ' +
          str(tagged_list_C4.index[4][0]) + ' (' + str(tagged_list_C4[4]) + '), ' +
          str(tagged_list_C4.index[6][0]) + ' (' + str(tagged_list_C4[6]) + '), ' +
          str(tagged_list_C4.index[8][0]) + ' (' + str(tagged_list_C4[8]) + ').')


    tagged_res_l2_D, tagged_list_D = make_tagged(tagged_res[(tagged_res['Main panel'] == 'D')])
    print('The five most common multi-disciplinarity areas in the '
          'Humanities from REF tags are: ' +
          # Note the skip-indexing because a & b = b & a due to symmetry
          str(tagged_list_D.index[0][0]) + ' (' + str(tagged_list_D[0]) + '), ' +
          str(tagged_list_D.index[2][0]) + ' (' + str(tagged_list_D[2]) + '), ' +
          str(tagged_list_D.index[4][0]) + ' (' + str(tagged_list_D[4]) + '), ' +
          str(tagged_list_D.index[6][0]) + ' (' + str(tagged_list_D[6]) + '), ' +
          str(tagged_list_D.index[8][0]) + ' (' + str(tagged_list_D[8]) + ').')

    ba_rgb2 = ['white', '#41558c', '#E89818', '#CF202A']
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("",
                                                               ba_rgb2
#                                                               ['white', #FFB600', '#00A9DF']
                                                               )
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 12))
    fig.subplots_adjust(hspace=.5, wspace=0.45)

    df_for_SOCSCI = df_for_SOCSCI.sort_index(axis=1)
    df_for_SOCSCI = df_for_SOCSCI.sort_index(axis=0)
    ax1.set_title('a.', loc='left', fontsize=20, y=1.025, x=-.075, fontweight='bold')
    sns.heatmap(df_for_SOCSCI,
                cmap=cmap,
                linewidths=.5,
                linecolor='w',
                ax=ax1,
                cbar=False
                )
    fig.colorbar(ax1.collections[0], ax=ax1, location="right", use_gridspec=False, pad=0.035,
                 shrink=1, anchor = (0, 0))
    sns.heatmap(df_for_SOCSCI,
                cmap=cmap,
                norm=LogNorm(),
                linewidths=.5,
                linecolor='w',
                ax=ax1,
                cbar=False
                )

    cbar_ax = fig.axes[-1]
    cbar_ax.set_title('Number of Pieces of Research', y=.15, x=4.5, rotation=270, fontsize=14)
    cbar_solids = cbar_ax.collections[0]
    cbar_solids.set_edgecolor("black")
    cbar_solids.set_linewidth(1)  # Adjust the linewidth if necessary
    cbar_ax.tick_params(axis='both', which='major', labelsize=12)
    ax2.set_title('b.', loc='left', fontsize=20, y=1.025, x=-.075, fontweight='bold')
    df_for_HUM = df_for_HUM.sort_index(axis=1)
    df_for_HUM = df_for_HUM.sort_index(axis=0)
    sns.heatmap(df_for_HUM,
                cmap=cmap,
                linewidths=.5,
                linecolor='w',
                ax=ax2,
                cbar=False
                )
    fig.colorbar(ax2.collections[0], ax=ax2, location="right", use_gridspec=False, pad=0.035,
                 shrink=1, anchor = (0, 0))
    sns.heatmap(df_for_HUM,
                cmap=cmap,
                norm=LogNorm(),
                linewidths=.5,
                linecolor='w',
                ax=ax2,
                cbar=False
                )
    mpl.rcParams['font.family'] = 'Graphik'
    plt.rcParams["axes.labelweight"] = "light"
    plt.rcParams["font.weight"] = "light"
    new_rc_params = {'text.usetex': False,
                     "svg.fonttype": 'none'
                     }
    mpl.rcParams.update(new_rc_params)
    cbar_ax = fig.axes[-1]
    cbar_solids = cbar_ax.collections[0]
    cbar_solids.set_edgecolor("black")
    cbar_solids.set_linewidth(1)  # Adjust the linewidth if necessary
    cbar_ax.tick_params(axis='both', which='major', labelsize=12)
    cbar_ax.set_title('Number of Pieces of Research', y=.15, x=4.5, rotation=270, fontsize=14)
    tagged_res_l2_C4 = tagged_res_l2_C4.sort_index(axis=1)
    tagged_res_l2_C4 = tagged_res_l2_C4.sort_index(axis=0)
    mask = np.triu(np.ones_like(df_for_HUM))
    ax3.set_title('c.', loc='left', fontsize=20, y=1.025, x=-.075, fontweight='bold')
    sns.heatmap(tagged_res_l2_C4,
                cmap=cmap,
                linewidths=.5,
                linecolor='w',
                ax=ax3,
                cbar=False
                )
    fig.colorbar(ax3.collections[0], ax=ax3, location="right", use_gridspec=False, pad=0.035,
                 shrink=1, anchor = (0, 0))
    sns.heatmap(tagged_res_l2_C4,
                cmap=cmap,
                norm=LogNorm(),
                linewidths=.5,
                linecolor='w',
                ax=ax3,
                cbar=False
                )
    cbar_ax = fig.axes[-1]
    cbar_ax.set_title('REF ICS Tags', y=.325, x=4.5, rotation=270, fontsize=14)
    cbar_solids = cbar_ax.collections[0]
    cbar_solids.set_edgecolor("black")
    cbar_solids.set_linewidth(1)
    cbar_ax.tick_params(axis='both', which='major', labelsize=12)

    tagged_res_l2_D = tagged_res_l2_D.sort_index(axis=1)
    tagged_res_l2_D = tagged_res_l2_D.sort_index(axis=0)
    ax4.set_title('d.', loc='left', fontsize=20, y=1.025, x=-.075, fontweight='bold')
    sns.heatmap(tagged_res_l2_D,
                cmap=cmap,
                linewidths=.5,
                linecolor='w',
                ax=ax4,
                cbar=False
                )
    fig.colorbar(ax4.collections[0], ax=ax4, location="right", use_gridspec=False, pad=0.035,
                 shrink=1, anchor = (0, 0))
    sns.heatmap(tagged_res_l2_D,
                cmap=cmap,
                norm=LogNorm(),
                linewidths=.5,
                linecolor='w',
                ax=ax4,
                cbar=False
                )
    cbar_ax = fig.axes[-1]
    cbar_ax.set_title('REF ICS Tags', y=.325, x=4.5, rotation=270, fontsize=14)
    cbar_solids = cbar_ax.collections[0]
    cbar_solids.set_edgecolor("black")
    cbar_solids.set_linewidth(1)  # Adjust the linewidth if necessary
    cbar_ax.tick_params(axis='both', which='major', labelsize=12)

    sns.despine(offset=10, trim=True, ax=ax1, top=False, right=True)
    sns.despine(offset=10, trim=True, ax=ax2, top=False, right=True)
    sns.despine(offset=10, trim=True, ax=ax3, top=False, right=True)
    sns.despine(offset=10, trim=True, ax=ax4, top=False, right=True)
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90, ha='right')
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90, ha='right')
    ax3.set_xticklabels(ax2.get_xticklabels(), rotation=90, ha='right')
    ax4.set_xticklabels(ax2.get_xticklabels(), rotation=90, ha='right')
    filename = 'figure_17'
    savefigures(plt, figure_path, filename)