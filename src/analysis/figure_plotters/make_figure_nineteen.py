import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib as mpl
import seaborn as sns
import gender_guesser.detector as gender
from matplotlib.patches import Patch
from helpers.figure_helpers import savefigures
mpl.rcParams['font.family'] = 'Graphik'
new_rc_params = {'text.usetex': False,
"svg.fonttype": 'none'
}
mpl.rcParams.update(new_rc_params)
d = gender.Detector()


def get_gender():
    dim_out = os.path.join(os.getcwd(),
                           '..',
                           '..',
                           'data',
                           'dimensions_returns')
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
                           right_on='REF impact case study identifier')
    author_level = pd.DataFrame(columns=['Panel',
                                         'UoA',
                                         'ICS_uid',
                                         'pub_uid',
                                         'first_name',
                                         'gender']
                                )
    counter = 0

    for index, row in paper_level.iterrows():
        paper_authors = row['authors']
        if paper_authors != np.nan:
            name_list = re.findall(r"'first_name': '(.*?)', 'last_name'", paper_authors)
            for name in name_list:
                author_level.at[counter, 'Panel'] = row['Main panel']
                author_level.at[counter, 'UoA'] = int(row['Unit of assessment number'])
                author_level.at[counter, 'ICS_uid'] = row['Key']
                author_level.at[counter, 'pub_uid'] = row['id']
                author_level.at[counter, 'first_name'] = name
                author_level.at[counter, 'gender'] = d.get_gender(name)
                counter += 1
    author_level['female'] = np.where(author_level['gender'] == 'female', 1, 0)
    author_level['female'] = np.where(author_level['gender'] == 'mostly_female', 1, author_level['female'])
    author_level = author_level[author_level['gender'] != 'unknown']
    author_level = author_level[author_level['gender'] != 'andy']
    paper_panels = author_level.groupby(['Panel'])['female'].mean()
    uoa_fem = pd.DataFrame(author_level.groupby(['UoA'])['female'].mean())
    return author_level, uoa_fem, paper_panels


def plot_gender(uoa_fem, paper_panels, figure_path):
    fig, (ax1) = plt.subplots(1, 1, figsize=(14, 7))
    uoa_fem.plot(kind='bar', ax=ax1, ec='k', alpha=1)
    mpl.rcParams['font.family'] = 'Graphik'
    new_rc_params = {'text.usetex': False,
                     "svg.fonttype": 'none'
                     }
    mpl.rcParams.update(new_rc_params)
    ba_rgb2 = ['#41558c', '#E89818', '#CF202A']
    plt.tight_layout()
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=0, fontsize=14)
    ax1.set_xlabel('Unit of Assessment Number', fontsize=20)
    for ax in [ax1]:
        for uoa in range(0, 13):
            ax.get_children()[uoa].set_color(ba_rgb2[0])
            ax.get_children()[uoa].set_edgecolor('k')
            ax.get_children()[3].set_color(ba_rgb2[1])
            ax.get_children()[3].set_edgecolor('k')
        for uoa in range(13, 34):
            ax.get_children()[uoa].set_color(ba_rgb2[1])
            ax.get_children()[uoa].set_edgecolor('k')
    legend_elements = [Patch(facecolor=ba_rgb2[0], edgecolor='k',
                             label=r'STEM', alpha=1),
                       Patch(facecolor=ba_rgb2[1], edgecolor='k',
                             label=r'SHAPE', alpha=1)]
    ax1.tick_params(axis='both', which='major', labelsize=16)
    for ax in [ax1]:
        ax.legend(handles=legend_elements,
                  frameon=True,
                  fontsize=15, framealpha=1, facecolor='w',
                  edgecolor=(0, 0, 0, 1), ncol=1,
                  loc='upper right', bbox_to_anchor=(1.01, 0.92)
                  )
