import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.ticker as tkr
import matplotlib.pyplot as plt
import matplotlib as mpl
import json
import warnings
from matplotlib.colors import LogNorm
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from nltk.stem.snowball import SnowballStemmer
from text_helpers import freq_dist, co_occurrence, set_diag, truncate_colormap
from matplotlib import gridspec
warnings.filterwarnings('ignore')
mpl.rc('font', family='Helvetica')
csfont = {'fontname': 'Helvetica'}
hfont = {'fontname': 'Helvetica'}

def make_word_vis(df1, df2, fieldname, figure_path, support_path):
    #stop_list = pd.read_csv(os.path.join(support_path,
    #                                     'custom_stopwords.txt'))
    #custom_stop = stop_list['words'].to_list() # @TODO: these don't actually get used?

    df1_dist, df1_words = freq_dist(df1, 'english', 'lemmatized_' + fieldname)
    df2_dist, df2_words = freq_dist(df2, 'english', 'lemmatized_' + fieldname)
    en_stemmer = SnowballStemmer('english')

    wordlist = []
    for elem in df1_words:
        wordlist.append(' '.join([en_stemmer.stem(w) for w in elem.split(' ') if w.isalnum()]))
    df1_words_mat = co_occurrence(wordlist, 5)

    wordlist = []
    for elem in df2_words:
        wordlist.append(' '.join([en_stemmer.stem(w) for w in elem.split(' ') if w.isalnum()]))
    df2_words_mat = co_occurrence(wordlist, 5)
    matsize = 25

#    df1_sum = df1_words_mat.sum().sum() # @TODO check that these don't actually get used?
#    df2_sum = df2_words_mat.sum().sum()

    df1_tot_row = pd.DataFrame(df1_words_mat.sum())
    df1_tot_row = df1_tot_row.sort_values(by=0, ascending=False)[0:matsize]

    df1_words_mat = df1_words_mat[df1_tot_row.index.to_list()]
    df1_words_mat = df1_words_mat.reindex(index=df1_tot_row.index.to_list())

    df2_tot_row = pd.DataFrame(df2_words_mat.sum())
    df2_tot_row = df2_tot_row.sort_values(by=0, ascending=False)[0:matsize]
    df2_words_mat = df2_words_mat[df2_tot_row.index.to_list()]
    df2_words_mat = df2_words_mat.reindex(index=df2_tot_row.index.to_list())

    df1_mask = np.zeros_like(df1_words_mat.iloc[0:matsize, 0:matsize], dtype=np.int16)
    df1_mask[np.triu_indices_from(df1_mask)] = True

    df2_mask = np.zeros_like(df2_words_mat.iloc[0:matsize, 0:matsize], dtype=np.int16)
    df2_mask[np.triu_indices_from(df2_mask)] = True
    pd.DataFrame.set_diag = set_diag
    df1_words_mat.astype(float).set_diag(np.nan)
    df2_words_mat.astype(float).set_diag(np.nan)

    sns.set_style('ticks')
    fig = plt.figure(figsize=(16, 13))
    ax1 = plt.subplot2grid((49, 48), (0, 0), rowspan=21, colspan=24)
    ax2 = plt.subplot2grid((49, 48), (0, 26), rowspan=21, colspan=20, projection='polar')
    ax3 = plt.subplot2grid((49, 48), (28, 0), rowspan=21, colspan=20, projection='polar')
    ax4 = plt.subplot2grid((49, 48), (28, 22), rowspan=21, colspan=24)
    ax1.set_title('A.', loc='left', y=1.01, **hfont, fontsize=21, x=-.05)
    ax2.set_title('B.', loc='left', y=1.01, **hfont, fontsize=21, x=-.35)
    ax3.set_title('C.', loc='left', y=1.01, **hfont, fontsize=22, x=-.20)
    ax4.set_title('D.', loc='left', y=1.01, **hfont, fontsize=21, x=0)
    formatter = tkr.ScalarFormatter(useMathText=True)
    formatter.set_scientific(False)
    cmap = plt.get_cmap('RdBu_r')
    cmap = truncate_colormap(cmap, 0.0, 1)

    ax_df1 = sns.heatmap(df1_words_mat.astype(float),
                         norm=LogNorm(1 + df1_words_mat.astype(float).min().min(),
                                      df1_words_mat.astype(float).max().max()),
                         cbar_kws={'ticks': [200, 400, 800, 1600, 3200],
                                   "shrink": 1, 'use_gridspec': True,
                                   "format": formatter},
                         mask=df1_mask,
                         vmin=1,
                         vmax=250,
                         cmap=cmap,
                         linewidths=.25,
                         ax=ax1)
    ax_df1.collections[0].colorbar.outline.set_edgecolor('k')
    ax_df1.collections[0].colorbar.outline.set_linewidth(1)
    ax_df1.collections[0].colorbar.ax.yaxis.set_ticks_position('left')

    iN = len(df1_dist[0:matsize]['count'])
    labs = df1_dist[0:matsize].index
    arrCnts = np.array(df1_dist[0:matsize]['count']) + .5
    theta = np.arange(0, 2 * np.pi, 2 * np.pi / (iN))
    width = (5 * np.pi) / iN
    bottom = 0.5
    ax2.set_theta_zero_location('W')
    ax2.plot(theta, len(theta) * [0.55], alpha=0.5, color='k', linewidth=1, linestyle='--')
    bars = ax2.plot(theta, arrCnts, alpha=1, linestyle='-', marker='o',
                    color='#377eb8', markersize=7, markerfacecolor='w',
                    markeredgecolor='#ff5148')
    ax2.axis('off')
    rotations = np.rad2deg(theta)
    y0, y1 = ax2.get_ylim()
    for x, bar, rotation, label in zip(theta, arrCnts, rotations, labs):
        offset = (bottom + bar) / (y1 - y0)
        lab = ax2.text(0, 0, label, transform=None,
                       ha='center', va='center')
        renderer = ax2.figure.canvas.get_renderer()
        bbox = lab.get_window_extent(renderer=renderer)
        invb = ax2.transData.inverted().transform([[0, 0], [bbox.width, 0]])
        lab.set_position((x, offset + (invb[1][0] - invb[0][0]) + .1))
        lab.set_transform(ax2.get_xaxis_transform())
        lab.set_rotation(rotation)
    ax2.fill_between(theta, arrCnts, alpha=0.075, color='#4e94ff')
    ax2.fill_between(theta, len(theta) * [0.55], alpha=1, color='w')
    circle = plt.Circle((0.0, 0.0), 0.1, transform=ax2.transData._b, color="k", alpha=0.3)
    ax2.add_artist(circle)
    ax2.plot((0, theta[0]), (0, arrCnts[0]),
             color='k', linewidth=1, alpha=0.5, linestyle='--')
    ax2.plot((0, theta[-1]), (0, arrCnts[-1]),
             color='k', linewidth=1, alpha=0.5, linestyle='--')

    iN = len(df2_dist[0:matsize]['count'])
    labs = df2_dist[0:matsize].index
    arrCnts = np.array(df2_dist[0:matsize]['count']) + .5
    theta = np.arange(0, 2 * np.pi, 2 * np.pi / (iN))
    width = (5 * np.pi) / iN
    bottom = 0.5
    ax3.set_theta_zero_location('W')
    ax3.plot(theta, len(theta) * [0.55], alpha=0.5, color='k', linewidth=1, linestyle='--')
    bars = ax3.plot(theta, arrCnts, alpha=1, linestyle='-', marker='o',
                    color='#377eb8', markersize=7, markerfacecolor='w',
                    markeredgecolor='#ff5148')
    ax3.axis('off')
    rotations = np.rad2deg(theta)
    y0, y1 = ax3.get_ylim()
    for x, bar, rotation, label in zip(theta, arrCnts, rotations, labs):
        offset = (bottom + bar) / (y1 - y0)
        lab = ax3.text(0, 0, label, transform=None,
                       ha='center', va='center')
        renderer = ax3.figure.canvas.get_renderer()
        bbox = lab.get_window_extent(renderer=renderer)
        invb = ax3.transData.inverted().transform([[0, 0], [bbox.width, 0]])
        lab.set_position((x, offset + (invb[1][0] - invb[0][0]) + .0175))
        lab.set_transform(ax3.get_xaxis_transform())
        lab.set_rotation(rotation)
    ax3.fill_between(theta, arrCnts, alpha=0.075, color='#4e94ff')
    ax3.fill_between(theta, len(theta) * [0.55], alpha=1, color='w')
    circle = plt.Circle((0.0, 0.0), 0.1, transform=ax3.transData._b, color="k", alpha=0.3)
    ax3.add_artist(circle)
    ax3.plot((0, theta[0]), (0, arrCnts[0]),
             color='k', linewidth=1, alpha=0.5, linestyle='--')
    ax3.plot((0, theta[-1]), (0, arrCnts[-1]),
             color='k', linewidth=1, alpha=0.5, linestyle='--')

    formatter = tkr.ScalarFormatter(useMathText=True)
    formatter.set_scientific(False)
    cmap = plt.get_cmap('RdBu_r')
    cmap = truncate_colormap(cmap, 0.0, 1)
    df2_words_mat = df2_words_mat.replace(0, 0.00001)
    ax_df2 = sns.heatmap(df2_words_mat.astype(float),
                         norm=LogNorm(1 + df2_words_mat.astype(float).min().min(),
                                      df2_words_mat.astype(float).max().max()),
                         cbar_kws={'ticks': [100, 200, 400, 1000, 2500],
                                   "shrink": 1, 'use_gridspec': True,
                                   "format": formatter},
                         mask=df2_mask,
                         cmap=cmap,
                         linewidths=.25,
                         vmin=0.0000, vmax=2500,
                         ax=ax4)
    ax_df2.collections[0].colorbar.ax.yaxis.set_ticks_position('left')
    ax_df2.collections[0].colorbar.outline.set_edgecolor('k')
    ax_df2.collections[0].colorbar.outline.set_linewidth(1)
    for _, spine in ax1.spines.items():
        spine.set_visible(True)
    for _, spine in ax4.spines.items():
        spine.set_visible(True)
    sns.despine(ax=ax1)
    sns.despine(ax=ax4)

    plt.savefig(os.path.join(figure_path, 'bigrams_unigrams_Panels_CD' + '.pdf'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'bigrams_unigrams_Panels_CD' + '.png'),
                bbox_inches='tight', dpi=400,
                facecolor='white', transparent=False)


