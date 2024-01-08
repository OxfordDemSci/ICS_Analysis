import os
import re
import numpy as np
import pandas as pd
import seaborn as sns
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import gender_guesser.detector as gender
import matplotlib.gridspec as gridspec
import matplotlib.colors
from PIL import Image
from .figure_helpers import savefigures
from mne_connectivity.viz import plot_connectivity_circle
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

d = gender.Detector()
import matplotlib as mpl
mpl.rcParams['font.family'] = 'Graphik'
plt.rcParams["font.family"] = 'Graphik'
plt.rcParams["axes.labelweight"] = "light"
plt.rcParams["font.weight"] = "light"
#matplotlib.use('Agg')

# @TODO this is not a good colour 3.
ba_rgb2 = ['#41558c', '#E89818', '#CF202A']

#ba_rgb2 = [(0 / 255, 160 / 255, 223 / 255, 0.65),
#           (255 / 255, 182 / 255, 0 / 255, 0.65),
#           (254 / 255, 59 / 255, 31 / 255, 0.65)]

#ba_rgb1 = [(0 / 255, 160 / 255, 223 / 255, 0.45),
#           (255 / 255, 182 / 255, 0 / 255, 0.45),
#           (254 / 255, 59 / 255, 31 / 255, 0.45)]


def make_descriptives(df, paper_level, cluster):
    print('\n*****************************************************')
    print('******* Descriptives for Grand Impact Theme {} *****************'.format(str(cluster)))
    print('*****************************************************\n')
    paper_level = filter_cluster(paper_level, cluster)
    df = filter_cluster(df, cluster)
    df_counts = df['Unit of assessment number'].value_counts()
    mystr = 'Distribution Across UoAs: '
    print('Number of ICS: ', len(df))
    for value, index in zip(df_counts, df_counts.index):
        mystr = mystr + 'UoA ' + str(int(index)) +\
                ' (' + str(value) + ', ' +\
                str(round(value/len(df)*100, 2)) + '%), '
    mystr = mystr[:-2]
    print(mystr)
    funder_list = []

    pattern = r'\[[^\]]*\]'
    for index, row in df.iterrows():
        funders = row['funders_extracted']
        if funders is not np.nan:
            funders = re.sub(pattern, '', funders)
            funders = funders.split(';')
            for funder in funders:
                funder_list.append(funder.strip())
    funder_count = pd.DataFrame(funder_list)[0].value_counts()
    funder_count = funder_count.sort_values(ascending=False)
    funder_count = funder_count[0:7].sort_values(ascending=False)
    print('The most frequent funder is: ' + str(funder_count.index[0]) +\
          '('+str(funder_count[0]) + '). The second most is: ' +\
          str(funder_count.index[1]) + '('+str(funder_count[1]) + ').')

    country_list = []
    for index, row in df.iterrows():
        countries = row['countries_extracted']
        if countries is not np.nan:
            countries = countries.split(';')
            for country in countries:
                country_list.append(country.strip())
    country_count = pd.DataFrame(country_list)[0].value_counts()
    country_count = country_count.sort_values(ascending=False)
    country_count = country_count.reset_index()
    country_count = pd.DataFrame(country_count)
    country_count = country_count.rename({0: 'Country'}, axis=1)
    country_count = country_count.rename({'count': 'Count'}, axis=1)
    print(country_count)
    print('The most frequent country beneficiary is : ' + str(country_count['Country'][0]) +
          '('+str(country_count['Count'][0]) + '). The second most is: ' +
           str(country_count['Country'][1]) + '('+str(country_count['Count'][1]) + ').' +
           ' and the third is ' + str(country_count['Country'][2]) + '('+str(country_count['Count'][2]) + ').')
    country_list = []
    for index, row in df.iterrows():
        countries = row['countries_extracted']
        if countries is not np.nan:
            countries = countries.split(';')
            for country in countries:
                country_list.append(country.strip())
    country_count = pd.DataFrame(country_list)[0].value_counts()
    country_count = country_count.sort_values(ascending=False)
    country_count = country_count.reset_index()