#    ax1.set_title('A.', loc='left', fontsize=24, x=-.025, y=1.025)
    ax1.set_ylabel('Percent Female', fontsize=18)
    ax1.set_ylim(0, 65)
    A_cited = pd.DataFrame(paper_panels).at['A', 'female']
    B_cited = pd.DataFrame(paper_panels).at['B', 'female']
    C_cited = pd.DataFrame(paper_panels).at['C', 'female']
    D_cited = pd.DataFrame(paper_panels).at['D', 'female']
    draw_brace(ax1, (0, 6), 60, 'Panel A: ' + str(round(A_cited, 2)))
    draw_brace(ax1, (7, 12), 60, 'Panel B: ' + str(round(B_cited, 2)))
    draw_brace(ax1, (13, 24), 60, 'Panel C: ' + str(round(C_cited, 2)))
    draw_brace(ax1, (25, 33), 60, 'Panel D: ' + str(round(D_cited, 2)))
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.tight_layout()
    sns.despine(offset=5, trim=True)
    filename = 'figure_19'
    savefigures(plt, figure_path, filename)


def draw_brace(ax, xspan, yminn, text):
    """Draws an annotated brace on the axes."""
    xmin, xmax = xspan
    xspan = xmax - xmin
    ax_xmin, ax_xmax = ax.get_xlim()
    xax_span = ax_xmax - ax_xmin
    ymin, ymax = ax.get_ylim()
    yspan = ymax - ymin
    resolution = int(xspan / xax_span * 100) * 2 + 1
    beta = 300. / xax_span
    x = np.linspace(xmin, xmax, resolution)
    x_half = x[:resolution // 2 + 1]
    y_half_brace = (1 / (1. + np.exp(-beta * (x_half - x_half[0])))
                    + 1 / (1. + np.exp(-beta * (x_half - x_half[-1]))))
    y = np.concatenate((y_half_brace, y_half_brace[-2::-1]))
    y = yminn + (.05 * y - .01) * yspan
    ax.autoscale(False)
    ax.plot(x, y, color='black', lw=1)
    ax.text((xmax + xmin) / 2., yminn + (yminn / 40) + .065 * yspan,
            text + '%', ha='center', va='bottom', fontsize=16)



def make_figure_nineteen():
    print('\n******************************************************')
    print('***************** Making Figure 19! ********************')
    print('********************************************************')
    figure_path = os.path.join(os.getcwd(),
                               '..',
                               '..',
                               'figures')
    author_level, uoa_fem, paper_panels = get_gender()
    paper_panels = paper_panels * 100
    uoa_fem = uoa_fem * 100
    mpl.rcParams['font.family'] = 'Graphik'
    new_rc_params = {'text.usetex': False,
                     "svg.fonttype": 'none'
                     }
    mpl.rcParams.update(new_rc_params)
    author_level_SHAPE = author_level[(author_level['Panel'] == 'C') |
                                      (author_level['Panel'] == 'D') |
                                      (author_level['UoA'] == 4)]
    author_level_STEM = author_level[((author_level['Panel'] == 'A') |
                                      (author_level['Panel'] == 'B')) &
                                     (author_level['UoA'] != 4)]
    author_level_PanelC = author_level[author_level['Panel'] == 'C']
    author_level_PanelD = author_level[author_level['Panel'] == 'D']
    print('************ ALL data ************')
    print(author_level['first_name'].value_counts()[0:20])
    print('************ STEM data ************')
    print(author_level_STEM['first_name'].value_counts()[0:20])
    print('************ SHAPE data ************')
    print(author_level_SHAPE['first_name'].value_counts()[0:20])
    print('************ Panel C ************')
    print(author_level_PanelC['first_name'].value_counts()[0:20])
    print('************ Panel D ************')
    print(author_level_PanelD['first_name'].value_counts()[0:20])
    print('Saving %female dataframe to ./tables')
    uoa_fem.to_csv(os.path.join(os.getcwd(), '..', '..', 'tables', 'percent_female_uoa.csv'))
    plot_gender(uoa_fem, paper_panels, figure_path)