def groupby_plotter(grp, figure_path, filename):
    """ Plot the groupedby aggregate data"""
    mpl.rcParams['font.family'] = 'Arial'
    csfont = {'fontname': 'Arial'}

    colors = [(0 / 255, 28 / 255, 84 / 255, 0.5), (232 / 255, 152 / 255, 24 / 255, 0.5)]
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 7), sharey=True)
    ax1.scatter(y=grp[(grp['Main panel'] == 'A') | (grp['Main panel'] == 'B')]['Number ICS'],
                x=grp[(grp['Main panel'] == 'A') | (grp['Main panel'] == 'B')]['FTE'],
                color=colors[0], s=140, edgecolor=(0, 0, 0, 1), linewidth=1)
    ax1.scatter(y=grp[(grp['Main panel'] == 'C') | (grp['Main panel'] == 'D')]['Number ICS'],
                x=grp[(grp['Main panel'] == 'C') | (grp['Main panel'] == 'D')]['FTE'],
                color=colors[1], s=140, edgecolor=(0, 0, 0, 1), linewidth=1)

    ax2.scatter(y=grp[(grp['Main panel'] == 'A') | (grp['Main panel'] == 'B')]['Number ICS'],
                x=grp[(grp['Main panel'] == 'A') | (grp['Main panel'] == 'B')]['Total Income (£bn)'],
                color=colors[0], s=140, edgecolor=(0, 0, 0, 1), linewidth=1)
    ax2.scatter(y=grp[(grp['Main panel'] == 'C') | (grp['Main panel'] == 'D')]['Number ICS'],
                x=grp[(grp['Main panel'] == 'C') | (grp['Main panel'] == 'D')]['Total Income (£bn)'],
                color=colors[1], s=140, edgecolor=(0, 0, 0, 1), linewidth=1)

    ax3.scatter(y=grp[(grp['Main panel'] == 'A') | (grp['Main panel'] == 'B')]['Number ICS'],
                x=grp[(grp['Main panel'] == 'A') | (grp['Main panel'] == 'B')]['Doctoral Degrees'],
                color=colors[0], s=140, edgecolor=(0, 0, 0, 1), linewidth=1)
    ax3.scatter(y=grp[(grp['Main panel'] == 'C') | (grp['Main panel'] == 'D')]['Number ICS'],
                x=grp[(grp['Main panel'] == 'C') | (grp['Main panel'] == 'D')]['Doctoral Degrees'],
                color=colors[1], s=140, edgecolor=(0, 0, 0, 1), linewidth=1)

    legend_elements1 = [Line2D([], [], marker='o',
                               markerfacecolor=colors[0], markeredgecolor='k',
                               label=r'A & B', linewidth=0, markersize=10),
                        Line2D([], [], marker='o',
                               markerfacecolor=colors[1], markeredgecolor='k',
                               label=r'C & D', linewidth=0, markersize=10)]

    for ax, title in zip([ax1, ax2, ax3], ['A.', 'B.', 'C.']):
        ax.yaxis.grid(linestyle='--', alpha=0.3)
        ax.xaxis.grid(linestyle='--', alpha=0.3)
        ax.set_title(title, loc='left', fontsize=18)
        ax.tick_params(axis='both', which='major', labelsize=13)
    ax3.legend(handles=legend_elements1, loc='lower right', frameon=True,
               fontsize=14, framealpha=1, facecolor='w',
               edgecolor=(0, 0, 0, 1),
               title='Main Panel', title_fontsize=14)

    ax1.set_ylabel('Number of ICS Submitted', fontsize=14)
    ax1.set_xlabel('Full Time Employed', fontsize=14)
    ax2.set_xlabel('Total Income (£bn)', fontsize=14)
    xlabels = ['£{:,.1f}'.format(x) + 'bn' for x in ax2.get_xticks()]
    ax2.set_xticklabels(xlabels)

    ax3.set_xlabel('Doctoral Degrees Conferred', fontsize=14)
    ax1.set_xlim(0, )
    ax3.set_xlim(0, )
    ax2.xaxis.set_major_locator(plt.MaxNLocator(4))
    bbox = dict(boxstyle="round", fc="1.")
    arrowprops = dict(
        linewidth=1.1,
        arrowstyle="->",
        connectionstyle="angle, angleA = 0, angleB = 90,\
        rad = 0")

    offset = 72
    ax1.annotate('Business & Management Studies:\n# ICS: %.0f, FTE: %.0f,\nIncome: £%.2fbn, %.0f Doctorates.' % (
    504, 6633.52, 0.52, 9199.56),
                 (6633.52, 495), xytext=(- 190, -50),
                 textcoords='offset points',
                 bbox=bbox, arrowprops=arrowprops)

    ax2.annotate(
        'Clinical Medicine:\n# ICS: %.0f, FTE: %.0f,\nIncome: £%.2fbn,\n%.0f Doctorates.' % (254, 4878.50, 9.88, 12174),
        (9.88, 248), xytext=(- 135, -160),
        textcoords='offset points',
        bbox=bbox, arrowprops=arrowprops)

    ax3.annotate(
        'Engineering:\n# ICS: %.0f, FTE: %.0f,\nIncome: £%.2fbn,\n%.0f Doctorates.' % (391, 7252.89, 6.97, 23725.02),
        (23725.02, 396), xytext=(-120, 40),
        textcoords='offset points',
        bbox=bbox, arrowprops=arrowprops)

    sns.despine()
    plt.tight_layout()
    plt.savefig(os.path.join(figure_path, filename + '.pdf'), bbox_inches = 'tight')
    plt.savefig(os.path.join(figure_path, filename + '.png'), bbox_inches = 'tight', dpi=800)