#   country_count = pd.DataFrame(country_count).rename({0: 'Count',
#                                                       'index': 'Region'},
#                                                       axis=1)
#
#    print('The most frequent regional beneficiary is : ' + str(country_count['region_clean'][0]) +
#          ' ('+str(country_count['Count'][0]) + '). The second most is: ' +
#           str(country_count['region_clean'][1]) + ' ('+str(country_count['Count'][1]) + ').')

    df_for, for_list = make_and_clean_for(paper_level)

    print('The five most common interdisciplinarities are: ' +
          str(for_list.index[0][0]) + ' (' + str(for_list[0]) + '), ' +
          str(for_list.index[1][0]) + ' (' + str(for_list[1]) + '), ' +
          str(for_list.index[2][0]) + ' (' + str(for_list[2]) + '), ' +
          str(for_list.index[3][0]) + ' (' + str(for_list[3]) + '), ' +
          str(for_list.index[4][0]) + ' (' + str(for_list[4]) + ').')
    type_count = paper_level['type'].value_counts()/len(paper_level)*100
    type_count = type_count.round(2)

    if len(type_count.index)>5:

        print('The most common types of underpinning research are: ' +
              str(type_count.index[0]) + ' (' + str(type_count[0]) + '%), ' +
              str(type_count.index[1]) + ' (' + str(type_count[1]) + '%), ' +
              str(type_count.index[2]) + ' (' + str(type_count[2]) + '%), ' +
              str(type_count.index[3]) + ' (' + str(type_count[3]) + '%), ' +
              str(type_count.index[4]) + ' (' + str(type_count[4]) + '%), ' +
              str(type_count.index[5]) + ' (' + str(type_count[5]) + '%).')

    elif len(type_count.index)>4:

        print('The most common types of underpinning research are: ' +
              str(type_count.index[0]) + ' (' + str(type_count[0]) + '%), ' +
              str(type_count.index[1]) + ' (' + str(type_count[1]) + '%), ' +
              str(type_count.index[2]) + ' (' + str(type_count[2]) + '%), ' +
              str(type_count.index[3]) + ' (' + str(type_count[3]) + '%), ' +
              str(type_count.index[4]) + ' (' + str(type_count[4]) + '%).')

    else:

        print('The most common types of underpinning research are: ' +
              str(type_count.index[0]) + ' (' + str(type_count[0]) + '%), ' +
              str(type_count.index[1]) + ' (' + str(type_count[1]) + '%), ' +
              str(type_count.index[2]) + ' (' + str(type_count[2]) + '%), ' +
              str(type_count.index[3]) + ' (' + str(type_count[3]) + '%), ')

    from wordcloud import STOPWORDS
    file = open(os.path.join(os.getcwd(),
                             '..',
                             '..',
                             'data',
                             'manual',
                             'stopwords',
                             'custom_stopwords.txt'), "r")
    data = file.read()
    data_into_list = data.replace('\n', '.').split(".")
    file.close()
    STOPWORDS = list(STOPWORDS)
    STOPWORDS.extend(data_into_list)
    stopwords = set(STOPWORDS)
    concept_holder = pd.DataFrame(columns=['score'])
    for row in paper_level['concepts'].to_list():
        temp_concept = re.findall(r"'concept': '(.*?)'", row)
        temp_score = re.findall(r"'relevance': (.*?)}", row)
        for concept, score in zip(temp_concept, temp_score):
            if concept not in stopwords:
                if concept in concept_holder.index:
                    concept_holder.at[concept, 'score'] = concept_holder.loc[concept, 'score'] + float(score)
                else:
                    concept_holder.at[concept, 'score'] = float(score)
    concept_holder = concept_holder.sort_values(by='score', ascending=False)
    print('The ten commonly seen concepts are: ' +
          str(concept_holder.index[0]) + ', ' +
          str(concept_holder.index[1]) + ', ' +
          str(concept_holder.index[2]) + ', ' +
          str(concept_holder.index[3]) + ', ' +
          str(concept_holder.index[4]) + ', ' +
          str(concept_holder.index[5]) + ', ' +
          str(concept_holder.index[6]) + ', ' +
          str(concept_holder.index[7]) + ', ' +
          str(concept_holder.index[8]) + ', ' +
          str(concept_holder.index[9]) + '.')

    print('The underpinning research with the highest Altmetric score:')
    print('Title: {}'.format(paper_level.loc[paper_level['Altmetric'].idxmax()]['preferred']))
    print('DOI: {}'.format(paper_level.loc[paper_level['Altmetric'].idxmax()]['doi']))
    print('Altmetric: {}'.format(paper_level.loc[paper_level['Altmetric'].idxmax()]['Altmetric']))

    print('The underpinning research with the highest number of citations:')
    print('Title: {}'.format(paper_level.loc[paper_level['Times Cited'].idxmax()]['preferred']))
    print('DOI: {}'.format(paper_level.loc[paper_level['Times Cited'].idxmax()]['doi']))
    print('Times Cited: {}'.format(paper_level.loc[paper_level['Times Cited'].idxmax()]['Times Cited']))

    print('The underpinning research with the highest relative ratio of citations:')
    print('Title: {}'.format(paper_level.loc[paper_level['Relative Citation Ratio'].idxmax()]['preferred']))
    print('DOI: {}'.format(paper_level.loc[paper_level['Relative Citation Ratio'].idxmax()]['doi']))
    print('Relative Citation Ratio: {}'.format(paper_level.loc[paper_level['Relative Citation Ratio'].idxmax()]['Relative Citation Ratio']))


    print('The average Altmetric score is: ', paper_level['Altmetric'].mean())
    print('The average citation count is: ', paper_level['Times Cited'].mean())
    print('The average relative citation ratio is: ', paper_level['Relative Citation Ratio'].mean())


