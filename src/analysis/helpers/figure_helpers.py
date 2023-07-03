import re
import os
import ast
import json
import warnings
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.ticker as tkr
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.colors import LogNorm
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.offsetbox import AnchoredText
from helpers.general_helpers import return_paper_level
from nltk.stem.snowball import SnowballStemmer
import gender_guesser.detector as gender
d = gender.Detector()
from helpers.text_helpers import freq_dist, co_occurrence, set_diag, truncate_colormap
warnings.filterwarnings('ignore')
mpl.rc('font', family='Arial')
csfont = {'fontname': 'Arial'}
hfont = {'fontname': 'Arial'}


def plot_impact_type_combined(df, figure_path):

    fig = plt.figure(figsize=(18, 12))
    gs = gridspec.GridSpec(16, 17, hspace=5, wspace=2)

    ax1 = fig.add_subplot(gs[0:2, 0:12])
    ax2 = fig.add_subplot(gs[2:4, 0:12])
    ax3 = fig.add_subplot(gs[4:6, 0:12])
    ax4 = fig.add_subplot(gs[6:8, 0:12])
    ax5 = fig.add_subplot(gs[8:10, 0:12])
    ax6 = fig.add_subplot(gs[10:12, 0:12])
    ax7 = fig.add_subplot(gs[12:14, 0:12])
    ax8 = fig.add_subplot(gs[14:16, 0:12])

    ax9 = fig.add_subplot(gs[0:16, 12:16])
    ax10 = fig.add_subplot(gs[0:16, 16:17])






    # uoa thing here

    groupby_counter = df.groupby(['Unit of assessment number']).size().reset_index().rename({0: 'Count'}, axis=1)
    temp = df.groupby(['Unit of assessment number',
                       'Summary impact type']).size().reset_index().rename({0: 'Count'}, axis=1)
    groupby_counter = groupby_counter.set_index('Unit of assessment number')
    Environmental = temp[temp['Summary impact type'] == 'Environmental'].rename({0: 'Count'}, axis=1)
    Environmental = Environmental.set_index('Unit of assessment number')
    groupby_counter['Environmental'] = Environmental['Count']
    groupby_counter['Environmental_pc'] = (groupby_counter['Environmental']/groupby_counter['Count'])*100
    Health = temp[temp['Summary impact type'] == 'Health'].rename({0: 'Count'}, axis=1)
    Health = Health.set_index('Unit of assessment number')
    groupby_counter['Health'] = Health['Count']
    groupby_counter['Health_pc'] = (groupby_counter['Health']/groupby_counter['Count'])*100
    Political = temp[temp['Summary impact type'] == 'Political'].rename({0: 'Count'}, axis=1)
    Political = Political.set_index('Unit of assessment number')
    groupby_counter['Political'] = Political['Count']
    groupby_counter['Political_pc'] = (groupby_counter['Political']/groupby_counter['Count'])*100
    Societal = temp[temp['Summary impact type'] == 'Societal'].rename({0: 'Count'}, axis=1)
    Societal = Societal.set_index('Unit of assessment number')
    groupby_counter['Societal'] = Societal['Count']
    groupby_counter['Societal_pc'] = (groupby_counter['Societal']/groupby_counter['Count'])*100
    Technological = temp[temp['Summary impact type'] == 'Technological'].rename({0: 'Count'}, axis=1)
    Technological = Technological.set_index('Unit of assessment number')
    groupby_counter['Technological'] = Technological['Count']
    groupby_counter['Technological_pc'] = (groupby_counter['Technological']/groupby_counter['Count'])*100
    Legal = temp[temp['Summary impact type'] == 'Legal'].rename({0: 'Count'}, axis=1)
    Legal = Legal.set_index('Unit of assessment number')
    groupby_counter['Legal'] = Legal['Count']
    groupby_counter['Legal_pc'] = (groupby_counter['Legal']/groupby_counter['Count'])*100
    Economic = temp[temp['Summary impact type'] == 'Economic'].rename({0: 'Count'}, axis=1)
    Economic = Economic.set_index('Unit of assessment number')
    groupby_counter['Economic'] = Economic['Count']
    groupby_counter['Economic_pc'] = (groupby_counter['Economic']/groupby_counter['Count'])*100
    Cultural = temp[temp['Summary impact type'] == 'Cultural'].rename({0: 'Count'}, axis=1)
    Cultural = Cultural.set_index('Unit of assessment number')
    groupby_counter['Cultural'] = Cultural['Count']
    groupby_counter['Cultural_pc'] = (groupby_counter['Cultural']/groupby_counter['Count'])*100
    groupby_counter['Environmental_pc'].plot(kind='bar', ax=ax1, ec='k')
    groupby_counter['Health_pc'].plot(kind='bar', ax=ax2, ec='k')
    groupby_counter['Political_pc'].plot(kind='bar', ax=ax3, ec='k')
    groupby_counter['Societal_pc'].plot(kind='bar', ax=ax4, ec='k')
    groupby_counter['Technological_pc'].plot(kind='bar', ax=ax5, ec='k')
    groupby_counter['Legal_pc'].plot(kind='bar', ax=ax6, ec='k')
    groupby_counter['Economic_pc'].plot(kind='bar', ax=ax7, ec='k')
    groupby_counter['Cultural_pc'] .plot(kind='bar', ax=ax8, ec='k')
    ax1.set_title('A.', loc='left', fontsize=18, x=-0.015)
    ax2.set_title('B.', loc='left', fontsize=18, x=-0.015)
    ax3.set_title('C.', loc='left', fontsize=18, x=-0.015)
    ax4.set_title('D.', loc='left', fontsize=18, x=-0.015)
    ax5.set_title('E.', loc='left', fontsize=18, x=-0.015)
    ax6.set_title('F.', loc='left', fontsize=18, x=-0.015)
    ax7.set_title('G.', loc='left', fontsize=18, x=-0.015)
    ax8.set_title('H.', loc='left', fontsize=18, x=-0.015)
    #ax1.set_ylabel('Environment', rotation=0, fontsize=15)
    #ax2.set_ylabel('Health', rotation=0, fontsize=15)
    #ax3.set_ylabel('Political', rotation=0, fontsize=15)
    #ax4.set_ylabel('Societal', rotation=0, fontsize=15)
    #ax5.set_ylabel('Technological', rotation=0, fontsize=15)
    #ax6.set_ylabel('Legal', rotation=0, fontsize=15)
    #ax7.set_ylabel('Economic', rotation=0, fontsize=15)
    #ax8.set_ylabel('Cultural', rotation=0, fontsize=15)
    colors2 = ['#001c54', '#E89818']
    plt.tight_layout()
    for ax in [ax1, ax2, ax3, ax4, ax5, ax6, ax7]:
        ax.set_xticklabels([])
        ax.set_xlabel('')
    ax8.set_xticklabels(ax8.get_xticklabels(), rotation=0, fontsize=14);
    ax8.set_xlabel('Unit of Assessment Number', fontsize=20)
    for ax in [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8]:
        for uoa in range(0, 34):
            ax.get_children()[uoa].set_color(colors2[0])
            ax.get_children()[uoa].set_edgecolor('k')
            ax.get_children()[3].set_color(colors2[1])
            ax.get_children()[3].set_edgecolor('k')
            for uoa in range(13, 34):
                ax.get_children()[uoa].set_color(colors2[1])
                ax.get_children()[uoa].set_edgecolor('k')
    figure_name = 'impacttype_vs_uoa'
    legend_elements = [Patch(facecolor=colors2[0], edgecolor='k',
                             label=r'STEM', alpha=0.7),
                       Patch(facecolor=colors2[1], edgecolor='k',
                             label=r'SHAPE', alpha=0.7)]
    ax8.legend(handles=legend_elements,
               frameon=True,
               fontsize=15, framealpha=1, facecolor='w',
               edgecolor=(0, 0, 0, 1), ncol=2,
               loc = 'upper left',# bbox_to_anchor=(1.00, 1)
              )
    for ax in [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8]:
        ax.set_ylim(0, 100)
        ax.tick_params(axis='both', which='major', labelsize=14)
        ylabels = ['{:,.0f}'.format(x) + '%' for x in ax.get_yticks()]
        ax.set_yticklabels(ylabels)
        sns.despine(ax=ax)

    #    plt.savefig(os.path.join(figure_path, figure_name + '.pdf'),
    #                bbox_inches='tight')
    #    plt.savefig(os.path.join(figure_path, figure_name + '.png'),
    #                bbox_inches='tight', dpi=400,
    #                facecolor='white', transparent=False)






    # heatmap thing here

    dfA = df[df['Main panel']=='A'].groupby('Summary impact type')['Summary impact type'].count()
    dfB = df[df['Main panel']=='B'].groupby('Summary impact type')['Summary impact type'].count()
    dfC = df[df['Main panel']=='C'].groupby('Summary impact type')['Summary impact type'].count()
    dfD = df[df['Main panel']=='D'].groupby('Summary impact type')['Summary impact type'].count()
    dfA = pd.DataFrame(dfA).rename({'Summary impact type': 'Panel: A'}, axis=1)
    dfB = pd.DataFrame(dfB).rename({'Summary impact type': 'Panel: B'}, axis=1)
    dfC = pd.DataFrame(dfC).rename({'Summary impact type': 'Panel: C'}, axis=1)
    dfD = pd.DataFrame(dfD).rename({'Summary impact type': 'Panel: D'}, axis=1)
    df_merge = pd.merge(pd.DataFrame(dfA), pd.DataFrame(dfB), how='left', left_index=True, right_index=True)
    df_merge = pd.merge(df_merge, pd.DataFrame(dfC), how='left', left_index=True, right_index=True)
    df_merge = pd.merge(df_merge, pd.DataFrame(dfD), how='left', left_index=True, right_index=True)
    a = df_merge.melt(ignore_index=False).reset_index()

    def heatmap(x, y, figsize, figure_path, filename, ax9, ax_cbar, **kwargs):
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
    #    plot_grid = plt.GridSpec(1, 15, hspace=0.2, wspace=0.1)
    #    print(figsize)
    #    ax9 = plt.subplot(plot_grid[:,:-1])
        marker = kwargs.get('marker', 's')
        kwargs_pass_on = {k:v for k,v in kwargs.items() if k not in [
             'color', 'palette', 'color_range', 'size',
             'size_range', 'size_scale', 'marker', 'x_order', 'y_order'
        ]}
        [x_to_num[v] for v in x]
        ax9.scatter(
            x=[x_to_num[v] for v in x],
            y=[y_to_num[v] for v in y],
            marker=marker,
            s=[value_to_size(v*5) for v in size],
            c=[value_to_color(v) for v in color],
            edgecolor='k',
            **kwargs_pass_on)
        ax9.set_xticks([v for k,v in x_to_num.items()])
        ax9.set_xticklabels([k for k in x_to_num], rotation=90, horizontalalignment='right', fontsize=14)
        ax9.set_yticks([v for k,v in y_to_num.items()])
        ax9.set_yticklabels([k for k in y_to_num], fontsize=14)
    #    ax9.set_yticklabels([])
        ax9.grid(False, 'major')
        ax9.grid(True, 'minor')
        ax9.set_xticks([t + 0.5 for t in ax9.get_xticks()], minor=True)
        ax9.set_yticks([t + 0.5 for t in ax9.get_yticks()], minor=True)
        ax9.set_xlim([-0.5, max([v for v in x_to_num.values()]) + 0.5])
        ax9.set_ylim([-0.5, max([v for v in y_to_num.values()]) + 0.5])
        ax9.set_facecolor('white')
        ax9.set_title('I.', loc ='left', fontsize=18)
        if color_min < color_max:
    #        ax = plt.subplot(plot_grid[:,-1])
            col_x = [0]*len(palette)
            bar_y=np.linspace(color_min, color_max, n_colors)
            bar_height = bar_y[1] - bar_y[0]
            ax_cbar.barh(
                y=bar_y,
                width=[5]*len(palette),
                left=col_x,
                height=bar_height,
                color=palette,
                linewidth=5
            )
            ax_cbar.set_xlim(1, 2)
            ax_cbar.grid(False)
            ax_cbar.set_facecolor('white')
    #        sns.despine(ax=ax9, left=True, bottom=True)
            ax_cbar.set_xticks([])
            ax_cbar.set_yticks(np.linspace(min(bar_y), max(bar_y), 5))
            ax_cbar.yaxis.tick_right()
            ax_cbar.tick_params(axis='y', which='major', labelsize=13)
        ax_cbar.set_ylim(0, 1356)


    heatmap(
        x=a['variable'],
        y=a['Summary impact type'],
        figsize = (16, 10),
        figure_path = figure_path,
        filename = 'panel_by_type',
        ax9=ax9,
        ax_cbar=ax10,
        size=a['value'],
        color=a['value'],
        color_range=[0, a['value'].max()],
        marker='h'
    )
    plt.tight_layout()
    filename = 'panel_by_type'
    plt.savefig(os.path.join(figure_path, filename + '.pdf'), bbox_inches = 'tight')
    plt.savefig(os.path.join(figure_path, filename + '.png'), bbox_inches = 'tight',
                dpi=400, facecolor='white', transparent=False)