def heatmap(x, y, figsize, figure_path, filename, **kwargs):
    # credit: kaggle.com/code/drazen/heatmap-with-sized-markers/notebook
    plt.figure(figsize=figsize)
    if 'color' in kwargs:
        color = kwargs['color']
    else:
        color = [1]*len(x)
    if 'palette' in kwargs:
        palette = kwargs['palette']
        n_colors = len(palette)
    else:
        n_colors = 256
        palette = sns.color_palette("Blues", n_colors)
    if 'color_range' in kwargs:
        color_min, color_max = kwargs['color_range']
    else:
        color_min, color_max = min(color), max(color)
    def value_to_color(val):
        if color_min == color_max:
            return palette[-1]
        else:
            val_position = float((val - color_min)) / (color_max - color_min)
            val_position = min(max(val_position, 0), 1)
            ind = int(val_position * (n_colors - 1))
            return palette[ind]
    if 'size' in kwargs:
        size = kwargs['size']
    else:
        size = [1]*len(x)
    if 'size_range' in kwargs:
        size_min, size_max = kwargs['size_range'][0], kwargs['size_range'][1]
    else:
        size_min, size_max = min(size), max(size)
    size_scale = kwargs.get('size_scale', 500)
    def value_to_size(val):
        if size_min == size_max:
            return 1 * size_scale
        else:
            val_position = (val - size_min) * 0.99 / (size_max - size_min) + 0.01
            val_position = min(max(val_position, 0), 1)
            return val_position * size_scale
    if 'x_order' in kwargs:
        x_names = [t for t in kwargs['x_order']]
    else:
        x_names = [t for t in sorted(set([v for v in x]))]
    x_to_num = {p[1]:p[0] for p in enumerate(x_names)}

    if 'y_order' in kwargs:
        y_names = [t for t in kwargs['y_order']]
    else:
        y_names = [t for t in sorted(set([v for v in y]))]
    y_to_num = {p[1]:p[0] for p in enumerate(y_names)}
    plot_grid = plt.GridSpec(1, 15, hspace=0.2, wspace=0.1)
    print(figsize)
    ax = plt.subplot(plot_grid[:,:-1])
    marker = kwargs.get('marker', 's')
    kwargs_pass_on = {k:v for k,v in kwargs.items() if k not in [
         'color', 'palette', 'color_range', 'size',
         'size_range', 'size_scale', 'marker', 'x_order', 'y_order'
    ]}
    [x_to_num[v] for v in x]
    ax.scatter(
        x=[x_to_num[v] for v in x],
        y=[y_to_num[v] for v in y],
        marker=marker,
        s=[value_to_size(v*5) for v in size],
        c=[value_to_color(v) for v in color],
        edgecolor='k',
        **kwargs_pass_on)
    ax.set_xticks([v for k,v in x_to_num.items()])
    ax.set_xticklabels([k for k in x_to_num], rotation=45, horizontalalignment='right', fontsize=14)
    ax.set_yticks([v for k,v in y_to_num.items()])
    ax.set_yticklabels([k for k in y_to_num], fontsize=14)
    ax.grid(False, 'major')
    ax.grid(True, 'minor')
    ax.set_xticks([t + 0.5 for t in ax.get_xticks()], minor=True)
    ax.set_yticks([t + 0.5 for t in ax.get_yticks()], minor=True)
    ax.set_xlim([-0.5, max([v for v in x_to_num.values()]) + 0.5])
    ax.set_ylim([-0.5, max([v for v in y_to_num.values()]) + 0.5])
    ax.set_facecolor('white')
    ax.set_title('A.', loc ='left', fontsize=18)
    if color_min < color_max:
        ax = plt.subplot(plot_grid[:,-1])
        col_x = [0]*len(palette)
        bar_y=np.linspace(color_min, color_max, n_colors)
        bar_height = bar_y[1] - bar_y[0]
        ax.barh(
            y=bar_y,
            width=[5]*len(palette),
            left=col_x,
            height=bar_height,
            color=palette,
            linewidth=5
        )
        ax.set_xlim(1, 2)
        ax.grid(False)
        ax.set_facecolor('white')
        sns.despine(ax=ax, left=True, bottom=True)
        ax.set_xticks([])
        ax.set_yticks(np.linspace(min(bar_y), max(bar_y), 5))
        ax.yaxis.tick_right()
        ax.tick_params(axis='y', which='major', labelsize=13)
    plt.savefig(os.path.join(figure_path, filename + '.pdf'), bbox_inches = 'tight')
    plt.savefig(os.path.join(figure_path, filename + '.png'), bbox_inches = 'tight',
                dpi=400, facecolor='white', transparent=False)


