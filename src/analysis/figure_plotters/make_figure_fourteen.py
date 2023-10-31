import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import geopandas as gpd
import pandas as pd
import os
import matplotlib.gridspec as gridspec
import seaborn as sns
import matplotlib.colors
import matplotlib.ticker as mtick
from helpers.figure_helpers import savefigures
mpl.rcParams['font.family'] = 'Graphik'
colors3 = ['#850101', '#001c54', '#E89818']


def make_geo_ax(df, ax, letter, leg_lab):
    country_list = []
    for index, row in df.iterrows():
        countries = row['countries_extracted']
        if countries is not np.nan:
            countries = countries.split(';')
            for country in countries:
                if ((country != 'TWN')
                        and (country != 'ESH')
                        and (country != 'GRL')
                        and (country != 'FLK')):
                    country_list.append(country.strip())
    df = pd.DataFrame(country_list)[0].value_counts()
    df = df.sort_values(ascending=False)
    df = df.reset_index()
    df = pd.DataFrame(df).rename({0: 'Count',
                                  'index': 'Country'},
                                 axis=1)
    SHAPEFILE_head = 'ne_110'
    SHAPEFILE_base = 'm_admin_0_countries_lakes.shp'
    geo_df = gpd.read_file(os.path.join(os.getcwd(),
                                        '..', '..',
                                        'data',
                                        'shapefiles',
                                        SHAPEFILE_head,
                                        SHAPEFILE_head + SHAPEFILE_base))
    geo_df = geo_df[['ADMIN', 'ADM0_A3', 'geometry']]
    geo_df.columns = ['country', 'country_code', 'geometry']
    geo_df = geo_df[geo_df['country'] != 'Taiwan']
    geo_df = geo_df[geo_df['country'] != 'Greenland']
    geo_df = geo_df[geo_df['country'] != 'Falkland Islands']
    geo_df = geo_df[geo_df['country'] != 'Puerto Rico']
    geo_df = geo_df.drop(geo_df.loc[geo_df['country'] == 'Antarctica'].index)
    geo_df = pd.merge(left=geo_df, right=df, how='left',
                      left_on='country_code', right_on='Country')
    geo_df = geo_df[geo_df['Count'].notnull()]
    col = 'Count'
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", [(63 / 255, 57 / 255, 95 / 255, 0.9),
                                                                                (69 / 255, 172 / 255, 52 / 255, 0.9),
                                                                                (255 / 255, 182 / 255, 0 / 255, 0.9)
                                                                    ])
    geo_df.plot(column=col, ax=ax, edgecolor='k', linewidth=0.25,
                cmap=cmap, scheme="natural_breaks",
                k=8, legend=True,
                legend_kwds={"loc": "lower left",
                             "frameon": True,
                             "edgecolor": 'k',
                             "ncols": 2,
                             "bbox_to_anchor": (0.05, 0.05),
                             "fmt": "{:.0f}",
                             "fontsize": 11,
                             "interval": True}
                )
    leg1 = ax.get_legend()
    leg1.set_title(leg_lab, prop={'size': 14})
    ax.set_xticks([])
    ax.set_xticklabels([])
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.set_title(letter, loc='left', x=0.025, fontsize=22, y=1.025)
#   @TODO this gets depricated in recent MPL versions
#    for legend_handle in ax.get_legend().legend_handles:
#        legend_handle.set_markeredgewidth(1)
#        legend_handle.set_markeredgecolor("black")
    sns.despine(left=True, top=True, bottom=True, right=True)
    return geo_df