def plot_funders():
    import gender_guesser.detector as gender
    d = gender.Detector()
    funder_level = pd.DataFrame(columns=['Panel', 'UoA', 'ICS_uid', 'pub_uid', 'funder'])
    dim_out = os.path.join(os.getcwd(), '..', '..',
                           'data', 'dimensions_returns')
    paper_level = return_paper_level(dim_out)
    figure_path = os.path.join(os.getcwd(), '..', '..', 'figures')
    grid_lookup = pd.read_csv(os.path.join(os.getcwd(), '..', '..', 'data', 'intermediate', 'grid_lookup.csv'))

    counter = 0

    for index, row in paper_level.iterrows():
        funder_raw = row['funder_orgs']
        funder_list = re.findall("'(.*?)'", funder_raw)#.split(' ')
        for funder in funder_list:
            funder_level.at[counter, 'Panel'] = row['Main panel']
            funder_level.at[counter, 'UoA'] = int(row['Unit of assessment number'])
            funder_level.at[counter, 'ICS_uid'] = row['Key']
            funder_level.at[counter, 'pub_uid'] = row['id']
            funder_level.at[counter, 'funder'] = funder
            counter += 1
    funder_level = pd.merge(funder_level, grid_lookup, how='left', left_on = 'funder', right_on = 'grid')
    d = gender.Detector()

    dim_out = os.path.join(os.getcwd(), '..', '..',
                           'data', 'dimensions_returns')
    paper_level = return_paper_level(dim_out)
    figure_path = os.path.join(os.getcwd(), '..', '..', 'figures')
    grid_lookup = pd.read_csv(os.path.join(os.getcwd(), '..', '..', 'data', 'intermediate', 'grid_lookup.csv'))

    funder_level_C = funder_level[funder_level['Panel']=='C']
    funder_counts_C = funder_level_C['name'].value_counts()

    funder_level_D = funder_level[funder_level['Panel']=='D']
    funder_counts_D = funder_level_D['name'].value_counts()

    funder_level_4 = funder_level[funder_level['UoA']==4.0]
    funder_counts_4 = funder_level_4['name'].value_counts()


    counter = 0
    df = pd.read_excel(os.path.join(os.getcwd(), '..', '..',
                                    'data', 'raw', 'raw_ics_data.xlsx'))

    df = df[df['Global research identifiers'].notnull()]
    import numpy as np

    ICS_funder_level = pd.DataFrame(columns=['Panel', 'UoA', 'ICS_uid', 'funder'])
    for index, row in paper_level.iterrows():
        if row['Global research identifiers'] is not np.nan:
            funder_row = row['Global research identifiers'].split(';')
            for funder in funder_row:
                ICS_funder_level.at[counter, 'Panel'] = row['Main panel']
                ICS_funder_level.at[counter, 'UoA'] = int(row['Unit of assessment number'])
                ICS_funder_level.at[counter, 'ICS_uid'] = row['REF impact case study identifier']
                ICS_funder_level.at[counter, 'funder'] = funder[1:-1]
                counter+=1


    ICS_funder_level['funder'] = np.where(ICS_funder_level['funder']=="270680.b", "grid.270680.b", ICS_funder_level['funder'])
    ICS_funder_level['funder'] = np.where(ICS_funder_level['funder']=="434257.3", "grid.434257.3", ICS_funder_level['funder'])
    ICS_funder_level['funder'] = np.where(ICS_funder_level['funder']=="2) grid.421126.2", "grid.421126.2", ICS_funder_level['funder'])
    ICS_funder_level['funder'] = np.where(ICS_funder_level['funder']=="1) grid.435802.8", "grid.435802.8", ICS_funder_level['funder'])


    ICS_funder_level['funder'] = np.where(ICS_funder_level['funder']=="426413.6", "grid.426413.6", ICS_funder_level['funder'])
    ICS_funder_level['funder'] = np.where(ICS_funder_level['funder']=="452966.a", "grid.452966.a", ICS_funder_level['funder'])
    ICS_funder_level['funder'] = np.where(ICS_funder_level['funder']=="2) grid.426413.6", "grid.426413.6", ICS_funder_level['funder'])
    ICS_funder_level['funder'] = np.where(ICS_funder_level['funder']=="1) grid.434257.3", "grid.434257.3", ICS_funder_level['funder'])

    ICS_funder_level['funder'] = np.where(ICS_funder_level['funder']=="2) grid.426413 .6", "grid.426413.6", ICS_funder_level['funder'])
    ICS_funder_level['funder'] = np.where(ICS_funder_level['funder']=="3) grid.434257.3", "grid.434257.3", ICS_funder_level['funder'])
    ICS_funder_level['funder'] = np.where(ICS_funder_level['funder']=="5) grid.434257.3", "grid.434257.3", ICS_funder_level['funder'])
    ICS_funder_level['funder'] = np.where(ICS_funder_level['funder']=="4) grid.502745.1", "grid.502745.1 ", ICS_funder_level['funder'])


    ICS_funder_level['funder'] = np.where(ICS_funder_level['funder']=="450921.b", "grid.450921.b", ICS_funder_level['funder'])
    ICS_funder_level['funder'] = np.where(ICS_funder_level['funder']=="2) grid.426413.6", "grid.426413.6", ICS_funder_level['funder'])
    ICS_funder_level['funder'] = np.where(ICS_funder_level['funder']=="4) grid.502745.1", "grid.502745.1", ICS_funder_level['funder'])

    ICS_funder_level['funder'] = ICS_funder_level['funder'].replace("1) ", "", regex=False)
    ICS_funder_level['funder'] = ICS_funder_level['funder'].replace("2) ", "", regex=False)
    ICS_funder_level['funder'] = ICS_funder_level['funder'].replace("3) ", "", regex=False)
    ICS_funder_level['funder'] = ICS_funder_level['funder'].replace("4) ", "", regex=False)
    ICS_funder_level['funder'] = ICS_funder_level['funder'].replace("5) ", "", regex=False)
    ICS_funder_level['funder'] = ICS_funder_level['funder'].replace("6) ", "", regex=False)
    ICS_funder_level['funder'] = ICS_funder_level['funder'].replace("7) ", "", regex=False)
    ICS_funder_level['funder'] = ICS_funder_level['funder'].replace("8) ", "", regex=False)
    ICS_funder_level['funder'] = ICS_funder_level['funder'].replace("9) ", "", regex=False)


    ICS_funder_level = pd.merge(ICS_funder_level, grid_lookup, how='left', left_on = 'funder', right_on = 'grid')


    ICS_funder_level_C = ICS_funder_level[ICS_funder_level['Panel']=='C']
    ICS_funder_level_D = ICS_funder_level[ICS_funder_level['Panel']=='D']
    ICS_funder_level_4 = ICS_funder_level[ICS_funder_level['UoA']==4.0]

    ICS_funder_level_C  = ICS_funder_level_C['name'].value_counts()
    ICS_funder_level_D  = ICS_funder_level_D['name'].value_counts()
    ICS_funder_level_4  = ICS_funder_level_4['name'].value_counts()



    colors2 = ['#001c54', '#E89818']
    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(16, 9))
    funder_counts_C[0:5].sort_values().plot(kind='barh', ax=ax1, edgecolor='k', color = colors2[0])
    funder_counts_D[0:5].sort_values().plot(kind='barh', ax=ax2, edgecolor='k', color = colors2[1])
    funder_counts_4[0:5].sort_values().plot(kind='barh', ax=ax3, edgecolor='k', color = colors2[0])
    ICS_funder_level_C[0:5].sort_values().plot(kind='barh', ax=ax4, edgecolor='k', color = colors2[1])
    ICS_funder_level_D[0:5].sort_values().plot(kind='barh', ax=ax5, edgecolor='k', color = colors2[0])
    ICS_funder_level_4[0:5].sort_values().plot(kind='barh', ax=ax6, edgecolor='k', color = colors2[1])

    ax1.set_title('A.', loc='left', fontsize=17)
    ax2.set_title('B.', loc='left', fontsize=17)
    ax3.set_title('C.', loc='left', fontsize=17)
    ax4.set_title('D.', loc='left', fontsize=17)
    ax5.set_title('E.', loc='left', fontsize=17)
    ax6.set_title('F.', loc='left', fontsize=17)
    ax4.set_xlabel('Instances of Funding', fontsize=16)
    ax5.set_xlabel('Instances of Funding', fontsize=16)
    ax6.set_xlabel('Instances of Funding', fontsize=16)

    sns.despine()
    plt.tight_layout()
    fig_path = os.path.join(os.getcwd(), '..', '..', 'figures')
    filename = 'funding'
    plt.savefig(os.path.join(fig_path, filename + '.pdf'),
                bbox_inches = 'tight')
    plt.savefig(os.path.join(fig_path, filename + '.png'),
                bbox_inches = 'tight',
                dpi=400, facecolor='white', transparent=False)