def make_author_level(paper_level):
    author_level=pd.DataFrame(columns=['Panel', 'UoA', 'ICS_uid',
                                       'pub_uid', 'first_name',
                                       'gender'])
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
    author_level['female'] = np.where(author_level['gender'] == 'female',
                                      1,
                                      0)
    author_level['female'] = np.where(author_level['gender'] == 'mostly_female',
                                      1,
                                      author_level['female'])
    author_level = author_level[author_level['gender'] != 'unknown']
    author_level = author_level[author_level['gender'] != 'andy']
    return author_level


def make_geo_ax(country_count, ax, letter):
    country_list = []
    for index, row in country_count.iterrows():
        countries = row['countries_extracted']
        if countries is not np.nan:
            countries = countries.split(';')
            for country in countries:
                country_list.append(country.strip())
    country_count = pd.DataFrame(country_list)[0].value_counts()
    country_count = country_count.sort_values(ascending=False)
    country_count = country_count.reset_index()
    country_count = pd.DataFrame(country_count).rename({0: 'Count',
                                                        'index': 'Country'},
                                                       axis=1)
    SHAPEFILE_head = 'ne_110'
    SHAPEFILE_base = 'm_admin_0_countries_lakes.shp'
    geo_df = gpd.read_file(os.path.join(os.getcwd(),
                                        '..',
                                        '..',
                                        'assets',
                                        'shapefiles',
                                        SHAPEFILE_head,
                                        SHAPEFILE_head + SHAPEFILE_base))
    geo_df = geo_df[['ADMIN', 'ADM0_A3', 'geometry']]
    geo_df.columns = ['country', 'country_code', 'geometry']
    country_count = country_count.rename({'Count': 'Country'}, axis=1)
    country_count = country_count.rename({'count': 'Count'}, axis=1)
    country_count = country_count[country_count['Country'] != 'TWN']
    country_count = country_count[country_count['Country'] != 'ESH']
    geo_df = geo_df.drop(geo_df.loc[geo_df['country'] == 'Antarctica'].index)
    geo_df = pd.merge(left=geo_df, right=country_count, how='left',
                      left_on='country_code', right_on='Country')
    geo_df = geo_df[geo_df['country'] != 'Western Sahara']
    geo_df = geo_df[geo_df['country'] != 'Taiwan']
    geo_df = geo_df[geo_df['country'] != 'Greenland']
    geo_df = geo_df[geo_df['country'] != 'Falkland Islands']
    geo_df = geo_df[geo_df['country'] != 'Puerto Rico']
    geo_df = geo_df[geo_df['Count'].notnull()]
    col = 'Count'
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", [(63 / 255, 57 / 255, 95 / 255, 0.9),
                                                                    (69 / 255, 172 / 255, 52 / 255, 0.9),
                                                                    (255 / 255, 182 / 255, 0 / 255, 0.9)
                                                                    ])
    geo_df.plot(column=col, ax=ax, edgecolor='k', linewidth=0.25,
                cmap=cmap, scheme="natural_breaks",
                k=5, legend=True,
                legend_kwds={"loc": "lower left",
                             "frameon": True,
                             "edgecolor": 'k',
                             "ncols": 1,
                             #"bbox_to_anchor": (-0.04, 0.1),
                             "fmt": "{:.0f}",
                             "fontsize": 11,
                             "interval": True}
                )
    leg1 = ax.get_legend()
    leg1.set_title("Beneficiaries", prop={'size': 12})
    ax.set_xticks([])
    ax.set_xticklabels([])
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.set_title(letter, loc='left', x=-0.015, fontsize=18, y=0.965, fontweight='bold')

    for legend_handle in ax.get_legend().legend_handles:
        legend_handle.set_markeredgecolor('black')
        legend_handle.set_markeredgewidth(0.75)

    sns.despine(ax=ax, left=True, bottom=True)
    return ax