def make_hist_by_panel(dfe, figure_path, file_name, variable, sum_stats):
    # This needs optimising/writing properly.
    dfeA = dfe[dfe['Main panel'] == 'A']
    dfeB = dfe[dfe['Main panel'] == 'B']
    dfeC = dfe[dfe['Main panel'] == 'C']
    dfeD = dfe[dfe['Main panel'] == 'D']
    fig = plt.figure(figsize=(12, 7.5))
    gs = gridspec.GridSpec(2, 2)
    mpl.rcParams['font.family'] = 'Helvetica'
    colors5 = ['#001c54', '#81216a', '#d63f53', '#f68f1d', '#d2e818']
    colors4 = ['#001c54', '#a22367', '#f27233', '#d2e818']

    ax1 = fig.add_subplot(gs[0:2, 0:1])
    ax2 = fig.add_subplot(gs[0:1, 1:2])
    ax3 = fig.add_subplot(gs[1:2, 1:2])

    for dataframe, color in zip([dfeA, dfeB, dfeC, dfeD], [0, 1, 2, 3]):
        sns.kdeplot(dataframe[variable + '_score'], ax=ax1,
                    common_norm=True,
                    color=colors5[color],
                    common_grid=True,
                    cut=0)
    for score in [0, 1, 2, 3, 4]:
        sns.kdeplot(dfeC['s' + str(score + 1) + '_' + variable + '_score'], ax=ax2,
                    common_norm=True, color=colors5[score],
                    common_grid=True, cut=0)
        sns.kdeplot(dfeD['s' + str(score + 1) + '_' + variable + '_score'], ax=ax3,
                    common_norm=True, color=colors5[score],
                    common_grid=True, cut=0)

    ax1.yaxis.grid(linestyle='--', alpha=0.3)
    ax1.xaxis.grid(linestyle='--', alpha=0.3)
    ax2.yaxis.grid(linestyle='--', alpha=0.3)
    ax2.xaxis.grid(linestyle='--', alpha=0.3)
    ax3.yaxis.grid(linestyle='--', alpha=0.3)
    ax3.xaxis.grid(linestyle='--', alpha=0.3)
    ax1.set_title('A.', loc='left', fontsize=18)
    ax1.tick_params(axis='both', which='major', labelsize=13)
    ax2.set_title('B.', loc='left', fontsize=18)
    ax2.tick_params(axis='both', which='major', labelsize=13)
    ax3.set_title('C.', loc='left', fontsize=18)
    ax1.tick_params(axis='both', which='major', labelsize=13)
    ax1.set_ylabel('Normalised Density', fontsize=14)
    ax2.set_ylabel('Normalised Density', fontsize=14)
    ax3.set_ylabel('Normalised Density', fontsize=14)
    ax1.set_xlabel('Combined ' + str.title(variable) + ' Score', fontsize=14)
    ax2.set_xlabel('', fontsize=14)
    ax3.set_xlabel(str.title(variable) + ' Scores (S1-S5)', fontsize=14)
    ax2.yaxis.set_label_position("right")
    ax3.yaxis.set_label_position("right")
    ax2.set_xticklabels([])
    ax2.yaxis.tick_right()
    ax3.yaxis.tick_right()

    legend_elements1 = [Line2D([0], [0], marker=None,
                               label=r'Panel: A', linewidth=1,
                               color=colors4[0]),
                        Line2D([0], [0], marker=None,
                               label=r'Panel: B', linewidth=1,
                               color=colors4[1]),
                        Line2D([0], [0], marker=None,
                               label=r'Panel: C', linewidth=1,
                               color=colors4[2]),
                        Line2D([0], [0], marker=None,
                               label=r'Panel: D', linewidth=1,
                               color=colors4[3])
                        ]

    legend_elements2 = [Line2D([0], [0], marker=None,
                               label=r'Section: 1', linewidth=1,
                               color=colors5[0]),
                        Line2D([0], [0], marker=None,
                               label=r'Section: 2', linewidth=1,
                               color=colors5[1]),
                        Line2D([0], [0], marker=None,
                               label=r'Section: 3', linewidth=1,
                               color=colors5[2]),
                        Line2D([0], [0], marker=None,
                               label=r'Section: 4', linewidth=1,
                               color=colors5[3]),
                        Line2D([0], [0], marker=None,
                               label=r'Section: 5', linewidth=1,
                               color=colors5[4])]

    if variable == 'sentiment':
        legend_loc = 'upper left'
    elif variable == 'flesch':
        legend_loc = 'upper left'

    ax1.legend(handles=legend_elements1, loc=legend_loc, frameon=True,
               fontsize=14, framealpha=1, facecolor='w',
               edgecolor=(0, 0, 0, 1)
               # title='Main Panel', title_fontsize=14
               )
    ax2.legend(handles=legend_elements2, loc=legend_loc, frameon=True,
               fontsize=11, framealpha=1, facecolor='w',
               edgecolor=(0, 0, 0, 1),
               title='Panel: C', title_fontsize=11
               )
    ax3.legend(handles=legend_elements2, loc=legend_loc, frameon=True,
               fontsize=11, framealpha=1, facecolor='w',
               edgecolor=(0, 0, 0, 1),
               title='Panel: D', title_fontsize=11
               )
    ax2.xaxis.set_ticklabels([])
    ax1.tick_params(axis='both', which='major', labelsize=13)
    ax2.tick_params(axis='both', which='major', labelsize=13)
    ax3.tick_params(axis='both', which='major', labelsize=13)

    if sum_stats is True:
        textstr1 = '\n'.join((
            r'Panel A: $\mu$=%.2f, $\sigma$=%.2f' % (np.around(dfeA[variable + '_score'].mean(),
                                                               decimals=2),
                                                     np.around(dfeA[variable + '_score'].std(),
                                                               decimals=2)),
            r'Panel B: $\mu$=%.2f, $\sigma$=%.2f' % (np.around(dfeB[variable + '_score'].mean(),
                                                               decimals=2),
                                                     np.around(dfeB[variable + '_score'].std(),
                                                               decimals=2)),
            r'Panel C: $\mu$=%.2f, $\sigma$=%.2f' % (np.around(dfeC[variable + '_score'].mean(),
                                                               decimals=2),
                                                     np.around(dfeC[variable + '_score'].std(),
                                                               decimals=2)),
            r'Panel D: $\mu$=%.2f, $\sigma$=%.2f' % (np.around(dfeD[variable + '_score'].mean(),
                                                               decimals=2),
                                                     np.around(dfeD[variable + '_score'].std(),
                                                               decimals=2))))

        textstr2 = '\n'.join((
            r'Section 1: $\mu$=%.2f, $\sigma$=%.2f' % (np.around(dfeC['s1_' + variable + '_score'].mean(),
                                                                 decimals=2),
                                                       np.around(dfeC['s1_' + variable + '_score'].std(),
                                                                 decimals=2)),
            r'Section 2: $\mu$=%.2f, $\sigma$=%.2f' % (np.around(dfeC['s2_' + variable + '_score'].mean(),
                                                                 decimals=2),
                                                       np.around(dfeC['s2_' + variable + '_score'].std(),
                                                                 decimals=2)),
            r'Section 3: $\mu$=%.2f, $\sigma$=%.2f' % (np.around(dfeC['s3_' + variable + '_score'].mean(),
                                                                 decimals=2),
                                                       np.around(dfeC['s3_' + variable + '_score'].std(),
                                                                 decimals=2)),
            r'Section 4: $\mu$=%.2f, $\sigma$=%.2f' % (np.around(dfeC['s4_' + variable + '_score'].mean(),
                                                                 decimals=2),
                                                       np.around(dfeC['s4_' + variable + '_score'].std(),
                                                                 decimals=2)),
            r'Section 5: $\mu$=%.2f, $\sigma$=%.2f' % (np.around(dfeC['s5_' + variable + '_score'].mean(),
                                                                 decimals=2),
                                                       np.around(dfeC['s5_' + variable + '_score'].std(),
                                                                 decimals=2))))

        textstr3 = '\n'.join((
            r'Section 1: $\mu$=%.2f, $\sigma$=%.2f' % (np.around(dfeD['s1_' + variable + '_score'].mean(),
                                                                 decimals=2),
                                                       np.around(dfeD['s1_' + variable + '_score'].std(),
                                                                 decimals=2)),
            r'Section 2: $\mu$=%.2f, $\sigma$=%.2f' % (np.around(dfeD['s2_' + variable + '_score'].mean(),
                                                                 decimals=2),
                                                       np.around(dfeD['s2_' + variable + '_score'].std(),
                                                                 decimals=2)),
            r'Section 3: $\mu$=%.2f, $\sigma$=%.2f' % (np.around(dfeD['s3_' + variable + '_score'].mean(),
                                                                 decimals=2),
                                                       np.around(dfeD['s3_' + variable + '_score'].std(),
                                                                 decimals=2)),
            r'Section 4: $\mu$=%.2f, $\sigma$=%.2f' % (np.around(dfeD['s4_' + variable + '_score'].mean(),
                                                                 decimals=2),
                                                       np.around(dfeD['s4_' + variable + '_score'].std(),
                                                                 decimals=2)),
            r'Section 5: $\mu$=%.2f, $\sigma$=%.2f' % (np.around(dfeD['s5_' + variable + '_score'].mean(),
                                                                 decimals=2),
                                                       np.around(dfeD['s5_' + variable + '_score'].std(),
                                                                 decimals=2))))
        props = dict(boxstyle='round', facecolor='white', edgecolor='k', alpha=1)

        # place a text box in upper left in axes coords
        ax1.text(0.05, 0.19, textstr1, transform=ax1.transAxes, fontsize=12,
                 verticalalignment='top', bbox=props)
        ax2.text(0.05, 0.385, textstr2, transform=ax2.transAxes, fontsize=10,
                 verticalalignment='top', bbox=props)
        ax3.text(0.05, 0.385, textstr3, transform=ax3.transAxes, fontsize=10,
                 verticalalignment='top', bbox=props)

    sns.despine(ax=ax1)
    sns.despine(ax=ax2, left=True, right=False)
    sns.despine(ax=ax3, left=True, right=False)

    plt.tight_layout()
    plt.savefig(os.path.join(figure_path, file_name + '.pdf'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, file_name + '.png'),
                bbox_inches='tight', dpi=400,
                facecolor='white', transparent=False)