def make_interdisciplinarity():
    dim_out = os.path.join(os.getcwd(), '..', '..',
                           'data', 'dimensions_returns')
    paper_level = return_paper_level(dim_out)
    second_level = paper_level['category_for'][0].split('second_level')[1]
    first_level = paper_level['category_for'][0].split('second_level')[0]
    for_set = set()
    for index, row in paper_level.iterrows():
        paper_fors = row['category_for']
        if paper_fors is not np.nan:
            first_level = paper_fors.split('second_level')[0]
            for_set = for_set.union(set(re.findall(r"'name': '(.*?)'", first_level)))
    df = pd.DataFrame(0, columns = list(for_set), index = list(for_set))

    for index, row in paper_level.iterrows():
        paper_fors = row['category_for']
        if paper_fors is not np.nan:
            first_level = paper_fors.split('second_level')[0]
            for_set_row = set(re.findall(r"'name': '(.*?)'", first_level))
            for_set = for_set.union(for_set_row)
            if len(for_set_row)>1:
                for field1 in for_set_row:
                    for field2 in for_set_row:
                        if field1!=field2:
                            df.at[field1, field2] += 1

    df = df.rename({'Information And Computing Sciences': 'IT'}, axis=0)
    df = df.rename({'Information And Computing Sciences': 'IT'}, axis=1)

    df = df.rename({'Built Environment And Design': 'Urban'}, axis=0)
    df = df.rename({'Built Environment And Design': 'Urban'}, axis=1)

    df = df.rename({'Biological Sciences': 'Biology'}, axis=0)
    df = df.rename({'Biological Sciences': 'Biology'}, axis=1)

    df = df.rename({'Health Sciences': 'Health'}, axis=0)
    df = df.rename({'Health Sciences': 'Health'}, axis=1)

    df = df.rename({'Language, Communication And Culture': 'Language'}, axis=0)
    df = df.rename({'Language, Communication And Culture': 'Language'}, axis=1)

    df = df.rename({'Earth Sciences': 'Earth'}, axis=0)
    df = df.rename({'Earth Sciences': 'Earth'}, axis=1)

    df = df.rename({'Physical Sciences': 'Physics'}, axis=0)
    df = df.rename({'Physical Sciences': 'Physics'}, axis=1)

    df = df.rename({'Chemical Sciences': 'Chem'}, axis=0)
    df = df.rename({'Chemical Sciences': 'Chem'}, axis=1)

    df = df.rename({'Economics': 'Econ'}, axis=1)
    df = df.rename({'Economics': 'Econ'}, axis=1)

    df = df.rename({'Biomedical And Clinical Sciences': 'Biomedical'}, axis=0)
    df = df.rename({'Biomedical And Clinical Sciences': 'Biomedical'}, axis=1)

    df = df.rename({'Agricultural, Veterinary And Food Sciences': 'Agriculture'}, axis=0)
    df = df.rename({'Agricultural, Veterinary And Food Sciences': 'Agriculture'}, axis=1)

    df = df.rename({'History, Heritage And Archaeology': 'History'}, axis=0)
    df = df.rename({'History, Heritage And Archaeology': 'History'}, axis=1)

    df = df.rename({'Law And Legal Studies': 'Law'}, axis=0)
    df = df.rename({'Law And Legal Studies': 'Law'}, axis=1)


    df = df.rename({'Environmental Sciences': 'Environmental'}, axis=0)
    df = df.rename({'Environmental Sciences': 'Environmental'}, axis=1)

    df = df.rename({'Law And Legal Studies': 'Law'}, axis=0)
    df = df.rename({'Law And Legal Studies': 'Law'}, axis=1)

    df = df.rename({'Creative Arts And Writing': 'Creative'}, axis=0)
    df = df.rename({'Creative Arts And Writing': 'Creative'}, axis=1)

    df = df.rename({'Commerce, Management, Tourism And Services': 'Tourism'}, axis=0)
    df = df.rename({'Commerce, Management, Tourism And Services': 'Tourism'}, axis=1)


    df = df.rename({'Mathematical Sciences': 'Mathematics'}, axis=0)
    df = df.rename({'Mathematical Sciences': 'Mathematics'}, axis=1)


    df = df.rename({'Philosophy And Religious Studies': 'Religion'}, axis=0)
    df = df.rename({'Philosophy And Religious Studies': 'Religion'}, axis=1)


    df = df.rename({'Human Society': 'Society'}, axis=0)
    df = df.rename({'Human Society': 'Society'}, axis=1)
    df.to_csv(os.path.join(os.getcwd(), '..', '..', 'data', 'intermediate', 'all_interdisciplinarity.csv'))