def make_wc_ax(paper_level, ax, letter):
    from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
    mask = np.array(Image.open(os.path.join(os.getcwd(), '..',
                                            '..', 'assets',
                                            'wordcloud_mask.png')))
    image_colors = ImageColorGenerator(mask)
    file = open(os.path.join(os.getcwd(),
                             '..',
                             '..',
                             'data',
                             'manual',
                             'stopwords',
                             'custom_stopwords.txt'),
                'r')
    data = file.read()
    data_into_list = data.replace('\n',
                                  '.').split(".")
    file.close()
    STOPWORDS = list(STOPWORDS)
    STOPWORDS.extend(data_into_list)
    stopwords = set(STOPWORDS)
    concept_holder = pd.DataFrame(columns=['score'])
    for row in paper_level['concepts'].to_list():
        temp_concept = re.findall(r"'concept': '(.*?)'", row)
        temp_score = re.findall(r"'relevance': (.*?)}", row)
        for concept, score in zip(temp_concept, temp_score):
            if concept not in stopwords:
                if concept in concept_holder.index:
                    concept_holder.at[concept,
                    'score'] = concept_holder.loc[concept,
                    'score'] + float(score)
                else:
                    concept_holder.at[concept, 'score'] = float(score)
    concept_dict = concept_holder.to_dict()['score']
    wc = WordCloud(collocations=True,
                   mask=mask, max_words=1000,
                   stopwords=stopwords,
                   normalize_plurals=True,
                   regexp=r"\w[\w' ]+",
                   background_color='white').generate_from_frequencies(concept_dict)
    ax.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
    ax.set_xticks([])
    ax.set_xticklabels([])
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.set_title(letter, loc='left', x=0.075, fontsize=18, y=1.0125, fontweight='bold')
    sns.despine(ax=ax, left=True, bottom=True)


def make_inter_ax(df_for, ax, letter):
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("",
                                                               ['white', '#41558c', '#E89818', '#CF202A']
                                                               )
    plot_connectivity_circle(df_for.replace(0, np.nan).to_numpy(),
                             list(df_for.index), padding=5,
                             facecolor='white', node_width=12,
                             textcolor='black', node_linewidth=1,
                             linewidth=5, colormap=cmap, vmin=None,
                             vmax=None, colorbar=False,
                             title=letter,
                             fontsize_title=20,
                             node_colors=['#E89818'], colorbar_size=0.75,
                             #colorbar_pos=(.4, 0.5),
                             ax=ax,
                             fontsize_names=14, fontsize_colorbar=13)
    ax.set_xticks([])
    ax.set_xticklabels([])
    ax.set_yticks([])
    ax.set_yticklabels([])
    return ax


def make_funder_ax(df, df1, ax, cluster, letter, letter2):
    funder_df = make_funder_df(df)
    edgecolors = ['k', 'w'] * 8
    ax.barh(width=funder_df['index'], y=funder_df[0],
            height=1, edgecolor=edgecolors, color=ba_rgb2[0])
    ax.set_ylabel('Percentage of Named Funding', fontsize=16)
    ax.set_ylim(-0.5, 12.65)
    for i, yi in enumerate(funder_df[0]):
        if (i % 2) != 0:
            mystr = funder_df[0].to_list()[i].split(' [')[0].replace('_temp', '')
            ax.text(0, yi, mystr, horizontalalignment='left',
                    verticalalignment='center', fontsize=13)
        else:
            ax.text(funder_df['index'].to_list()[i]+(ax.get_xlim()[1]/85),
                    yi,
                    "{:.2%}".format(funder_df['index'].to_list()[i] / len(df)),
                    fontsize=13, horizontalalignment='left',
                    verticalalignment='center',
                    color='k')
    ax.set_xlim(ax.get_xlim()[0], ax.get_xlim()[1]+(ax.get_xlim()[1]/10))
    ax.set_xticks([])
    ax.set_xticklabels([])
    ax.set_yticks([])
    ax.set_yticklabels([])
    sns.despine(ax=ax, left=True, bottom=True)
    ax.set_title(letter, loc='left', x=-0.065, fontsize=18, y=1.025, fontweight='bold')
    axin2 = inset_axes(ax, width="100%", height="100%", loc='lower right',
                       bbox_to_anchor=(0.825, 0.02, .3, .3),
                       bbox_transform=ax.transAxes)
    fem = df1['female'].sum() / len(df1['female']) * 100
    men = 100 - fem
    bar_container = axin2.bar(x=['Female', 'Male'], height=[fem, men],
                              color=[ba_rgb2[1], ba_rgb2[0]],
                              width=0.8, edgecolor='k')
    axin2.set_title(letter2, loc='left', x=-0.15, fontsize=18, y=1.075, fontweight='bold')
    axin2.tick_params(axis='both', which='major', labelsize=14)
    sns.despine(ax=axin2)
    axin2.set_ylabel('Gender of\nAuthors', fontsize=16)
    axin2.bar_label(bar_container,
                    fmt='%.2f%%', padding=0.05, fontsize=12)
    fmt = '%.0f%%'
    yticks = mtick.FormatStrFormatter(fmt)
    axin2.yaxis.set_major_formatter(yticks)
    return ax