def find_keywords(df, keyword_dict):
    keyword_count = {}
    for key, value in keyword_dict.items():
        keyword_count[key] = len(df[df.apply(lambda r: any([kw in r[0] for kw in value]),
                                             axis=1)])
    return keyword_count


def make_keyword_figure():
    merged_path = os.path.join(os.getcwd(), '..', '..', 'data', 'merged')
    keyword_out = os.path.join(os.getcwd(), '..', '..', 'data', 'keywords')
    asset_path = os.path.join(os.getcwd(), '..', '..', 'assets')
    figure_path = os.path.join(os.path.join(os.getcwd(), '..', '..', 'figures'))
    df = pd.read_csv(os.path.join(merged_path, 'merged_ref_data_exc_output.csv'), index_col=0)
    with open(os.path.join(asset_path, 'keyword_dictionary.json')) as json_file:
        keyword_dict = json.load(json_file)
    fourstar_mask =  ((df['3*_Impact'] == '0.0') &
                      (df['2*_Impact']=='0.0') &
                      (df['1*_Impact'] == '0.0') &
                      (df['Unclassified_Impact']=='0.0'))
    freetext = ['1. Summary of the impact',
                '2. Underpinning research',
                '3. References to the research',
                '4. Details of the impact',
                '5. Sources to corroborate the impact']
    df_text = df[freetext].apply(lambda x: x.astype(str).str.lower())
    keyword_counter = {}
    keyword_counter['all_studies'] = find_keywords(df_text, keyword_dict)
    keyword_counter['by_panels'] = {}
    for panel in df['Main panel'].unique():
        temp_df = df[df['Main panel'] == panel]
        temp_df = temp_df[freetext].apply(lambda x: x.astype(str).str.lower())
        keyword_counter['by_panels'][panel] = find_keywords(temp_df, keyword_dict)
    shape_mask = ((df['Main panel'] == 'D') |
                 (df['Main panel'] == 'C') |
                 (df['Unit of assessment number'] == '4.0'))
    shape = df[shape_mask][freetext].apply(lambda x: x.astype(str).str.lower())
    non_shape = df[~shape_mask][freetext].apply(lambda x: x.astype(str).str.lower())
    keyword_counter['all_grades'] = {}
    keyword_counter['all_grades']['SHAPE'] = find_keywords(shape, keyword_dict)
    keyword_counter['all_grades']['Non-SHAPE'] = find_keywords(non_shape, keyword_dict)
    keyword_counter['four_star'] = {}
    fourstar = df[fourstar_mask]
    shape_fourstar = fourstar[shape_mask][freetext].apply(lambda x: x.astype(str).str.lower())
    non_shape_fourstar = fourstar[~shape_mask][freetext].apply(lambda x: x.astype(str).str.lower())
    keyword_counter['four_star']['SHAPE'] = find_keywords(shape_fourstar, keyword_dict)
    keyword_counter['four_star']['Non-SHAPE'] = find_keywords(non_shape_fourstar, keyword_dict)

    fig = plt.figure(figsize=(15, 8))
    gs = gridspec.GridSpec(2, 2)
    mpl.rcParams['font.family'] = 'Arial'
    colors5 = ['#001c54', '#732268', '#c2365b', '#ed7239', '#e8be18']
    colors4 = ['#001c54', '#902467', '#e35b46', '#e8be18']
    colors2 = [colors4[0], colors4[3]]
    ax1 = fig.add_subplot(gs[0:2, 0:1])
    ax2 = fig.add_subplot(gs[0:1, 1:2])
    ax3 = fig.add_subplot(gs[1:2, 1:2])
    sorted_dict = {key: value for key, value in sorted(keyword_counter['by_panels'].items())}
    df1 = pd.DataFrame.from_dict(sorted_dict)
    ax1 = df1.plot(ax=ax1, kind='barh', edgecolor='k', color=colors4, alpha=0.8)
    df2 = pd.DataFrame.from_dict(keyword_counter['four_star'])
    ax2 = df2.plot(ax=ax2, kind='bar', edgecolor='k', color = colors2, alpha=0.8)
    df3 = pd.DataFrame.from_dict(keyword_counter['all_grades'])
    ax3 = df3.plot(ax=ax3, kind='bar', edgecolor='k', color = colors2, legend=False, alpha=0.8)
    ax3.set_xticks(ax3.get_xticks())
    ax3.set_xticklabels(ax3.get_xticklabels(), rotation=0)


    ax1.set_title('A.', loc='left', fontsize=18)
    ax1.tick_params(axis='both', which='major', labelsize=14)
    ax2.set_title('B.', loc='left', fontsize=18)
    ax2.tick_params(axis='both', which='major', labelsize=11)
    ax3.set_title('C.', loc='left', fontsize=18)
    ax3.tick_params(axis='both', which='major', labelsize=11)
    ax2.set_xticklabels([])

    ax1.set_xlabel('Number of ICS (All Grades)', fontsize=14)
    ax2.set_ylabel('Number of ICS (Certified 4*)', fontsize=14)
    ax3.set_ylabel('Number of ICS (All Grades)', fontsize=14)