def plot_gender(figure_path):
    dim_out = os.path.join(os.getcwd(), '..', '..',
                           'data', 'dimensions_returns')
    paper_level = return_paper_level(dim_out)
    figure_path = os.path.join(os.getcwd(), '..', '..', 'figures')
    author_level = pd.DataFrame(columns=['Panel', 'UoA', 'ICS_uid', 'pub_uid', 'first_name', 'gender'])
    counter = 0
    for index, row in paper_level.iterrows():
        paper_authors = row['authors']
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

    fig, (ax1) = plt.subplots(1, 1, figsize=(16, 6))
    uoa_fem.plot(kind='bar', ax=ax1, ec='k')

    colors2 = ['#001c54', '#E89818']
    plt.tight_layout()
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=0, fontsize=14)
    ax1.set_xlabel('Unit of Assessment Number', fontsize=20)
    for ax in [ax1]:
        for uoa in range(0, 13):
            ax.get_children()[uoa].set_color(colors2[0])
            ax.get_children()[uoa].set_edgecolor('k')
            ax.get_children()[3].set_color(colors2[1])
            ax.get_children()[3].set_edgecolor('k')
        for uoa in range(13, 34):
            ax.get_children()[uoa].set_color(colors2[1])
            ax.get_children()[uoa].set_edgecolor('k')
    legend_elements = [Patch(facecolor=colors2[0], edgecolor='k',
                             label=r'STEM', alpha=0.7),
                       Patch(facecolor=colors2[1], edgecolor='k',
                             label=r'SHAPE', alpha=0.7)]
    for ax in [ax1]:
        ax.legend(handles=legend_elements,
                  frameon=True,
                  fontsize=15, framealpha=1, facecolor='w',
                  edgecolor=(0, 0, 0, 1), ncol=1,
                  loc='center right', bbox_to_anchor=(1.125, 0.5)
                  )
    ax1.set_title('A.', loc='left', fontsize=18)
    ax1.set_ylabel('Fraction Female', fontsize=18)
    ax1.set_ylim(0, 0.65)
    A_cited = pd.DataFrame(paper_panels).at['A', 'female']
    B_cited = pd.DataFrame(paper_panels).at['B', 'female']
    C_cited = pd.DataFrame(paper_panels).at['C', 'female']
    D_cited = pd.DataFrame(paper_panels).at['D', 'female']
    draw_brace(ax1, (0, 6), 0.6, 'Panel A: ' + str(round(A_cited, 2)))
    draw_brace(ax1, (7, 12), 0.6, 'Panel B: ' + str(round(B_cited, 2)))
    draw_brace(ax1, (13, 24), 0.6, 'Panel C: ' + str(round(C_cited, 2)))
    draw_brace(ax1, (25, 33), 0.6, 'Panel D: ' + str(round(D_cited, 2)))

    plt.tight_layout()
    sns.despine()
    filename = 'percent_female'
    plt.savefig(os.path.join(figure_path, filename + '.pdf'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, filename + '.png'),
                bbox_inches='tight',
                dpi=400, facecolor='white', transparent=False)