def unpack_funder(funder):
    if funder == 'Department for Business, Energy and Industrial Strategy': funder = 'DBEIS'
    #if funder == 'ESRC': funder = 'Economic and Social Research Council'
    if funder == 'NHS': funder = 'National Health Service'
    if funder == 'WCT': funder = 'Wellcome Trust'
    if funder == 'WGOV': funder = 'Welsh Government'
#    if funder == 'AHRC': funder = 'Arts and Humanities Research Council'
    if funder == 'ACE': funder = 'Arts Council England'
    if funder == 'SGOV': funder = 'Scottish Government'
    if funder == 'UKGOV': funder = 'UK Government'
    if funder == 'MRC': funder = 'Medical Research Council'
#    if funder == 'EPSRC': funder = 'Engineering and Physical Sciences Research Council'
    if funder == 'MCC': funder = 'Millenium Challenge Corporation'
    if funder == 'BA': funder = 'British Academy'
    if funder == 'UKHO': funder = 'UKHO'
    if funder == 'THF': funder = 'The Health Foundation'
    if funder == 'SFC': funder = 'Scottish Funding Council'
    if funder == 'STFC': funder = 'Science and Technology Facilities Council'
    if funder == 'LHT': funder = 'Leverhulme Trust'
    if funder == 'LT': funder = 'Leverhulme Trust'
    if funder == 'AMR': funder = 'Action Medical Research'
    if funder == 'ARUK': funder = 'Arthritis Research UK'
    if funder == 'DEFRA': funder = 'Department for Environment, Food and Rural Affairs'
    if funder == 'BMGF': funder = 'Bill and Melinda Gates Foundation'
    if funder == 'NIHCR': funder = 'National Institute for Health and Care Research'
    if funder == 'RSOC': funder = 'Royal Society'
    if funder == 'RAE': funder = 'Royal Academy of Engineering'
    if funder == 'RENG': funder = 'Research England'
    if funder == 'PHE': funder = 'Public Health England'
    if funder == 'NUFF': funder = 'Nuffield Foundation'
    if funder == 'Department for International Development': funder = 'Dept. for Int. Dev.'
    if funder == 'Department for Work and Pensions': funder = 'DWP'
    if funder == 'Education Endowment Foundation': funder = 'Educ. Endow. Found.'
    if funder == 'NERC': funder = 'Natural Environment Research Council'
    if funder == 'NLHF': funder = 'National Lot. (Heritage)'
    if funder == 'BBSRC': funder = 'Biotechnology and Biological Sciences Research Council'
    if funder == 'WHO': funder = 'World Health Organization'
    if funder == 'EC': funder = 'European Commission'
    if funder == 'EU': funder = 'EU'
    if funder == 'EURC': funder = 'European Union'
    if funder == 'EUCO': funder = 'European Research Council'
    return funder

def make_funder_df(df):
    pattern = r'\[[^\]]*\]'
    funder_list = []
    for index, row in df.iterrows():
        funders = row['funders_extracted']
        if funders is not np.nan:
            funders = re.sub(pattern, '', funders)
            funders = funders.split(';')
            for funder in funders:
                funder = funder.strip()
                funder = unpack_funder(funder)
                funder_list.append(funder.strip())
    funder_count = pd.DataFrame(funder_list)[0].value_counts()
    funder_count = funder_count[funder_count.index.str.len() > 0]
    funder_count = funder_count.dropna()
    funder_count = funder_count.sort_values(ascending=False)
    funder_count = funder_count[0:7].sort_values(ascending=True)
    mylist = list(funder_count.index)
    temp = [ele + '_temp' for ele in list(funder_count.index)]
    mylist.extend(temp)
    funder_df = pd.DataFrame(mylist, list(funder_count.values) * 2)
    funder_df = funder_df.reset_index()
    funder_df = funder_df.sort_values(by=['index', 0])
    funder_df = funder_df.reset_index()
    funder_df.at[1, 'index'] = 0
    funder_df.at[3, 'index'] = 0
    funder_df.at[5, 'index'] = 0
    funder_df.at[7, 'index'] = 0
    funder_df.at[9, 'index'] = 0
    funder_df.at[11, 'index'] = 0
    funder_df.at[13, 'index'] = 0
    funder_df['index'] = funder_df['index'].astype(int)
    return funder_df


