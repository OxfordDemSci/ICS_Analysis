import os
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl


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
    ax3.set_xlabel('Doctoral Degrees Conferred', fontsize=14)
    ax1.set_xlim(0, )
    ax3.set_xlim(0, )

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

    # sns.despine()
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