def plot_heat_topics(heat_topics, count, figure_path):
    sns.set_style('ticks')
    fig, ax1 = plt.subplots(figsize=(18, 6))
    heat_topics = heat_topics.sort_index()
    cmap = plt.get_cmap('RdBu_r')
    formatter = tkr.ScalarFormatter(useMathText=True)
    formatter.set_scientific(False)
    sns.heatmap(heat_topics.div(count, axis=0),
                cmap=cmap,
                linewidths=.1,
                linecolor='k',
                ax=ax1,
                cbar=False
                #                cbar_ax = cbar_ax,
                #                cbar_kws={'ticks': [0.05, 0.10, 0.15, 0.20, 0.25],
                #                          "shrink": 1,
                #                          'use_gridspec': True,
                #                          'pad': 0.0125,
                ##                          'edgecolor': 'k',
                #                          "format": formatter}
                )
    fig.colorbar(ax1.collections[0], ax=ax1, location="right", use_gridspec=False, pad=0.0125)
    sns.heatmap(heat_topics.div(count, axis=0),
                cmap=cmap,
                norm=LogNorm(),
                linewidths=.1,
                linecolor='k',
                ax=ax1,
                cbar=False
                )
    ax1.set_xlabel('Topics', fontsize=16)
    ax1.set_ylabel('Units of Assessment', fontsize=14)
    ax1.set_title('A.', fontsize=16, loc='left')

    cbar_ax = fig.axes[-1]
    cbar_solids = cbar_ax.collections[0]
    cbar_solids.set_edgecolor("k")
    cbar_solids.set_lw(1.0)
    plt.savefig(os.path.join(figure_path, 'topics_weighted_uoas.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'topics_weighted_uoas.png'),
                dpi=600, bbox_inches='tight')

def plot_impacttype_vs_uoa(figure_path, df):
    groupby_counter = df.groupby(['Unit of assessment number']).size().reset_index().rename({0: 'Count'}, axis=1)
    temp = df.groupby(['Unit of assessment number',
                       'Summary impact type']).size().reset_index().rename({0: 'Count'}, axis=1)
    groupby_counter = groupby_counter.set_index('Unit of assessment number')


    Environmental = temp[temp['Summary impact type'] == 'Environmental'].rename({0: 'Count'}, axis=1)
    Environmental = Environmental.set_index('Unit of assessment number')
    groupby_counter['Environmental'] = Environmental['Count']
    groupby_counter['Environmental_pc'] = (groupby_counter['Environmental']/groupby_counter['Count'])*100

    Health = temp[temp['Summary impact type'] == 'Health'].rename({0: 'Count'}, axis=1)
    Health = Health.set_index('Unit of assessment number')
    groupby_counter['Health'] = Health['Count']
    groupby_counter['Health_pc'] = (groupby_counter['Health']/groupby_counter['Count'])*100

    Political = temp[temp['Summary impact type'] == 'Political'].rename({0: 'Count'}, axis=1)
    Political = Political.set_index('Unit of assessment number')
    groupby_counter['Political'] = Political['Count']
    groupby_counter['Political_pc'] = (groupby_counter['Political']/groupby_counter['Count'])*100

    Societal = temp[temp['Summary impact type'] == 'Societal'].rename({0: 'Count'}, axis=1)
    Societal = Societal.set_index('Unit of assessment number')
    groupby_counter['Societal'] = Societal['Count']
    groupby_counter['Societal_pc'] = (groupby_counter['Societal']/groupby_counter['Count'])*100

    Technological = temp[temp['Summary impact type'] == 'Technological'].rename({0: 'Count'}, axis=1)
    Technological = Technological.set_index('Unit of assessment number')
    groupby_counter['Technological'] = Technological['Count']
    groupby_counter['Technological_pc'] = (groupby_counter['Technological']/groupby_counter['Count'])*100

    Legal = temp[temp['Summary impact type'] == 'Legal'].rename({0: 'Count'}, axis=1)
    Legal = Legal.set_index('Unit of assessment number')
    groupby_counter['Legal'] = Legal['Count']
    groupby_counter['Legal_pc'] = (groupby_counter['Legal']/groupby_counter['Count'])*100

    Economic = temp[temp['Summary impact type'] == 'Economic'].rename({0: 'Count'}, axis=1)
    Economic = Economic.set_index('Unit of assessment number')
    groupby_counter['Economic'] = Economic['Count']
    groupby_counter['Economic_pc'] = (groupby_counter['Economic']/groupby_counter['Count'])*100

    Cultural = temp[temp['Summary impact type'] == 'Cultural'].rename({0: 'Count'}, axis=1)
    Cultural = Cultural.set_index('Unit of assessment number')
    groupby_counter['Cultural'] = Cultural['Count']
    groupby_counter['Cultural_pc'] = (groupby_counter['Cultural']/groupby_counter['Count'])*100
    fig, (ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8) = plt.subplots(8, 1, figsize=(16, 9),
                                                                 sharex='all')
    groupby_counter['Environmental_pc'].plot(kind='bar', ax=ax1, ec='k')
    groupby_counter['Health_pc'].plot(kind='bar', ax=ax2, ec='k')
    groupby_counter['Political_pc'].plot(kind='bar', ax=ax3, ec='k')
    groupby_counter['Societal_pc'].plot(kind='bar', ax=ax4, ec='k')
    groupby_counter['Technological_pc'].plot(kind='bar', ax=ax5, ec='k')
    groupby_counter['Legal_pc'].plot(kind='bar', ax=ax6, ec='k')
    groupby_counter['Economic_pc'].plot(kind='bar', ax=ax7, ec='k')
    groupby_counter['Cultural_pc'] .plot(kind='bar', ax=ax8, ec='k')

    ax1.set_title('A. Environment', loc='left', fontsize=18)
    ax2.set_title('B. Health', loc='left', fontsize=18)
    ax3.set_title('C. Political', loc='left', fontsize=18)
    ax4.set_title('D. Societal', loc='left', fontsize=18)
    ax5.set_title('E. Technological', loc='left', fontsize=18)
    ax6.set_title('F. Legal', loc='left', fontsize=18)
    ax7.set_title('G. Economic', loc='left', fontsize=18)
    ax8.set_title('H. Cultural', loc='left', fontsize=18)

    colors2 = ['#001c54', '#E89818']

    plt.tight_layout()
    sns.despine()
    ax8.set_xticklabels(ax8.get_xticklabels(), rotation=0, fontsize=14);
    ax8.set_xlabel('Unit of Assessment Number', fontsize=20)
    for ax in [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8]:
        for uoa in range(0, 34):
            ax.get_children()[uoa].set_color(colors2[0])
            ax.get_children()[uoa].set_edgecolor('k')
        ax.get_children()[3].set_color(colors2[1])
        ax.get_children()[3].set_edgecolor('k')
        for uoa in range(13, 34):
            ax.get_children()[uoa].set_color(colors2[1])
            ax.get_children()[uoa].set_edgecolor('k')
    figure_name = 'impacttype_vs_uoa'

    legend_elements = [Patch(facecolor=colors2[0], edgecolor='k',
                             label=r'STEM', alpha=0.7),
                       Patch(facecolor=colors2[1], edgecolor='k',
                             label=r'SHAPE', alpha=0.7)]
    ax1.legend(handles=legend_elements,
               frameon=True,
               fontsize=15, framealpha=1, facecolor='w',
               edgecolor=(0, 0, 0, 1), ncol=2,
               loc = 'upper right', bbox_to_anchor=(1.005, 1.5)
              )

    for ax in [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8]:
        ax.set_ylim(0, 100)
        ax.tick_params(axis='both', which='major', labelsize=13)
        ylabels = ['{:,.0f}'.format(x) + '%' for x in ax.get_yticks()]
        ax.set_yticklabels(ylabels)

    plt.savefig(os.path.join(figure_path, figure_name + '.pdf'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, figure_name + '.png'),
                bbox_inches='tight', dpi=400,
                facecolor='white', transparent=False)


def score_read_vs_gpa(merge_path, figure_path):
    df_wtext = pd.read_pickle(os.path.join(merge_path, 'merged_with_text_features.pkl'))
    subset = ['Institution name', 'Unit of assessment number']
    scored = df_wtext.drop_duplicates(subset = subset)
    scored['ICS GPA'] = (pd.to_numeric(scored['4*_Impact'], errors='coerce')*4 +
                         pd.to_numeric(scored['3*_Impact'], errors='coerce')*3 +
                         pd.to_numeric(scored['2*_Impact'], errors='coerce')*2 +
                         pd.to_numeric(scored['1*_Impact'], errors='coerce')*1)/100
    shape_mask = ((scored['Main panel'] == 'C') |
                  (scored['Main panel'] == 'D') |
                  (scored['Unit of assessment number'] == '4'))
    scored = scored[shape_mask]
    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(12, 9),
                                                           sharey='row', sharex='col')
    colors2 = ['#001c54', '#E89818']

    def make_merge_score_nlp(df, variable):
        sentiment = df_wtext[subset].groupby(subset).mean([variable])
        sentiment = sentiment.reset_index()
        merge = pd.merge(scored, sentiment, left_on=subset, right_on=subset)
        merge = merge[['ICS GPA', variable]]
        merge = merge.dropna()
        return merge

    lw = 0.5
    variable = 's1_flesch_score'
    merge = make_merge_score_nlp(scored, variable)
    ax1 = sns.regplot(x='ICS GPA', y=variable, data=merge, ax=ax1, ci=99.9,
                     scatter_kws={'fc': 'w', 'ec': colors2[1]},
                      line_kws={'color': colors2[0], 'lw': lw})
    corr = np.round(np.corrcoef(merge['ICS GPA'], merge[variable])[0, 1], 2)
    ax1.add_artist(AnchoredText(f"Pearson's $r$ : {corr}", loc='lower left', prop=dict(fontsize=12)))

    variable = 's2_flesch_score'
    merge = make_merge_score_nlp(scored, variable)
    ax2 = sns.regplot(x='ICS GPA', y=variable, data=merge, ax=ax2, ci=99.9,
                     scatter_kws={'fc': 'w', 'ec': colors2[1]},
                    line_kws={'color': colors2[0], 'lw': lw})
    corr = np.round(np.corrcoef(merge['ICS GPA'], merge[variable])[0, 1], 2)
    ax2.add_artist(AnchoredText(f"Pearson's $r$ : {corr}", loc='lower left', prop=dict(fontsize=12)))

    variable = 's3_flesch_score'
    merge = make_merge_score_nlp(scored, variable)
    ax3 = sns.regplot(x='ICS GPA', y=variable, data=merge, ax=ax3, ci=99.9,
                      scatter_kws={'fc': 'w', 'ec': colors2[1]},
                      line_kws={'color': colors2[0], 'lw': lw})
    corr = np.round(np.corrcoef(merge['ICS GPA'], merge[variable])[0, 1], 2)
    ax3.add_artist(AnchoredText(f"Pearson's $r$ : {corr}", loc='lower left', prop=dict(fontsize=12)))

    variable = 's1_sentiment_score'
    merge = make_merge_score_nlp(scored, variable)
    ax4 = sns.regplot(x='ICS GPA', y=variable, data=merge, ax=ax4, ci=99.9,
                      scatter_kws={'fc': 'w', 'ec': colors2[0]},
                      line_kws={'color': colors2[1], 'lw': lw})
    corr = np.round(np.corrcoef(merge['ICS GPA'], merge[variable])[0, 1], 2)
    ax4.add_artist(AnchoredText(f"Pearson's $r$ : {corr}", loc='lower left', prop=dict(fontsize=12)))

    variable = 's2_sentiment_score'
    merge = make_merge_score_nlp(scored, variable)
    ax5 = sns.regplot(x='ICS GPA', y=variable, data=merge, ax=ax5, ci=99.9,
                      scatter_kws={'fc': 'w', 'ec': colors2[0]},
                      line_kws={'color': colors2[1], 'lw': lw})
    corr = np.round(np.corrcoef(merge['ICS GPA'], merge[variable])[0, 1], 2)
    ax5.add_artist(AnchoredText(f"Pearson's $r$ : {corr}", loc='lower left', prop=dict(fontsize=12)))

    variable = 's3_sentiment_score'
    merge = make_merge_score_nlp(scored, variable)
    ax6 = sns.regplot(x='ICS GPA', y=variable, data=merge, ax=ax6, ci=99.9,
                      scatter_kws={'fc': 'w', 'ec': colors2[0]},
                      line_kws={'color': colors2[1], 'lw': lw})
    corr = np.round(np.corrcoef(merge['ICS GPA'], merge[variable])[0, 1], 2)
    ax6.add_artist(AnchoredText(f"Pearson's $r$ : {corr}", loc='lower left', prop=dict(fontsize=12)))

    for ax in [ax1, ax2, ax3]:
        ax.set_xlabel('')
    ax1.set_ylabel('Flesch Score', fontsize=14)
    ax2.set_ylabel('')
    ax3.set_ylabel('')
    ax4.set_ylabel('Sentiment Score', fontsize=14)
    ax5.set_ylabel('')
    ax6.set_ylabel('')
    ax4.set_xlabel('ICS GPA', fontsize=14)
    ax5.set_xlabel('ICS GPA', fontsize=14)
    ax6.set_xlabel('ICS GPA', fontsize=14)

    ax1.set_title('A.', loc='left', fontsize=18)
    ax2.set_title('B.', loc='left', fontsize=18)
    ax3.set_title('C.', loc='left', fontsize=18)
    ax4.set_title('D.', loc='left', fontsize=18)
    ax5.set_title('E.', loc='left', fontsize=18)
    ax6.set_title('F.', loc='left', fontsize=18)

    for ax in [ax1, ax2, ax3, ax4, ax5, ax6]:
        ax.grid(which="both", linestyle='--', alpha=0.2)
        ax.yaxis.set_major_locator(plt.MaxNLocator(5))

    ax4.set_xticklabels(ax4.get_xticklabels(), rotation=0, fontsize=13)
    ax5.set_xticklabels(ax5.get_xticklabels(), rotation=0, fontsize=13)
    ax6.set_xticklabels(ax6.get_xticklabels(), rotation=0, fontsize=13)
    ax1.set_yticklabels(ax1.get_yticklabels(), rotation=0, fontsize=13)
    ax4.set_yticklabels(ax4.get_yticklabels(), rotation=0, fontsize=13)
    sns.despine()
    figure_name = 'score_read_vs_gpa'
    plt.savefig(os.path.join(figure_path, figure_name + '.pdf'),
                bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, figure_name + '.png'),
                bbox_inches='tight', dpi=400,
                facecolor='white', transparent=False)


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
    mpl.rcParams['font.family'] = 'Arial'
    colors5 = ['#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#084594']
    colors4 = ['#6baed6', '#4292c6', '#2171b5', '#084594']

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
    keyword_counter['all_grades']['STEM'] = find_keywords(non_shape, keyword_dict)
    keyword_counter['four_star'] = {}
    fourstar = df[fourstar_mask]
    shape_fourstar = fourstar[shape_mask][freetext].apply(lambda x: x.astype(str).str.lower())
    non_shape_fourstar = fourstar[~shape_mask][freetext].apply(lambda x: x.astype(str).str.lower())
    keyword_counter['four_star']['SHAPE'] = find_keywords(shape_fourstar, keyword_dict)
    keyword_counter['four_star']['STEM'] = find_keywords(non_shape_fourstar, keyword_dict)

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
    print("Corr(GPA,  FTE) for STEM is: ",
          round(scored[~shape_mask]['ICS_GPA'].corr(df['fte']), 3))
    print("Corr(GPA,  FTE) for SHAPE is: ",
          round(scored[shape_mask]['ICS_GPA'].corr(df['fte']), 3))
    print("Corr(GPA, Total Income) for all ICS is: ",
          round(scored['ICS_GPA'].corr(df['tot_income']), 3))
    print("Corr(GPA, Total Income) for STEM is: ",
          round(scored[~shape_mask]['ICS_GPA'].corr(df['tot_income']), 3))
    print("Corr(GPA, Total Income) for SHAPE is: ",
          round(scored[shape_mask]['ICS_GPA'].corr(df['tot_income']), 3))
    print("Corr(GPA, Number Degrees) for all ICS is: ",
          round(scored['ICS_GPA'].corr(df['num_doc_degrees_total']), 3))
    print('Mean GPA is ',
          round(scored['ICS_GPA'].mean(), 2))
    print('Mean GPA for STEM is ',
          round(scored[~shape_mask]['ICS_GPA'].mean(), 3))
    print('Mean GPA for SHAPE is ',
          round(scored[shape_mask]['ICS_GPA'].mean(), 3))
    print('Mean GPA for STEM (FTE>=100) is ',
          round(scored[~shape_mask & (scored['fte']>=100)]['ICS_GPA'].mean(), 3))
    print('Mean GPA for SHAPE (FTE>=100) is ',
          round(scored[shape_mask & (scored['fte']>=100)]['ICS_GPA'].mean(), 3))
    print('Mean GPA for STEM (50<=FTE) is ',
          round(scored[~shape_mask & (scored['fte']<=50)]['ICS_GPA'].mean(), 3))
    print('Mean GPA for SHAPE (50<FTE) is ',
          round(scored[shape_mask & (scored['fte']<=50)]['ICS_GPA'].mean(), 3))
    print('Mean GPA for STEM (1 ICS submitted) is ',
          round(scored[~shape_mask & (scored['size']==1)]['ICS_GPA'].mean(), 3))
    print('Mean GPA for SHAPE (1 ICS submitted) is ',
          round(scored[shape_mask & (scored['size']==1)]['ICS_GPA'].mean(), 3))
    print('Mean GPA for STEM (>1 ICS submitted) is ',
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
                               label=r'STEM', linewidth=0, markersize=10),
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
    fig = plt.figure(figsize=(12, 6))
    gs = gridspec.GridSpec(2, 2)
    mpl.rcParams['font.family'] = 'Arial'
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

    print(f'STEM ICS GPA mean: ',
          round(df_nonshape['ICS_GPA'].mean(), 2))
    print(f'SHAPE ICS GPA mean: ',
          round(df_shape['ICS_GPA'].mean(),2 ))

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
                               label=r'STEM', linewidth=2,
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
    plt.savefig(os.path.join(figure_path, 'ics_gpa.png'),
                bbox_inches='tight', dpi=800)
    df.to_csv(os.path.join(out_path, 'department_gpa.csv'), index=False)