def filter_cluster(df, cluster_number):
    df = df[df['cluster_id'].notnull()]
    df = df[df['cluster_id'] == cluster_number]
    return df


def make_and_clean_for(paper_level):
    for_set = set()
    for index, row in paper_level.iterrows():
        paper_fors = row['category_for']
        if paper_fors is not np.nan:
            first_level = paper_fors.split('second_level')[0]
            for_set = for_set.union(set(re.findall(r"'name': '(.*?)'", first_level)))
    df_for = pd.DataFrame(0, columns=list(for_set), index=list(for_set))
    for_list = []
    for index, row in paper_level.iterrows():
        paper_fors = row['category_for']
        if paper_fors is not np.nan:
            first_level = paper_fors.split('second_level')[0]
            for_set_row = set(re.findall(r"'name': '(.*?)'", first_level))
            for_set = for_set.union(for_set_row)
            if len(for_set_row) > 1:
                for field1 in for_set_row:
                    for field2 in for_set_row:
                        if field1 != field2:
                            df_for.at[field1, field2] += 1
                            for_list.append(str(field1) + '; ' + str(field2))
    df_for = df_for.rename({'Information and Computing Sciences': 'IT'}, axis=0)
    df_for = df_for.rename({'Information and Computing Sciences': 'IT'}, axis=1)
    df_for = df_for.rename({'Built Environment and Design': 'Urban'}, axis=0)
    df_for = df_for.rename({'Built Environment and Design': 'Urban'}, axis=1)
    df_for = df_for.rename({'Biological Sciences': 'Biology'}, axis=0)
    df_for = df_for.rename({'Biological Sciences': 'Biology'}, axis=1)
    df_for = df_for.rename({'Health Sciences': 'Health'}, axis=0)
    df_for = df_for.rename({'Health Sciences': 'Health'}, axis=1)
    df_for = df_for.rename({'Language, Communication and Culture': 'Language'}, axis=0)
    df_for = df_for.rename({'Language, Communication and Culture': 'Language'}, axis=1)
    df_for = df_for.rename({'Earth Sciences': 'Earth'}, axis=0)
    df_for = df_for.rename({'Earth Sciences': 'Earth'}, axis=1)
    df_for = df_for.rename({'Physical Sciences': 'Physics'}, axis=0)
    df_for = df_for.rename({'Physical Sciences': 'Physics'}, axis=1)
    df_for = df_for.rename({'Chemical Sciences': 'Chem'}, axis=0)
    df_for = df_for.rename({'Chemical Sciences': 'Chem'}, axis=1)
    df_for = df_for.rename({'Economics': 'Econ'}, axis=1)
    df_for = df_for.rename({'Economics': 'Econ'}, axis=1)
    df_for = df_for.rename({'Biomedical and Clinical Sciences': 'Biomedical'}, axis=0)
    df_for = df_for.rename({'Biomedical and Clinical Sciences': 'Biomedical'}, axis=1)
    df_for = df_for.rename({'Agricultural, Veterinary and Food Sciences': 'Agriculture'}, axis=0)
    df_for = df_for.rename({'Agricultural, Veterinary and Food Sciences': 'Agriculture'}, axis=1)
    df_for = df_for.rename({'History, Heritage and Archaeology': 'History'}, axis=0)
    df_for = df_for.rename({'History, Heritage and Archaeology': 'History'}, axis=1)
    df_for = df_for.rename({'Law and Legal Studies': 'Law'}, axis=0)
    df_for = df_for.rename({'Law and Legal Studies': 'Law'}, axis=1)
    df_for = df_for.rename({'Environmental Sciences': 'Environmental'}, axis=0)
    df_for = df_for.rename({'Environmental Sciences': 'Environmental'}, axis=1)
    df_for = df_for.rename({'Law and Legal Studies': 'Law'}, axis=0)
    df_for = df_for.rename({'Law and Legal Studies': 'Law'}, axis=1)
    df_for = df_for.rename({'Creative Arts and Writing': 'Creative'}, axis=0)
    df_for = df_for.rename({'Creative Arts and Writing': 'Creative'}, axis=1)
    df_for = df_for.rename({'Commerce, Management, Tourism and Services': 'Tourism'}, axis=0)
    df_for = df_for.rename({'Commerce, Management, Tourism and Services': 'Tourism'}, axis=1)
    df_for = df_for.rename({'Mathematical Sciences': 'Mathematics'}, axis=0)
    df_for = df_for.rename({'Mathematical Sciences': 'Mathematics'}, axis=1)
    df_for = df_for.rename({'Philosophy and Religious Studies': 'Religion'}, axis=0)
    df_for = df_for.rename({'Philosophy and Religious Studies': 'Religion'}, axis=1)
    df_for = df_for.rename({'Human Society': 'Society'}, axis=0)
    df_for = df_for.rename({'Human Society': 'Society'}, axis=1)
    return df_for, pd.DataFrame(for_list).value_counts()


