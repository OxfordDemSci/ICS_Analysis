import os
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl


def groupby_plotter(grp, figure_path, filename):
    """ Plot the groupedby aggregate data"""
    mpl.rcParams['font.family'] = 'Helvetica'
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