#    ax2.yaxis.tick_right()
#    ax3.yaxis.tick_right()
    ax2.yaxis.set_label_position("right")
    ax3.yaxis.set_label_position("right")
#    ax2.yaxis.set_ticks_position('right')
#    ax3.yaxis.set_ticks_position('right')

    ax1.legend(frameon=True,
               fontsize=12, framealpha=1, facecolor='w',
               edgecolor=(0, 0, 0, 1),
               title='Panels', title_fontsize=14)
    ax2.legend(frameon=True,
               fontsize=12, framealpha=1, facecolor='w',
               edgecolor=(0, 0, 0, 1),
               #title='Panels', title_fontsize=14
              )
    ax1.set_axisbelow(True)
    ax2.set_axisbelow(True)
    ax3.set_axisbelow(True)
    ax1.xaxis.grid(linestyle='--', alpha=0.4)
    ax1.yaxis.grid(linestyle='--', alpha=0.4)
    ax2.xaxis.grid(linestyle='--', alpha=0.4)
    ax2.yaxis.grid(linestyle='--', alpha=0.4)
    ax3.xaxis.grid(linestyle='--', alpha=0.4)
    ax3.yaxis.grid(linestyle='--', alpha=0.4)
    sns.despine(ax=ax1, top=False)
    sns.despine(ax=ax2, left = True, right=False, top=False)
    sns.despine(ax=ax3, left = True, right=False)
    plt.tight_layout()
    plt.savefig(os.path.join(figure_path, 'keyword_analysis.pdf'), bbox_inches = 'tight')
    plt.savefig(os.path.join(figure_path, 'keyword_analysis.png'), bbox_inches = 'tight', dpi=800)