def make_uoa_ax(df, ax, letter):
    uoa_list = []
    outer = [len(df[df['Main panel'] == 'C']),
             len(df[df['Main panel'] == 'D']),
             len(df[df['Unit of assessment number'] == 4])]
    df['Unit of assessment number'] = df['Unit of assessment number'].astype(int)
    pan_c = df[(df['Unit of assessment number'] >= 13) &
               (df['Unit of assessment number'] <= 24)]
    pan_d = df[(df['Unit of assessment number'] > 24)]
    pan_c_list = pan_c['Unit of assessment number'].value_counts()
    pan_c_list = pan_c_list.sort_index().to_list()
    pan_d_list = pan_d['Unit of assessment number'].value_counts()
    pan_d_list = pan_d_list.sort_index().to_list()
    uoa_list.extend(pan_c_list)
    uoa_list.extend(pan_d_list)
    uoa_list.extend([len(df[df['Unit of assessment number'] == 4])])
    col_list = []
    col_list.extend([ba_rgb2[0]] * len(pan_c_list))
    col_list.extend([ba_rgb2[1]] * len(pan_d_list))
    col_list.extend([ba_rgb2[2]])
    df_counts = df['Unit of assessment number'].value_counts()
    df_counts = (df_counts / len(df)) * 100
    col = []
    for val in df_counts.index:
        if val == 4:
            col.append(ba_rgb2[2])
        elif (val >= 13) and (val < 25):
            col.append(ba_rgb2[0])
        else:
            col.append(ba_rgb2[1])
    df_counts.plot(kind='bar', ax=ax, edgecolor='k', color=col, legend=True)
    ax.set_ylabel('Percentage of ICS', fontsize=16)
    ax.set_xlabel('Unit of Assessment', fontsize=16)
    size = 0.3
    axin2 = inset_axes(ax, width="100%", height="100%", loc='upper left',
                       bbox_to_anchor=(0.5, .5, .6, .6),
                       bbox_transform=ax.transAxes)
    wedges, texts = axin2.pie(outer, radius=1,
                              colors=[ba_rgb2[0], ba_rgb2[1], ba_rgb2[2]], rotatelabels =True, startangle=360,
                              wedgeprops=dict(width=size, edgecolor='k', linewidth=0.5),
                              explode = [0.15, 0.15, 0.15])
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
#    kw = dict(arrowprops=dict(arrowstyle="-"),
#              bbox=bbox_props,
#              zorder=0, va="center")
    recipe = ['Panel C', 'Panel D', 'UoA 4']
#    for i, p in enumerate(wedges):
#
#        ang = (p.theta2 - p.theta1) / 2 + p.theta1
#        y = np.sin(np.deg2rad(ang))
#        x = np.cos(np.deg2rad(ang))
#        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
#        connectionstyle = f"angle,angleA=0,angleB={ang}"
#        kw["arrowprops"].update({"connectionstyle": connectionstyle,
#                                 "color": "k"})
#        shifter_out_x = 1.15
#        if recipe[i] == 'UoA 4':
#            shifter_out_y = 1.9
#        else:
#            shifter_out_y = 1.6
#        axin2.annotate(recipe[i], xy=(x, y), xytext=(shifter_out_x * np.sign(x), shifter_out_y * y),
#                       horizontalalignment=horizontalalignment, fontsize=13,
#                       **kw)
    from matplotlib.patches import Patch
    legend_elements = [Patch(edgecolor=(0,0,0,1),lw=0.75,
                             facecolor=ba_rgb2[2], label='UoA 4', linestyle='-'),
                       Patch(edgecolor=(0,0,0,1),lw=0.75,
                             facecolor=ba_rgb2[0], label=r'Panel C', linestyle='-'),
                       Patch(edgecolor=(0,0,0,1),lw=0.75,
                             facecolor=ba_rgb2[1], label=r'Panel D', linestyle='-'),
                       ]
    ax.legend(handles=legend_elements, loc='lower right', frameon=True,
              bbox_to_anchor=[1, 0.125],
              fontsize=12, framealpha=1, facecolor='w',
              title = 'Discipline',
              edgecolor='k', handletextpad=0.25)

    ax.set_title(letter, loc='left', x=-0.125, fontsize=18, y=1.015, fontweight='bold')
    ax.tick_params(axis='y', which='major', labelsize=14)
    ax.tick_params(axis='x', which='major', labelsize=12)
    fmt = '%.0f%%'
    yticks = mtick.FormatStrFormatter(fmt)
    ax.yaxis.set_major_formatter(yticks)
    sns.despine(ax=ax)
    return ax


