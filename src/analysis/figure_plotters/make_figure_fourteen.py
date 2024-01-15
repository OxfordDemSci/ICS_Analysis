import pandas as pd
import os
import matplotlib as mpl
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
import seaborn as sns
from helpers.figure_helpers import savefigures
mpl.rcParams['font.family'] = 'Graphik'
plt.rcParams["axes.labelweight"] = "light"
plt.rcParams["font.weight"] = "light"
ba_rgb2 = ['#41558c', '#E89818', '#CF202A']

def print_top_bot_scores(scored, string_filter):
    print('For: ' + str(string_filter) + '...')
    print('Top 10 departments with most FTE, mean GPA: ',
          scored.sort_values(by='fte', ascending=False)[0:10]['ICS_GPA'].mean())
    print('Bottom 10 departments with least FTE, mean GPA: ',
          scored.sort_values(by='fte', ascending=True)[0:10]['ICS_GPA'].mean())
    print('Top 10 departments with most Income, mean GPA: ',
          scored.sort_values(by='tot_income', ascending=False)[0:10]['ICS_GPA'].mean())
    print('Bottom 10 departments with least Income, mean GPA: ',
          scored.sort_values(by='tot_income', ascending=True)[0:10]['ICS_GPA'].mean())
    print('Top 10 departments with most Number of Doctoral Degrees, mean GPA: ',
          scored.sort_values(by='num_doc_degrees_total', ascending=False)[0:10]['ICS_GPA'].mean())
    print('Bottom 10 departments with least Number of Doctoral Degrees, mean GPA: ',
          scored.sort_values(by='num_doc_degrees_total', ascending=True)[0:10]['ICS_GPA'].mean())


