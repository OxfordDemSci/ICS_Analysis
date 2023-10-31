import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.colors
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
from matplotlib.colors import LogNorm
from helpers.figure_helpers import savefigures

figure_path = os.path.join(os.getcwd(), '..', '..', 'figures')
mpl.rcParams['font.family'] = 'Graphik'
sns.set(font='Graphik', style="ticks")
fig, ax1 = plt.subplots(figsize=(26, 14))


def make_heat_topics():
    ics_ref = pd.read_csv(os.path.join(os.getcwd(), '..', '..',
                                     'data', 'final', 'enhanced_ref_data.csv'))
    ics_ref = ics_ref[['REF impact case study identifier', 'Unit of assessment number']]
    df = pd.read_excel(os.path.join(os.getcwd(), '..', '..',
                                    'data', 'topic_model',
                                    'nn3_threshold0.01_reduced.xlsx')
                       )
    df = pd.merge(df, ics_ref, how='left',
                  left_on='REF impact case study identifier',
                  right_on='REF impact case study identifier')
    df['Unit of assessment number'] = df['Unit of assessment number'].astype(int)
    heat = pd.DataFrame(0,
                        index=df['Unit of assessment number'].unique(),
                        columns=list(range(0, 83)))
    for index in heat.index:
        uoa = df[df['Unit of assessment number'] == index]
        for row in uoa.index:
            for column in heat.columns:
                prob = uoa.at[row, column]
                heat.loc[index, column] = heat.at[index, column] + prob
    count = df.groupby(['Unit of assessment number'])['Unit of assessment number'].count()
    lookup = pd.read_csv(os.path.join(os.getcwd(), '..', '..',
                                      'data', 'manual', 'topic_lookup',
                                      'topic_lookup.csv'))



    topic_order = lookup.drop_duplicates().sort_values(ascending=True,
                                                       by='cluster_id')['topic_id'].to_list()
    topic_names = lookup.drop_duplicates().sort_values(ascending=True,
                                                       by='cluster_id')['topic_name_short'].to_list()
    heat = heat[topic_order]
    topic_names = [x.strip() for x in topic_names]
    return heat, count, topic_names