def make_topic_value_counts(df, ax, letter):
    y_pos = np.arange(len(df['topic_name_short'].value_counts()))
    x = df['topic_name_short'].value_counts()
    y = df['topic_name_short'].value_counts().index
    ax.set_yticklabels([])
    ax.set_yticks([])
    ax.invert_xaxis()
    hbars = ax.barh(y, x, color=ba_rgb2[0], edgecolor='k')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(y)
    ax.bar_label(hbars, fmt='%.0f', padding=6, fontsize=17)
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.set_title(letter, loc='left', x=-0.1, fontsize=18, y=0.985, fontweight='bold')
    sns.despine(ax=ax, left=True, right=False, top=True, bottom=True)
    ax.set_xticklabels([])
    ax.set_xticks([])
    ax.set_xlabel('Number of Impact\nCase Studies', fontsize=16)
    ax.set_ylim(ax.get_ylim()[0]+.4, ax.get_ylim()[1]-0.4)
    for bar in hbars:
        bar.set_edgecolor("k")
        bar.set_linewidth(1)
    return ax


def make_ts_ax(paper_level, ax, letter):
    import matplotlib.dates as mdates
    paper_level['date_normal'] = pd.to_datetime(paper_level['date_normal'])
    paper_level = paper_level[(paper_level['date_normal'] > '2000-01-01') &
                              (paper_level['date_normal'] < '2024-01-01')]
    to_plot = paper_level['date_normal'].value_counts().sort_index().cumsum()
    index = to_plot.index.tolist()
    vals = to_plot.tolist()
    ax.plot(index, vals, color=ba_rgb2[1])
    ax.set_title(letter, loc='left', x=-0.05, fontsize=18, y=1.03, fontweight='bold')
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.yaxis.tick_right()
    ax.yaxis.set_ticks_position('both')
    ax.set_ylabel("Research\nCount", fontsize=16)
    ax.yaxis.set_label_position("right")
    formatter = mdates.DateFormatter("%Y")  ### formatter of the date
    locator = mdates.YearLocator()
    ax.xaxis.set_major_formatter(formatter)  ## calling the formatter for the x-axis
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_locator(plt.MaxNLocator(3))
    sns.despine(ax=ax, left=True, right=False, top=True, bottom=False)
    return ax


def make_cluster_figure(df, paper_level, cluster):
    print('\n******************************************************')
    print('***************** Making Figure {}! ********************'.format(str(cluster+3)))
    print('********************************************************')
    paper_level = filter_cluster(paper_level, cluster)
    df = filter_cluster(df, cluster)
    df_for, for_list = make_and_clean_for(paper_level)
    author_level = make_author_level(paper_level)
    fig = plt.figure(figsize=(13, 20), tight_layout=True)
    spec = gridspec.GridSpec(nrows=34, ncols=34, figure=fig)
    ax1 = fig.add_subplot(spec[0:9, 0:12])
    ax2 = fig.add_subplot(spec[0:10, 14:25])
    ax3 = fig.add_subplot(spec[0:4, 26:34])
    ax4 = fig.add_subplot(spec[2:27, 0:27])
    ax5 = fig.add_subplot(spec[6:18, 28:31])
    ax6 = fig.add_subplot(spec[20:32, 0:16])
    ax7 = fig.add_subplot(spec[20:32, 19:34], polar=True)
    make_uoa_ax(df, ax1, 'a.')
    make_wc_ax(paper_level, ax2, 'b.')
    make_ts_ax(paper_level, ax3, 'c.')
    make_geo_ax(df, ax4, 'd.')
    make_topic_value_counts(df, ax5, 'e.')
    make_funder_ax(df, author_level, ax6, cluster, 'f.', 'g.')
    make_inter_ax(df_for, ax7, 'h.')
    filepath = os.path.join(os.getcwd(), '..', '..', 'figures')
    savefigures(fig, filepath, 'figure_'+str(cluster+3))