def make_figure_fourteen():
    print('\n******************************************************')
    print('***************** Making Figure 14! ********************')
    print('********************************************************')
    colors = [(63 / 255, 57 / 255, 95 / 255, 0.9),
              (69 / 255, 172 / 255, 52 / 255, 0.9),
              (255 / 255, 182 / 255, 0 / 255, 0.9)]
    df = pd.read_csv(os.path.join(os.getcwd(),
                                  '..',
                                  '..',
                                  'data',
                                  'final',
                                  'enhanced_ref_data.csv'),
                     index_col=0)
    df['Unit of assessment number'] = df['Unit of assessment number'].astype(int)
    fig = plt.figure(figsize=(24, 21))
    spec = gridspec.GridSpec(ncols=36, nrows=30, figure=fig)
    ax1 = fig.add_subplot(spec[0:10, 0:30])
    ax2 = fig.add_subplot(spec[10:20, 0:30])
    ax3 = fig.add_subplot(spec[20:30, 0:30])
    ax4 = fig.add_subplot(spec[0:9, 29:36])
    ax5 = fig.add_subplot(spec[10:19, 29:36])
    ax6 = fig.add_subplot(spec[20:29, 29:36])
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
    UoA4 = make_geo_ax(df[df['Unit of assessment number'] == 4.0],
                       ax1, 'A.',
                       'Mentioned as Beneficiary\n           (UoA 4)        ')
    mpl.rcParams['font.family'] = 'Graphik'
    print('UoA4 countries listed: ',
          len(UoA4[UoA4['Count'] > 0]))
    UoA4 = UoA4.sort_values(by='Count',
                            ascending=False)[0:10].sort_values(ascending=True,
                                                               by='Count')
    PanelC = make_geo_ax(df[df['Main panel'] == 'C'],
                         ax2, 'C.',
                         'Mentioned as Beneficiary\n            (Panel C)       ')
    print('PanelC countries listed: ',
          len(PanelC[PanelC['Count'] > 0]))
    PanelC = PanelC.sort_values(by='Count', ascending=False)[0:10].sort_values(ascending=True,
                                                                               by='Count')
    PanelD = make_geo_ax(df[df['Main panel'] == 'D'],
                         ax3, 'E.',
                         'Mentioned as Beneficiary\n            (Panel D)        ')
    print('PanelD countries listed: ',
          len(PanelD[PanelD['Count'] > 0]))
    PanelD = PanelD.sort_values(by='Count',
                                ascending=False)[0:10].sort_values(ascending=True,
                                                                   by='Count')
    UoA4['Count'] = (UoA4['Count'] / UoA4['Count'].sum()) * 100
    norm = plt.Normalize(0, UoA4['Count'].max())
    colors = cmap(norm(UoA4['Count']))
    bar_container_uoa4 = ax4.barh(y=UoA4['Country'],
                                  width=UoA4['Count'],
                                  color=colors,
                                  edgecolor='k',
                                  alpha=1)

    PanelC['Count'] = (PanelC['Count'] / PanelC['Count'].sum()) * 100
    norm = plt.Normalize(0, PanelC['Count'].max())
    colors = cmap(norm(PanelC['Count']))
    bar_container_panelc = ax5.barh(y=PanelC['Country'],
                                    width=PanelC['Count'],
                                    color=colors,
                                    edgecolor='k',
                                    alpha=1)

    PanelD['Count'] = (PanelD['Count'] / PanelD['Count'].sum()) * 100
    norm = plt.Normalize(0,
                         PanelD['Count'].max())
    colors = cmap(norm(PanelD['Count']))
    bar_container_paneld = ax6.barh(y=PanelD['Country'],
                                    width=PanelD['Count'],
                                    color=colors,
                                    edgecolor='k',
                                    alpha=1)
    fmt = '%.0f%%'
    xticks = mtick.FormatStrFormatter(fmt)
    ax4.xaxis.set_major_formatter(xticks)
    ax5.xaxis.set_major_formatter(xticks)
    ax6.xaxis.set_major_formatter(xticks)

    fmt = '%.2f%%'
    ax4.bar_label(bar_container_uoa4,
                  fmt=fmt,
                  padding=5,
                  fontsize=15)
    ax5.bar_label(bar_container_panelc,
                  fmt=fmt,
                  padding=5,
                  fontsize=15)
    ax6.bar_label(bar_container_paneld,
                  fmt=fmt,
                  padding=5,
                  fontsize=15)
    sns.despine(ax=ax4,
                offset=5,
                trim=True)
    sns.despine(ax=ax5,
                offset=5,
                trim=True)
    sns.despine(ax=ax6,
                offset=5,
                trim=True)
    sns.despine(left=True, top=True, bottom=True, right=True, ax=ax1)
    sns.despine(left=True, top=True, bottom=True, right=True, ax=ax2)
    sns.despine(left=True, top=True, bottom=True, right=True, ax=ax3)
    sns.despine(left=True, top=True, bottom=True, right=True, ax=ax4)
    fig.subplots_adjust(hspace=2)
    fig.subplots_adjust(wspace=-.1)
    ax4.set_xlabel('Unit of Assessment 4', fontsize=16)
    ax5.set_xlabel('Panel C', fontsize=16)
    ax6.set_xlabel('Panel D', fontsize=16)
    for ax in [ax4, ax5, ax6]:
        ax.set_ylabel('', fontsize=16)
        ax.tick_params(axis='both', which='major', labelsize=15)
    ax4.set_title('B.', loc='left', x=-0.05, fontsize=22, y=1.025)
    ax5.set_title('D.', loc='left', x=-0.05, fontsize=22, y=1.025)
    ax6.set_title('F.', loc='left', x=-0.05, fontsize=22, y=1.025)
    file_name = 'figure_14'
    figure_path = os.path.join(os.getcwd(), '..', '..', 'figures')
    savefigures(plt, figure_path, file_name)

    df_global = df[df['region_extracted'].str.contains('global', na=False)]
    print('The number of global in UoA 4:',
          len(df_global[df_global['Unit of assessment number'] == 4.0]))
    print('The number of global in Panel C:',
          len(df_global[df_global['Main panel'] == 'C']))
    print('The number of global in Panel D:',
          len(df_global[df_global['Main panel'] == 'D']))

    print('The percent of global in UoA 4:',
          len(df_global[df_global['Unit of assessment number'] == 4.0]) /
          len(df[df['Unit of assessment number'] == 4.0])*100)
    print('The percent of global in Panel C:',
          len(df_global[df_global['Main panel'] == 'C']) /
          len(df[df['Main panel'] == 'C'])*100)
    print('The percent of global in Panel D:',
          len(df_global[df_global['Main panel'] == 'D']) /
          len(df[df['Main panel'] == 'D'])*100)