def make_gpa_vs_environment(figure_path, df):
    subset = ['Institution name', 'Unit of assessment number']
    scored = df.drop_duplicates(subset = subset)
    counter = pd.Series(df.groupby(subset).size(),
                        name='size').reset_index()
    scored['ICS_GPA'] = (pd.to_numeric(scored['4*_Impact'], errors='coerce')*4 +
                         pd.to_numeric(scored['3*_Impact'], errors='coerce')*3 +
                         pd.to_numeric(scored['2*_Impact'], errors='coerce')*2 +
                         pd.to_numeric(scored['1*_Impact'], errors='coerce')*1)/100
    scored = pd.merge(scored, counter, left_on = subset, right_on = subset)
    shape_mask = ((scored['Main panel'] == 'C') |
                  (scored['Main panel'] == 'D') |
                  (scored['Unit of assessment number'] == '4'))
    print("Corr(GPA,  FTE) for all ICS is: ",
          round(scored['ICS_GPA'].corr(df['fte']), 3))
    print("Corr(GPA,  FTE) for Non-SHAPE is: ",
          round(scored[~shape_mask]['ICS_GPA'].corr(df['fte']), 3))
    print("Corr(GPA,  FTE) for SHAPE is: ",
          round(scored[shape_mask]['ICS_GPA'].corr(df['fte']), 3))
    print("Corr(GPA, Total Income) for all ICS is: ",
          round(scored['ICS_GPA'].corr(df['tot_income']), 3))
    print("Corr(GPA, Total Income) for Non-SHAPE is: ",
          round(scored[~shape_mask]['ICS_GPA'].corr(df['tot_income']), 3))
    print("Corr(GPA, Total Income) for SHAPE is: ",
          round(scored[shape_mask]['ICS_GPA'].corr(df['tot_income']), 3))
    print("Corr(GPA, Number Degrees) for all ICS is: ",
          round(scored['ICS_GPA'].corr(df['num_doc_degrees_total']), 3))
    print('Mean GPA is ',
          round(scored['ICS_GPA'].mean(), 2))
    print('Mean GPA for Non-SHAPE is ',
          round(scored[~shape_mask]['ICS_GPA'].mean(), 3))
    print('Mean GPA for SHAPE is ',
          round(scored[shape_mask]['ICS_GPA'].mean(), 3))
    print('Mean GPA for Non-SHAPE (FTE>=100) is ',
          round(scored[~shape_mask & (scored['fte']>=100)]['ICS_GPA'].mean(), 3))
    print('Mean GPA for SHAPE (FTE>=100) is ',
          round(scored[shape_mask & (scored['fte']>=100)]['ICS_GPA'].mean(), 3))
    print('Mean GPA for Non-SHAPE (50<=FTE) is ',
          round(scored[~shape_mask & (scored['fte']<=50)]['ICS_GPA'].mean(), 3))
    print('Mean GPA for SHAPE (50<FTE) is ',
          round(scored[shape_mask & (scored['fte']<=50)]['ICS_GPA'].mean(), 3))
    print('Mean GPA for Non-SHAPE (1 ICS submitted) is ',
          round(scored[~shape_mask & (scored['size']==1)]['ICS_GPA'].mean(), 3))
    print('Mean GPA for SHAPE (1 ICS submitted) is ',
          round(scored[shape_mask & (scored['size']==1)]['ICS_GPA'].mean(), 3))
    print('Mean GPA for Non-SHAPE (>1 ICS submitted) is ',
          round(scored[~shape_mask & (scored['size']>1)]['ICS_GPA'].mean(), 3))
    print('Mean GPA for SHAPE (>1 ICS submitted) is ',
          round(scored[shape_mask & (scored['size']>1)]['ICS_GPA'].mean(), 3))
    scored = df.drop_duplicates(subset = subset)
    scored['ICS_GPA'] = (pd.to_numeric(df['4*_Impact'], errors='coerce')*4 +
                         pd.to_numeric(df['3*_Impact'], errors='coerce')*3 +
                         pd.to_numeric(df['2*_Impact'], errors='coerce')*2 +
                         pd.to_numeric(df['1*_Impact'], errors='coerce')*1)/100
    scored = pd.merge(scored, counter, how='inner', left_on = subset, right_on = subset)
    size = 60
    colors = [(0 / 255, 28 / 255, 84 / 255, 1), (232 / 255, 152 / 255, 24 / 255, 1)]
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 5.5), sharey=True)
    ax1.scatter(y=scored[~shape_mask]['ICS_GPA'],
                x=scored[~shape_mask]['fte'],
                color=colors[0], s=size, edgecolor=(0, 0, 0, 1), linewidth=.5)
    ax1.scatter(y=scored[shape_mask]['ICS_GPA'],
                x=scored[shape_mask]['fte'],
                color=colors[1], s=size, edgecolor=(0, 0, 0, 1), linewidth=.5)
    ax2.scatter(y=scored[~shape_mask]['ICS_GPA'],
                x=scored[~shape_mask]['tot_income']/1000000000,
                color=colors[0], s=size, edgecolor=(0, 0, 0, 1), linewidth=.5)
    ax2.scatter(y=scored[shape_mask]['ICS_GPA'],
                x=scored[shape_mask]['tot_income']/1000000000,
                color=colors[1], s=size, edgecolor=(0, 0, 0, 1), linewidth=.5)
    ax3.scatter(y=scored[~shape_mask]['ICS_GPA'],
                x=scored[~shape_mask]['num_doc_degrees_total'],
                color=colors[0], s=size, edgecolor=(0, 0, 0, 1), linewidth=.5)
    ax3.scatter(y=scored[shape_mask]['ICS_GPA'],
                x=scored[shape_mask]['num_doc_degrees_total'],
                color=colors[1], s=size, edgecolor=(0, 0, 0, 1), linewidth=.5)
    legend_elements1 = [Line2D([], [], marker='o',
                               markerfacecolor=colors[0], markeredgecolor='k',
                               label=r'Non-SHAPE', linewidth=0, markersize=10),
                        Line2D([], [], marker='o',
                               markerfacecolor=colors[1], markeredgecolor='k',
                               label=r'SHAPE', linewidth=0, markersize=10)]
    for ax, title in zip([ax1, ax2, ax3], ['A.', 'B.', 'C.']):
        ax.yaxis.grid(linestyle='--', alpha=0.3)
        ax.xaxis.grid(linestyle='--', alpha=0.3)
        ax.set_title(title, loc='left', fontsize=20)
        ax.tick_params(axis='both', which='major', labelsize=14)
    ax3.legend(handles=legend_elements1, loc='lower right', frameon=True,
               fontsize=14, framealpha=1, facecolor='w',
               edgecolor=(0, 0, 0, 1),
               title='Subject Area', title_fontsize=14)
    ax1.set_ylabel('Departmental GPA', fontsize=14)
    ax1.set_xlabel('Full Time Employed', fontsize=14)
    ax2.set_xlabel('Total Income (£bn)', fontsize=14)
    ax3.set_xlabel('Doctoral Degrees Conferred', fontsize=14)
    ax1.yaxis.set_major_locator(plt.MaxNLocator(5))
    xlabels = ['£{:,.1f}'.format(x) + 'bn' for x in ax2.get_xticks()]
    ax2.set_xticklabels(xlabels)
    plt.tight_layout()
    sns.despine()
    filename = 'gpa_vs_environment'
    plt.savefig(os.path.join(figure_path, filename + '.pdf'), bbox_inches = 'tight')
    plt.savefig(os.path.join(figure_path, filename + '.png'), bbox_inches = 'tight', dpi=800)