def draw_brace(ax, xspan, yminn,text):
    """Draws an annotated brace on the axes."""
    xmin, xmax = xspan
    xspan = xmax - xmin
    ax_xmin, ax_xmax = ax.get_xlim()
    xax_span = ax_xmax - ax_xmin
    ymin, ymax = ax.get_ylim()
    yspan = ymax - ymin
    resolution = int(xspan/xax_span*100)*2+1
    beta = 300./xax_span
    x = np.linspace(xmin, xmax, resolution)
    x_half = x[:resolution//2+1]
    y_half_brace = (1/(1.+np.exp(-beta*(x_half-x_half[0])))
                    + 1/(1.+np.exp(-beta*(x_half-x_half[-1]))))
    y = np.concatenate((y_half_brace, y_half_brace[-2::-1]))
    y = yminn + (.05*y - .01)*yspan
    ax.autoscale(False)
    ax.plot(x, y, color='black', lw=1)
    ax.text((xmax+xmin)/2., yminn+(yminn/20) +.07*yspan,
            text, ha='center', va='bottom', fontsize=12)


def plot_metrics_shape(cited_by_uoa, altm_by_uoa, ratio_by_uoa, paper_panels, figure_path):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(17, 9), sharex='all')

    cited_by_uoa = pd.DataFrame(cited_by_uoa)
    altm_by_uoa = pd.DataFrame(altm_by_uoa)
    ratio_by_uoa = pd.DataFrame(ratio_by_uoa)

    cited_by_uoa = cited_by_uoa[(cited_by_uoa.index==4) | (cited_by_uoa.index>13)]
    altm_by_uoa = altm_by_uoa[(altm_by_uoa.index==4) | (altm_by_uoa.index>13)]
    ratio_by_uoa = ratio_by_uoa[(ratio_by_uoa.index==4) | (ratio_by_uoa.index>13)]

    cited_by_uoa.plot(kind='bar', ax=ax1, ec='k', legend=False)
    altm_by_uoa.plot(kind='bar', ax=ax2, ec='k', legend=False)
    ratio_by_uoa.plot(kind='bar', ax=ax3, ec='k', legend=False)
    colors2 = ['#850101', '#001c54', '#E89818']
    plt.tight_layout()
    ax3.set_xticklabels(ax3.get_xticklabels(), rotation=0, fontsize=14)
    ax3.set_xlabel('Unit of Assessment Number', fontsize=20)
    for ax in [ax1, ax2, ax3]:
        ax.get_children()[0].set_color(colors2[0])
        ax.get_children()[0].set_edgecolor('k')
        counter = 1
        for uoa in [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                    24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]:
            if uoa < 26:
                ax.get_children()[counter].set_color(colors2[1])
            else:
                ax.get_children()[counter].set_color(colors2[2])
            ax.get_children()[counter].set_edgecolor('k')
            counter += 1
    legend_elements = [Patch(facecolor=colors2[0], edgecolor='k',
                             label=r'UoA 4', alpha=0.7),
                       Patch(facecolor=colors2[1], edgecolor='k',
                             label=r'STEM', alpha=0.7),
                       Patch(facecolor=colors2[2], edgecolor='k',
                             label=r'SHAPE', alpha=0.7)]
    for ax in [ax3]:
        ax.legend(handles=legend_elements,
                  frameon=True,
                  fontsize=12, framealpha=1, facecolor='w',
                  edgecolor=(0, 0, 0, 1), ncol=1,
                  loc = 'center right'
                  )
    ax1.set_title('A.', loc='left', fontsize=18)
    ax2.set_title('B.', loc='left', fontsize=18)
    ax3.set_title('C.', loc='left', fontsize=18)

    ax1.set_ylabel('Av. Times Cited', fontsize=17)
    ax2.set_ylabel('Av. Altmetric Score', fontsize=17)
    ax3.set_ylabel('Av. Relative Ratio', fontsize=17)
    ax1.set_ylim(0, 120)
    ax2.set_ylim(0, 120)
    ax3.set_ylim(0, 3.25)

    C_cited = paper_panels.at['C', 'Average Times Cited']
    D_cited = paper_panels.at['D', 'Average Times Cited']
    C_altm = paper_panels.at['C', 'Average Altmetric']
    D_altm = paper_panels.at['D', 'Average Altmetric']
    C_ratio = paper_panels.at['C', 'Relative Ratio']
    D_ratio = paper_panels.at['D', 'Relative Ratio']

    draw_brace(ax1, (1, 14), 100, 'Panel C: ' + str(round(C_cited, 2)))
    draw_brace(ax1, (14, 21), 100, 'Panel D: ' + str(round(D_cited, 2)))
    draw_brace(ax2, (1, 14), 100, 'Panel C: ' + str(round(C_altm, 2)))
    draw_brace(ax2, (14, 21), 100, 'Panel D: ' + str(round(D_altm, 2)))
    draw_brace(ax3, (1, 14), 2.5, 'Panel C: ' + str(round(C_ratio, 2)))
    draw_brace(ax3, (14, 21), 2.5, 'Panel D: ' + str(round(D_ratio, 2)))

    plt.tight_layout()
    sns.despine()
    filename = 'altmetrics_and_citations_shape'
    plt.savefig(os.path.join(figure_path, filename + '.pdf'),
                bbox_inches = 'tight')
    plt.savefig(os.path.join(figure_path, filename + '.png'),
                bbox_inches = 'tight',
                dpi=400, facecolor='white', transparent=False)