def make_brace(xmin, xmax, ax, text, multi):
    xspan = xmax - xmin
    ax_xmin, ax_xmax = ax1.get_xlim()
    xax_span = ax_xmax - ax_xmin
    ymin, ymax = ax1.get_ylim()
    ymax = ymax * multi
    yspan = ymax - ymin
    resolution = int(xspan / xax_span * 100) * 2 + 1  # guaranteed uneven
    beta = 300. / xax_span  # the higher this is, the smaller the radius
    x = np.linspace(xmin, xmax, resolution)
    x_half = x[:resolution // 2 + 1]
    y_half_brace = (1 / (1. + np.exp(-beta * (x_half - x_half[0])))
                    + 1 / (1. + np.exp(-beta * (x_half - x_half[-1]))))
    y = np.concatenate((y_half_brace, y_half_brace[-2::-1]))
    y = ymin + (.05 * y - .01) * yspan - 23
    ax1.plot(x, y, color='black', lw=1)
    ax1.text((xmax + xmin) / 2., ymin + 0.85 * yspan, text,
             ha='center', va='bottom', fontsize=24, rotation=90)


def rotate_point(x, y, angle_rad):
    cos, sin = np.cos(angle_rad), np.sin(angle_rad)
    return cos * x - sin * y, sin * x + cos * y


def draw_brace(ax, span, position, text, text_pos,
               brace_scale=1.0, beta_scale=300., rotate=False, rotate_text=False):
    '''
        all positions and sizes are in axes units
        span: size of the curl
        position: placement of the tip of the curl
        text: label to place somewhere
        text_pos: position for the label
        beta_scale: scaling for the curl, higher makes a smaller radius
        rotate: true rotates to place the curl vertically
        rotate_text: true rotates the text vertically
    '''
    ax_xmin, ax_xmax = ax.get_xlim()
    xax_span = ax_xmax - ax_xmin
    resolution = int(span / xax_span * 100) * 2 + 1
    beta = beta_scale / xax_span
    x = np.linspace(-span / 2., span / 2., resolution)
    x_half = x[:int(resolution / 2) + 1]
    y_half_brace = (1 / (1. + np.exp(-beta * (x_half - x_half[0])))
                    + 1 / (1. + np.exp(-beta * (x_half - x_half[-1]))))
    y = np.concatenate((y_half_brace, y_half_brace[-2::-1]))
    max_y = np.max(y)
    min_y = np.min(y)
    y /= (max_y - min_y)
    y *= brace_scale
    y -= max_y
    if rotate:
        x, y = rotate_point(x, y, np.pi / 2)
    x += position[0]
    y += position[1]
    ax.autoscale(False)
    ax.plot(x, y, color='black', lw=1, clip_on=False)
    ax.text(text_pos[0], text_pos[1], text,
            ha='center', va='bottom',
            rotation=90 if rotate_text else 0,
            fontsize=24)


def make_figure_two():
    print('\n*****************************************************')
    print('***************** Making Figure 2! ********************')
    print('*******************************************************')
    heat_topics, count, xaxis_labels = make_heat_topics()
    heat_topics = heat_topics.sort_index()
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("",
                                                               ['#FFB600',
                                                                'white',
                                                                '#00A9DF'
                                                                ]
                                                               )

    cmap = plt.get_cmap(cmap)
    formatter = tkr.ScalarFormatter(useMathText=True)
    formatter.set_scientific(False)
    sns.heatmap(heat_topics.div(count, axis=0),
                cmap=cmap,
                linewidths=.5,
                linecolor='w',
                ax=ax1,
                cbar=False
                )
    fig.colorbar(ax1.collections[0], ax=ax1,
                 location="right", use_gridspec=False, pad=0.0125,
                 shrink=0.765, anchor=(0, 0))
    sns.heatmap(heat_topics.div(count, axis=0),
                cmap=cmap,
                norm=LogNorm(),
                linewidths=.5,
                linecolor='w',
                ax=ax1,
                cbar=False
                )

    ax1.set_ylim(23, -7)
    ax1.set_xlabel('Topics', fontsize=16)
    cbar_ax = fig.axes[-1]
    cbar_ax.set_title('Average Weight', y=.375, x=3,
                      rotation=270, fontsize=20)
    cbar_solids = cbar_ax.collections[0]
    cbar_solids.set_edgecolor("k")
    cbar_solids.set_lw(1.0)
    cbar_ax.tick_params(axis='both', which='major', labelsize=16)
    xmin, xmax = (0, 9)
    make_brace(xmin, xmax, ax1, '1. Arts', 1)
    xmin, xmax = (10, 21)
    make_brace(xmin, xmax, ax1, '2. Heritage', 1)
    xmin, xmax = (22, 26)
    make_brace(xmin, xmax, ax1, '3. Education', 1)
    xmin, xmax = (27, 30)
    make_brace(xmin, xmax, ax1, '4. Economy', 1)
    xmin, xmax = (31, 33)
    make_brace(xmin, xmax, ax1, '5. Employment', 1)
    xmin, xmax = (34, 37)
    make_brace(xmin, xmax, ax1, '6. Crime', 1)
    xmin, xmax = (38, 44)
    make_brace(xmin, xmax, ax1, '7. Family', 1)
    xmin, xmax = (45, 58)
    make_brace(xmin, xmax, ax1, '8. Governance', 1)
    xmin, xmax = (59, 72)
    make_brace(xmin, xmax, ax1, '9. Health', 1)
    xmin, xmax = (73, 82)
    make_brace(xmin, xmax, ax1, '10. Environment', 1)
    draw_brace(ax1, 11, [-6, 7],
               '  Panel C', [-7, 8], rotate=True,
               rotate_text=True)
    draw_brace(ax1, 9, [-6, 18],
               '  Panel D', [-7, 18], rotate=True,
               rotate_text=True)
    ax1.tick_params(axis='both', which='major', labelsize=14)
    ax1.set_xlabel('')
    ax1.set_ylabel('Unit of Assessment', fontsize=18, y=.38)
    sns.despine(offset=5, trim=True, ax=ax1)
    ax1.set_xticklabels(xaxis_labels, rotation=90)
    filename = 'figure_2'
    savefigures(plt, figure_path, filename)