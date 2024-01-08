import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt


def make_figure_three():
    print('Making Figure 3!')
    df_ref = pd.read_csv(os.path.join(os.getcwd(),
                                      '..',
                                      '..',
                                      'data',
                                      'final',
                                      'enhanced_ref_data.csv'))
    ba_rgb2 = ['#41558c', '#E89818', '#CF202A']
    holder = pd.DataFrame(columns=['Prob'])
    step = 5
    upper = 100
    iterator = np.round(step / upper, 3)
    for x in range(0, upper, step):
        x = x / upper
        temp = df_ref[(df_ref['BERT_prob'] >= x) & (df_ref['BERT_prob'] < (x + iterator))]
        holder.at[str(x) + '-' + str(np.round(x + iterator, 3)),
                  'N'] = len(temp)
        try:
            holder.at[str(x) + '-' + str(np.round(x + iterator, 3)),
            'Prob'] = len(temp[temp['reassigned'] == 0]) / len(
                temp)
        except ZeroDivisionError:
            holder.at[x, 'Prob'] = np.nan

    reassigned = df_ref[df_ref['reassigned'] == 0]
    not_reassigned = df_ref[df_ref['reassigned'] == 1]
    print(len(reassigned) / (len(reassigned) + len(not_reassigned)))

    fig, (ax1, ax2) = plt.subplots(1, 2,
                                   figsize=(11, 5.5),
                                   constrained_layout=True)
    holder['N'].plot(kind='bar', edgecolor='k', ax=ax1,
                     color=ba_rgb2[0], legend=False, width=1)
    holder['Prob'].plot(kind='bar', edgecolor='k', ax=ax2,
                        color=ba_rgb2[1], legend=False, width=1)
    mpl.rcParams['font.family'] = 'Graphik'
    ax2.yaxis.tick_right()
    ax2.yaxis.set_ticks_position('right')
    ax2.yaxis.set_label_position("right")
    ax1.grid(False)
    ax2.grid(False)
    ax2.spines[['left', 'top']].set_visible(False)
    sns.despine(ax=ax1)
    ax1.set_title('a.', loc='left', fontsize=18, y=1.025)
    ax2.set_title('b.', loc='left', fontsize=18, y=1.025)
    ax2.set_ylabel('Likelihood of Reassignment', fontsize=15)
    ax2.set_xlabel('Original BERT Weight', fontsize=15)
    ax1.set_ylabel('Frequency', fontsize=15)
    ax1.set_xlabel('Original BERT Weight', fontsize=15)
    figure_path = os.path.join(os.getcwd(), '..', '..', 'figures')
    filename = 'figure_3'
    plt.savefig(os.path.join(figure_path,
                             filename + '.svg'),
                bbox_inches='tight')