def plot_metrics_all(cited_by_uoa, altm_by_uoa, ratio_by_uoa, paper_panels, fig_path):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(16, 9), sharex='all')
    cited_by_uoa.plot(kind='bar', ax=ax1, ec='k')
    altm_by_uoa.plot(kind='bar', ax=ax2, ec='k')
    ratio_by_uoa.plot(kind='bar', ax=ax3, ec='k')
    colors2 = ['#001c54', '#E89818']
    plt.tight_layout()
    ax3.set_xticklabels(ax3.get_xticklabels(), rotation=0, fontsize=14)
    ax3.set_xlabel('Unit of Assessment Number', fontsize=20)
    for ax in [ax1, ax2, ax3]:
        for uoa in range(0, 13):
            ax.get_children()[uoa].set_color(colors2[0])
            ax.get_children()[uoa].set_edgecolor('k')
            ax.get_children()[3].set_color(colors2[1])
            ax.get_children()[3].set_edgecolor('k')
        for uoa in range(13, 34):
            ax.get_children()[uoa].set_color(colors2[1])
            ax.get_children()[uoa].set_edgecolor('k')
    legend_elements = [Patch(facecolor=colors2[0], edgecolor='k',
                             label=r'STEM', alpha=0.7),
                       Patch(facecolor=colors2[1], edgecolor='k',
                             label=r'SHAPE', alpha=0.7)]
    for ax in [ax1, ax2, ax3]:
        ax.legend(handles=legend_elements,
                  frameon=True,
                  fontsize=15, framealpha=1, facecolor='w',
                  edgecolor=(0, 0, 0, 1), ncol=1,
                  loc='center right'
                  )
    ax1.set_title('A.', loc='left', fontsize=18)
    ax2.set_title('B.', loc='left', fontsize=18)
    ax3.set_title('C.', loc='left', fontsize=18)
    ax1.set_ylabel('Av. Times Cited.', fontsize=18)
    ax2.set_ylabel('Av. Altmetric Score', fontsize=18)
    ax3.set_ylabel('Av. Relative Ratio', fontsize=18)
    ax1.set_ylim(0, 475)
    ax2.set_ylim(0, 160)
    ax3.set_ylim(0, 8)
    A_cited = paper_panels.at['A', 'Average Times Cited']
    B_cited = paper_panels.at['B', 'Average Times Cited']
    C_cited = paper_panels.at['C', 'Average Times Cited']
    D_cited = paper_panels.at['D', 'Average Times Cited']
    A_altm = paper_panels.at['A', 'Average Altmetric']
    B_altm = paper_panels.at['B', 'Average Altmetric']
    C_altm = paper_panels.at['C', 'Average Altmetric']
    D_altm = paper_panels.at['D', 'Average Altmetric']
    A_ratio = paper_panels.at['A', 'Relative Ratio']
    B_ratio = paper_panels.at['B', 'Relative Ratio']
    C_ratio = paper_panels.at['C', 'Relative Ratio']
    D_ratio = paper_panels.at['D', 'Relative Ratio']
    draw_brace(ax1, (0, 6), 425, 'Panel A: ' + str(round(A_cited, 2)))
    draw_brace(ax1, (7, 12), 425, 'Panel B: ' + str(round(B_cited, 2)))
    draw_brace(ax1, (13, 24), 425, 'Panel C: ' + str(round(C_cited, 2)))
    draw_brace(ax1, (25, 35), 425, 'Panel D: ' + str(round(D_cited, 2)))
    draw_brace(ax2, (0, 6), 142.5, 'Panel A: ' + str(round(A_altm, 2)))
    draw_brace(ax2, (7, 12), 142.5, 'Panel B: ' + str(round(B_altm, 2)))
    draw_brace(ax2, (13, 24), 142.5, 'Panel C: ' + str(round(C_altm, 2)))
    draw_brace(ax2, (25, 35), 142.5, 'Panel D: ' + str(round(D_altm, 2)))

    draw_brace(ax3, (0, 6), 7.5, 'Panel A: ' + str(round(A_ratio, 2)))
    draw_brace(ax3, (7, 12), 7.5, 'Panel B: ' + str(round(B_ratio, 2)))
    draw_brace(ax3, (13, 24), 7.5, 'Panel C: ' + str(round(C_ratio, 2)))
    draw_brace(ax3, (25, 35), 7.5, 'Panel D: ' + str(round(D_ratio, 2)))

    plt.tight_layout()
    sns.despine()
    filename = 'altmetrics_and_citations'
    plt.savefig(os.path.join(fig_path, filename + '.pdf'),
                bbox_inches='tight')
    plt.savefig(os.path.join(fig_path, filename + '.png'),
                bbox_inches='tight',
                dpi=400, facecolor='white', transparent=False)