def make_simple_scores_figure(df, figure_path, out_path):
    fig = plt.figure(figsize=(12, 8))
    gs = gridspec.GridSpec(2, 2)
    mpl.rcParams['font.family'] = 'Helvetica'
    colors5_blue = ['#3a5e8cFF', '#10a53dFF',
                    '#541352FF', '#ffcf20FF', '#2f9aa0FF']
    df['4*_Impact'] = pd.to_numeric(df['4*_Impact'],
                                    errors='coerce')
    df['3*_Impact'] = pd.to_numeric(df['3*_Impact'],
                                    errors='coerce')
    df['2*_Impact'] = pd.to_numeric(df['2*_Impact'],
                                    errors='coerce')
    df['1*_Impact'] = pd.to_numeric(df['1*_Impact'],
                                    errors='coerce')
    df['ICS_GPA'] = (df['4*_Impact']*4 +
                     df['3*_Impact']*3 +
                     df['2*_Impact']*2 +
                     df['1*_Impact']*1)/100
    df = df[['Institution name',
             'Main panel', 'Unit of assessment number', 'ICS_GPA']]
    df = df.drop_duplicates(subset = ['Institution name',
                                      'Unit of assessment number'])
    shape_mask = ((df['Main panel'] == 'C') |
                  (df['Main panel'] == 'D') |
                  (df['Unit of assessment number'] == '4'))
    df_shape = df[shape_mask]
    df_nonshape = df[~shape_mask]
    df_panelc = df[df['Main panel'] == 'C']
    df_paneld = df[df['Main panel'] == 'D']
    print(f'Panel C ICS GPA mean: ',
          round(df_panelc['ICS_GPA'].mean(), 2))
    print(f'Panel D ICS GPA mean: ',
          round(df_paneld['ICS_GPA'].mean(),2 ))
    ax1 = fig.add_subplot(gs[0:2, 0:1])
    ax2 = fig.add_subplot(gs[0:1, 1:2])
    ax3 = fig.add_subplot(gs[1:2, 1:2])
    colors = ['#001c54', '#E89818']
    nbins = 18
    letter_fontsize = 24
    label_fontsize = 18
    mpl.rcParams['font.family'] = 'Arial'
    csfont = {'fontname': 'Arial'}
    sns.kdeplot(df_shape['ICS_GPA'],
                ax=ax1, color= colors[1]
               )
    sns.kdeplot(df_nonshape['ICS_GPA'],
                ax=ax1, color= colors[0]
               )
    sns.distplot(df_panelc['ICS_GPA'],
                 hist_kws={'facecolor': colors[1],
                           'edgecolor': 'k',
                           'alpha': 0.7},
                 kde_kws={'color': colors[0]}, ax=ax2, bins=nbins)
    sns.distplot(df_paneld['ICS_GPA'],
                 hist_kws={'facecolor': colors[0],
                           'edgecolor': 'k',
                           'alpha': 0.7},
                 kde_kws={'color': colors[1]}, ax=ax3, bins=nbins)
    ax1.grid(which="both", linestyle='--', alpha=0.3)
    ax2.grid(which="both", linestyle='--', alpha=0.3)
    ax3.grid(which="both", linestyle='--', alpha=0.3)
    ax2.yaxis.set_label_position("right")
    ax3.yaxis.set_label_position("right")
    ax2.set_xticklabels([])
    ax2.yaxis.tick_right()
    ax3.yaxis.tick_right()
    sns.despine(ax=ax2, left=True, right=False, top=True, bottom=True)
    sns.despine(ax=ax3, left=True, right=False)
    sns.despine(ax=ax1, top =True)
    ax2.set_xlabel('')
    legend_elements1 = [Line2D([0], [0], marker=None,
                               label=r'SHAPE', linewidth=2,
                               color=colors[1]),
                        Line2D([0], [0], marker=None,
                               label=r'Non-SHAPE', linewidth=2,
                               color=colors[0])]
    legend_elements2 = [Patch(facecolor=colors[1], edgecolor='k',
                              label=r'Bins', alpha=0.7),
                        Line2D([0], [0], color=colors[0], lw=1, linestyle='-',
                               label=r'KDE', alpha=0.7)]
    legend_elements3 = [Patch(facecolor=colors[0], edgecolor='k',
                              label=r'Bins', alpha=0.7),
                        Line2D([0], [0], color=colors[1], lw=1, linestyle='-',
                               label=r'KDE', alpha=0.7)]
    ax1.legend(handles=legend_elements1,
               frameon=True,
               fontsize=15, framealpha=1, facecolor='w',
               edgecolor=(0, 0, 0, 1)
              )
    ax2.legend(handles=legend_elements2,
               frameon=True,
               fontsize=15, framealpha=1, facecolor='w',
               edgecolor=(0, 0, 0, 1),
               title='Panel C', title_fontsize=14)
    ax3.legend(handles=legend_elements3,
               frameon=True,
               fontsize=15, framealpha=1, facecolor='w',
               edgecolor=(0, 0, 0, 1),
               title='Panel D', title_fontsize=14)
    ax1.set_xlabel('ICS GPA', fontsize=label_fontsize)
    ax3.set_xlabel('ICS GPA', fontsize=label_fontsize)
    ax1.set_ylabel('Density', fontsize=label_fontsize)
    ax2.set_ylabel('Density', fontsize=label_fontsize)
    ax3.set_ylabel('Density', fontsize=label_fontsize)
    ax1.tick_params(axis='both', which='major', labelsize=14)
    ax2.tick_params(axis='both', which='major', labelsize=14)
    ax3.tick_params(axis='both', which='major', labelsize=14)
    ax1.set_title('A.', loc='left', fontsize=letter_fontsize, y=1.035)
    ax2.set_title('B.', loc='left', fontsize=letter_fontsize, y=1.035)
    ax3.set_title('C.', loc='left', fontsize=letter_fontsize, y=1.035)
    plt.tight_layout()
    plt.savefig(os.path.join(figure_path, 'ics_gpa.pdf'),
                bbox_inches='tight')
    df.to_csv(os.path.join(out_path, 'department_gpa.csv'), index=False)