def make_figure_fourteen():
    print('\n*****************************************************')
    print('***************** Making Figure 14! *******************')
    print('*******************************************************')
    df = pd.read_csv(os.path.join(os.getcwd(),
                                  '..',
                                  '..',
                                  'data',
                                  'final',
                                  'enhanced_ref_data.csv'),
#                     index_col=0,
                     usecols=['Institution name',
                              'Main panel',
                              'Unit of assessment number',
                              'ICS_GPA',
                              'num_doc_degrees_total',
                              'fte',
                              'tot_income']
                     )
    df['Unit of assessment number'] = df['Unit of assessment number'].astype(int)
    figure_path = os.path.join(os.getcwd(), '..', '..', 'figures')
    colors = ba_rgb2
    subset = ['Institution name', 'Unit of assessment number']
    scored = df.drop_duplicates(subset=subset)
    counter = pd.Series(df.groupby(subset).size(), name='size').reset_index()
    scored = scored.copy()
    scored = pd.merge(scored, counter, left_on=subset, right_on=subset)
    uoa4_mask = (scored['Unit of assessment number'] == 4)
    panelc_mask = (scored['Main panel'] == 'C')
    paneld_mask = (scored['Main panel'] == 'D')
    scored = pd.merge(scored,
                      counter,
                      how='inner',
                      left_on=subset,
                      right_on=subset)
    size = 60
    scored = scored[['Institution name',
                     'Main panel',
                     'Unit of assessment number',
                     'ICS_GPA',
                     'num_doc_degrees_total',
                     'fte',
                     'tot_income']]
    shape_mask = ((scored['Main panel'] == 'C') |
                  (scored['Main panel'] == 'D') |
                  (scored['Unit of assessment number'] == 4))
    scored_shape = scored[shape_mask]
    scored_nonshape = scored[~shape_mask]
    scored_uoa4 = scored[scored['Unit of assessment number'] == 4]
    scored_panelc = scored[scored['Main panel'] == 'C']
    scored_paneld = scored[scored['Main panel'] == 'D']
    print(f'STEM ICS GPA mean: ',
          round(scored_nonshape['ICS_GPA'].mean(), 2))
    print(f'SHAPE ICS GPA mean: ',
          round(scored_shape['ICS_GPA'].mean(),2 ))
    print(f'UoA 4 ICS GPA mean: ',
          round(scored_uoa4['ICS_GPA'].mean(), 2))
    print(f'Panel C ICS GPA mean: ',
          round(scored_panelc['ICS_GPA'].mean(), 2))
    print(f'Panel D ICS GPA mean: ',
          round(scored_paneld['ICS_GPA'].mean(), 2))
    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(12, 10))
    nbins = 18
    label_fontsize = 18
    sns.distplot(scored_uoa4['ICS_GPA'],
                 hist_kws={'facecolor': colors[0],
                           'edgecolor': 'k',
                           'alpha': 1},
                 kde_kws={'color': colors[1]}, ax=ax1, bins=nbins)
    sns.distplot(scored_panelc['ICS_GPA'],
                 hist_kws={'facecolor': colors[0],
                           'edgecolor': 'k',
                           'alpha': 1},
                 kde_kws={'color': colors[1]}, ax=ax2, bins=nbins)
    sns.distplot(scored_paneld['ICS_GPA'],
                 hist_kws={'facecolor': colors[0],
                           'edgecolor': 'k',
                           'alpha': 1},
                 kde_kws={'color': colors[1]}, ax=ax3, bins=nbins)
    ax1.grid(which="both", linestyle='--', alpha=0.3)
    ax2.grid(which="both", linestyle='--', alpha=0.3)
    ax3.grid(which="both", linestyle='--', alpha=0.3)
    sns.despine()
    legend_elements3 = [Patch(facecolor=colors[0], edgecolor='k',
                              label=r'Bins', alpha=1),
                        Line2D([0], [0], color=colors[1], lw=1, linestyle='-',
                               label=r'KDE', alpha=1)]
    ax1.legend(handles=legend_elements3,
               frameon=True,
               fontsize=15, framealpha=1, facecolor='w',
               edgecolor=(0, 0, 0, 1),
               title='GPA', title_fontsize=14
              )

    ax1.set_xlabel('ICS GPA (UoA 4)', fontsize=14)
    ax2.set_xlabel('ICS GPA (Panel C)', fontsize=14)
    ax3.set_xlabel('ICS GPA (Panel D)', fontsize=14)
    ax1.set_ylabel('Density', fontsize=14)
    ax2.set_ylabel('', fontsize=label_fontsize)
    ax3.set_ylabel('', fontsize=label_fontsize)
    ax1.set_xlim(-0.5, 4.5)
    ax2.set_xlim(-0.5, 4.5)
    ax3.set_xlim(-0.5, 4.5)
    ax1.set_ylim(0, 1)
    ax2.set_ylim(0, 1)
    ax3.set_ylim(0, 1)
    ax1.tick_params(axis='both', which='major', labelsize=14)
    ax2.tick_params(axis='both', which='major', labelsize=14)
    ax3.tick_params(axis='both', which='major', labelsize=14)
    ax1.set_title('a.', loc='left', fontsize=18, y=1.035)
    ax2.set_title('b.', loc='left', fontsize=18, y=1.035)
    ax3.set_title('c.', loc='left', fontsize=18, y=1.035)

    # second row

    ax4.scatter(y=scored[panelc_mask]['ICS_GPA'],
                x=scored[panelc_mask]['fte'],
                color=colors[0], s=size, edgecolor=(0, 0, 0, 1),
                linewidth=.5)
    ax4.scatter(y=scored[paneld_mask]['ICS_GPA'],
                x=scored[paneld_mask]['fte'],
                color=colors[1], s=size, edgecolor=(0, 0, 0, 1),
                linewidth=.5)
    ax4.scatter(y=scored[uoa4_mask]['ICS_GPA'],
    x=scored[uoa4_mask]['fte'],
                color=colors[2], s=size, edgecolor=(0, 0, 0, 1),
                linewidth=.5)

    ax5.scatter(y=scored[panelc_mask]['ICS_GPA'],
                x=scored[panelc_mask]['tot_income'].div(1000000),
                color=colors[0], s=size, edgecolor=(0, 0, 0, 1),
                linewidth=.5)
    ax5.scatter(y=scored[paneld_mask]['ICS_GPA'],
                x=scored[paneld_mask]['tot_income'].div(1000000),
                color=colors[1], s=size, edgecolor=(0, 0, 0, 1),
                linewidth=.5)
    ax5.scatter(y=scored[uoa4_mask]['ICS_GPA'],
                x=scored[uoa4_mask]['tot_income'].div(1000000),
                color=colors[2], s=size, edgecolor=(0, 0, 0, 1),
                linewidth=.5)

    ax6.scatter(y=scored[panelc_mask]['ICS_GPA'],
                x=scored[panelc_mask]['num_doc_degrees_total'],
                color=colors[0], s=size, edgecolor=(0, 0, 0, 1),
                linewidth=.5)
    ax6.scatter(y=scored[paneld_mask]['ICS_GPA'],
                x=scored[paneld_mask]['num_doc_degrees_total'],
                color=colors[1], s=size, edgecolor=(0, 0, 0, 1),
                linewidth=.5)
    ax6.scatter(y=scored[uoa4_mask]['ICS_GPA'],
                x=scored[uoa4_mask]['num_doc_degrees_total'],
                color=colors[2], s=size, edgecolor=(0, 0, 0, 1),
                linewidth=.5)

    legend_elements1 = [Line2D([], [], marker='o',
                               markerfacecolor=colors[2], markeredgecolor='k',
                               label=r'UoA 4', linewidth=0, markersize=10),
                        Line2D([], [], marker='o',
                               markerfacecolor=colors[0], markeredgecolor='k',
                               label=r'Panel C', linewidth=0, markersize=10),
                        Line2D([], [], marker='o',
                               markerfacecolor=colors[1], markeredgecolor='k',
                                label=r'Panel D', linewidth=0, markersize=10)]
    for ax, title in zip([ax4, ax5, ax6], ['d.', 'e.', 'f.']):
        ax.yaxis.grid(linestyle='--', alpha=0.3)
        ax.xaxis.grid(linestyle='--', alpha=0.3)
        ax.set_title(title, loc='left', fontsize=18)
        ax.tick_params(axis='both', which='major', labelsize=14)
    ax6.legend(handles=legend_elements1, loc='lower right', frameon=True,
               fontsize=14, framealpha=1, facecolor='w',
               edgecolor=(0, 0, 0, 1),
               title='Subject Area', title_fontsize=14)
    ax4.set_ylabel('Departmental GPA', fontsize=14)
    ax4.set_xlabel('Full Time Employed', fontsize=14)
    ax5.set_xlabel('Total Income (£m)', fontsize=14)
    ax6.set_xlabel('Doctoral Degrees Conferred', fontsize=14)
    ax4.yaxis.set_major_locator(plt.MaxNLocator(5))
    ax5.yaxis.set_major_locator(plt.MaxNLocator(5))
    ax6.yaxis.set_major_locator(plt.MaxNLocator(5))
    ax4.set_ylim(0.25, 4.25)
    ax5.set_ylim(0.25, 4.25)
    ax6.set_ylim(0.25, 4.25)
    plt.tight_layout()
    sns.despine(offset=5, trim=True)
    file_name = 'figure_14'
    savefigures(plt, figure_path, file_name)

    print_top_bot_scores(scored[(scored['Main panel'] == 'C') |
                                (scored['Main panel'] == 'D') |
                                (scored['Unit of assessment number'] == 4)],
                         'All SHAPE')
    print_top_bot_scores(scored[(scored['Main panel'] == 'C')],
                         'Panel C')
    print_top_bot_scores(scored[(scored['Main panel'] == 'D')],
                         'Panel D')
    print_top_bot_scores(scored[(scored['Unit of assessment number'] == 4)],
                         'UoA 4')