def plot_topic_keywords(figure_path):
    mpl.rcParams['font.family'] = 'Arial'
    mpl.rc('font', family='Arial')
    csfont = {'fontname': 'Arial'}
    hfont = {'fontname': 'Arial'}
    words = pd.read_csv(os.path.join(
        os.getcwd(), '..', '..', 'data',
        'topic_outputs', 'production_model',
        'BERT_keywords_full_text.csv'),
                        index_col = None,
                        converters={"0": ast.literal_eval,
                                    "1": ast.literal_eval,
                                    "2": ast.literal_eval,
                                    "3": ast.literal_eval,
                                    "4": ast.literal_eval})

    lookup = pd.read_csv(os.path.join(
        os.getcwd(), '..', '..', 'data',
        'topic_outputs', 'production_model',
        'ics_data_modelling_top_5_full_text.csv'),
                           index_col = None)

    color_list = ['#001c54', '#E89818',
                  '#001c54', '#E89818',
                  '#001c54', '#E89818',
                  '#001c54', '#E89818',
                  '#001c54', '#E89818',
                  '#001c54', '#E89818']
    topic_list = pd.DataFrame(lookup['topic_top1'].value_counts())[0:12].index.tolist()
    df = pd.DataFrame(lookup['topic_top1'].value_counts())[0:12]
    fig, ((ax1, ax2, ax3),
          (ax4, ax5, ax6),
          (ax7, ax8, ax9),
          (ax10, ax11, ax12)) = plt.subplots(4, 3, figsize=(14, 8.5))
    colour_counter = 0
    for topic, ax in zip(topic_list, [ax1, ax2, ax3, ax4,
                                      ax5, ax6, ax7, ax8,
                                      ax9, ax10, ax11, ax12]):
        mydict = {}
        for word in range(0, 5, 1):
            mydict[words.loc[topic, str(word)][0]] = words.loc[topic, str(word)][1]

        ax.set_axisbelow(True)
        ax.barh(y = list(mydict.keys()),
                width = list(mydict.values()), color=color_list[colour_counter],
                edgecolor='k', alpha=0.8)
        ax.invert_yaxis()
        ax.set_xlim(0, 0.475)
        ax.set_title('Topic: ' + str(topic) + ' (n=' + str(df.at[topic, 'topic_top1']) + ')')
        colour_counter += 1
    plt.tight_layout()
    sns.despine(left=True, bottom=True)
    ax1_ax9 = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9]
    ax10_ax12 = [ax10, ax11, ax12]
    for ax in ax1_ax9:
        ax.set_xticks([])
    for ax in ax10_ax12:
        ax.set_xlabel('Weight', fontsize=15)
        sns.despine(ax=ax, bottom=False, left=True)

    plt.savefig(os.path.join(figure_path, 'top_twelve_topics.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'top_twelve_topics.png'),
                dpi = 600, bbox_inches='tight')