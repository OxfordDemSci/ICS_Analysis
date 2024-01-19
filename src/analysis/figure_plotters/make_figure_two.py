import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.ticker as tkr
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

mpl.rcParams['font.family'] = 'Graphik'
plt.rcParams["font.family"] = 'Graphik'
new_rc_params = {'text.usetex': False,
"svg.fonttype": 'none'
}
mpl.rcParams.update(new_rc_params)

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

    def rotate_point(x, y, angle_rad):
        cos, sin = np.cos(angle_rad), np.sin(angle_rad)
        return cos * x + sin * y, sin * x - cos * y

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
            ha='left', va='bottom',
            rotation=90 if rotate_text else 0,
            fontsize=18)


def make_brace(xmin, xmax, ax1, text, multi):
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
    y = ymin + (0.025 * y - .01) * yspan - 87
    ax1.autoscale(False)
    ax1.plot(x, y, color='black', lw=1, zorder=1, clip_on=False)
    ax1.text((xmax + xmin) / 2., ymin + 1.07 * yspan, text,
             ha='center', va='bottom', fontsize=24, rotation=0)


def make_figure_two():
    print('Making Figure 2!')
    df_ref = pd.read_csv(os.path.join(os.getcwd(),
                                      '..',
                                      '..',
                                      'data',
                                      'final',
                                      'enhanced_ref_data.csv'))
    df_lookup = pd.read_csv(os.path.join(os.getcwd(),
                                         '..',
                                         '..',
                                         'data',
                                         'manual',
                                         'topic_lookup',
                                         'topic_lookup.csv'),
                            encoding='cp1252')
    df_ref['Unit of assessment number'] = df_ref['Unit of assessment number'].astype(int)

    df_ref = df_ref[df_ref['topic_name_short'].notnull()]
    df = pd.DataFrame(0,
                      columns=df_lookup['topic_name_short'].str.strip().unique(),
                      index=df_ref['Unit of assessment number'].sort_values(ascending=True).unique())
    for index, row in df_ref.iterrows():
        df.at[row['Unit of assessment number'], row['topic_name_short'].strip()] += 1

    topic_order = df_lookup.drop_duplicates().sort_values(ascending=True,
                                                          by='cluster_id')['topic_name_short'].to_list()
    topic_names = df_lookup.drop_duplicates().sort_values(ascending=True,
                                                          by='cluster_id')['topic_name_short'].to_list()
    df = df[topic_order]
    topic_names = [x.strip() for x in topic_names]
    top_values = df.div(df.sum(axis=1), axis=0).stack().nlargest(10)
    for (row, col), value in top_values.items():
        print(f"UoA: {row}, Topic Short Name: {col}, Relative Frequency: {value}")

    fig, ax1 = plt.subplots(figsize=(16, 24))
    cmap = mpl.colors.LinearSegmentedColormap.from_list("",
                                                        ["white",
                                                         "#41558c",
                                                         "#E89818",
#                                                         "#CF202A",
                                                         ]
                                                        )
    figure_path = os.path.join(os.getcwd(), '..', '..', 'figures')
    cmap = plt.get_cmap(cmap)
    formatter = tkr.ScalarFormatter(useMathText=True)
    formatter.set_scientific(False)
    sns.heatmap(df.div(df.sum(axis=1), axis=0).transpose(),
                cmap=cmap,
                linewidths=.5,
                linecolor='w',
                ax=ax1, zorder=0,
                cbar=False
                )
    fig.colorbar(ax1.collections[0], ax=ax1,
                 location="bottom", use_gridspec=False,
                 pad=-0.10,
                 aspect=50,
                 shrink=1, anchor=(0, 0))
    sns.heatmap(df.div(df.sum(axis=1), axis=0).transpose(),
                cmap=cmap,
                norm=LogNorm(),
                linewidths=.5, zorder=0,
                linecolor='w',
                ax=ax1,
                cbar=False
                )

    ax1.set_xlabel('Topics', fontsize=16)
    cbar_ax = fig.axes[-1]
    cbar_ax.set_title('Relative Frequency',  # =.375, x=1,
                      rotation=0, fontsize=22)
    cbar_solids = cbar_ax.collections[0]
    cbar_solids.set_edgecolor("k")
    cbar_solids.set_lw(1.0)
    cbar_ax.tick_params(axis='both', which='major', labelsize=16)

    xmin, xmax = (1.5, 12.5)
    make_brace(xmin, xmax, ax1, 'Panel C', 20)
    xmin, xmax = (0, 1)
    make_brace(xmin, xmax, ax1, 'UoA 4', 20)
    xmin, xmax = (13.5, 22.5)
    make_brace(xmin, xmax, ax1, 'Panel D', 20)
    min_top, max_top = 0, 9

    x_indenter = 0.45
    starter = 24.3
    draw_brace(ax1,
               max_top - min_top - 1.35,
               [starter, min_top + ((max_top - min_top) / 2)],
               '1. Arts',
               [24.65, min_top + ((max_top - min_top) / 2) + x_indenter],
               rotate=True,
               rotate_text=False)

    min_top, max_top = 9, 21
    draw_brace(ax1,
               max_top - min_top - 1.35,
               [starter, min_top + ((max_top - min_top) / 2)],
               '2. Heritage',
               [24.5, min_top + ((max_top - min_top) / 2) + x_indenter],
               rotate=True,
               rotate_text=False)

    min_top, max_top = 21, 26
    draw_brace(ax1,
               max_top - min_top - 1.35,
               [starter, min_top + ((max_top - min_top) / 2)],
               '3. Education',
               [24.5, min_top + ((max_top - min_top) / 2) + x_indenter],
               rotate=True,
               rotate_text=False)

    min_top, max_top = 26, 30
    draw_brace(ax1,
               max_top - min_top - 1.35,
               [starter, min_top + ((max_top - min_top) / 2)],
               '4. Business',
               [24.5, min_top + ((max_top - min_top) / 2) + x_indenter],
               rotate=True,
               rotate_text=False)

    min_top, max_top = 30, 33
    draw_brace(ax1,
               max_top - min_top - 1.35,
               [starter, min_top + ((max_top - min_top) / 2)],
               '5. Employment',
               [24.5, min_top + ((max_top - min_top) / 2) + x_indenter],
               rotate=True,
               rotate_text=False)

    min_top, max_top = 33, 37
    draw_brace(ax1,
               max_top - min_top - 1.35,
               [starter, min_top + ((max_top - min_top) / 2)],
               '6. Crime',
               [24.5, min_top + ((max_top - min_top) / 2) + x_indenter],
               rotate=True,
               rotate_text=False)

    min_top, max_top = 37, 44
    draw_brace(ax1,
               max_top - min_top - 1.35,
               [starter, min_top + ((max_top - min_top) / 2)],
               '7. Family',
               [24.5, min_top + ((max_top - min_top) / 2) + x_indenter],
               rotate=True,
               rotate_text=False)

    min_top, max_top = 44, 59
    draw_brace(ax1,
               max_top - min_top - 1.35,
               [starter, min_top + ((max_top - min_top) / 2)],
               '8. Governance',
               [24.5, min_top + ((max_top - min_top) / 2) + x_indenter],
               rotate=True,
               rotate_text=False)

    min_top, max_top = 59, 73
    draw_brace(ax1,
               max_top - min_top - 1.35,
               [starter, min_top + ((max_top - min_top) / 2)],
               '9. Health',
               [24.5, min_top + ((max_top - min_top) / 2) + x_indenter],
               rotate=True,
               rotate_text=False)

    min_top, max_top = 73, 84
    draw_brace(ax1,
               max_top - min_top - 1.35,
               [starter, min_top + ((max_top - min_top) / 2)],
               '10. Environment',
               [24.5, min_top + ((max_top - min_top) / 2) + x_indenter],
               rotate=True,
               rotate_text=False)

    ax1.tick_params(axis='both', which='major', labelsize=14)
    ax1.set_xlabel('Unit of Assessment', fontsize=20, y=.38)
    ax1.xaxis.set_label_position('top')
    ax1.xaxis.set_ticks_position('top')
    ax1.yaxis.set_ticks_position('both')
    sns.despine(offset=5, trim=True, ax=ax1, bottom=False, top=False, right=False)

    filename = 'figure_2'
    plt.savefig(os.path.join(figure_path, filename + '.svg'), bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, filename + '.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, filename + '.png'), bbox_inches='tight',
                dpi=800, transparent=True, facecolor='white')
    zero_counts = df.eq(0).sum(axis=1)
    print("UoAs which span the least amount of topics?")
    print(zero_counts.nlargest(5).index)
    print("UoAs which span the most amount of topics?")
    print(zero_counts.nsmallest(5).index)
