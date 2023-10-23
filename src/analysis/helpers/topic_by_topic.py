import os
import re
import unicodedata
import numpy as np
import pandas as pd
import seaborn as sns
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import gender_guesser.detector as gender
import matplotlib.gridspec as gridspec
from PIL import Image
from sankeyflow import Sankey
from .figure_helpers import savefigures
from .general_helpers import return_paper_level
from mne_connectivity.viz import plot_connectivity_circle
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

d = gender.Detector()
plt.rcParams["font.family"] = "Helvetica"
ba_rgb2 = [(0 / 255, 160 / 255, 223 / 255, 0.65),
           (255 / 255, 182 / 255, 0 / 255, 0.65),
           (254 / 255, 59 / 255, 31 / 255, 0.65)]

ba_rgb1 = [(0 / 255, 160 / 255, 223 / 255, 0.45),
           (255 / 255, 182 / 255, 0 / 255, 0.45),
           (254 / 255, 59 / 255, 31 / 255, 0.45)]


def make_descriptives(cluster):
    df = pd.read_csv(os.path.join(os.getcwd(), '..', '..', 'data',
                                  'topic_lookup',
                                  'raw_with_topic_data.csv'))
    dim_out = os.path.join(os.getcwd(), '..', '..',
                           'data', 'dimensions_returns')
    paper_level = return_paper_level(dim_out)
    paper_level = pd.merge(paper_level,
                           df[['REF impact case study identifier', 'Cluster']],
                           how='left',
                           right_on = 'REF impact case study identifier',
                           left_on='Key')
    country_count = pd.read_csv(os.path.join(os.getcwd(), '..', '..',
                                             'data', 'intermediate',
                                             'ICS_countries_funders_manual.csv'))
    country_count = pd.merge(country_count,
                             df[['REF impact case study identifier', 'Cluster']],
                             how='left',
                             on = 'REF impact case study identifier')

    country_count = filter_cluster(country_count, cluster)
    paper_level = filter_cluster(paper_level, cluster)
    df = filter_cluster(df, cluster)
    df_for = make_and_clean_for(paper_level)
    author_level = make_author_level(paper_level)

    df_counts = df['Unit of assessment number'].value_counts()
    mystr = 'Distribution Across UoAs: '
    print('Number of ICS: ', len(df))
    for value, index in zip(df_counts, df_counts.index):
        mystr = mystr + 'UoA ' + str(value) + ' (' + str(index) + '), '
    mystr = mystr[:-2]
    print(mystr)

    funder_count = pd.read_csv(os.path.join(os.getcwd(), '..', '..',
                                            'data', 'intermediate',
                                            'ICS_countries_funders_manual.csv'))
    funder_count = pd.merge(funder_count, df[['REF impact case study identifier',
                                              'Cluster']],
                            how='left', on='REF impact case study identifier')
    funder_count = filter_cluster(funder_count, cluster)
    funder_list = []
    for index, row in funder_count.iterrows():
        funders = row['Funders[full name]']
        if funders is not np.nan:
            funders = funders.split(';')
            for funder in funders:
                funder_list.append(funder.strip())
    funder_count = pd.DataFrame(funder_list)[0].value_counts()
    funder_count = funder_count.sort_values(ascending=False)
    funder_count = funder_count[0:7].sort_values(ascending=False)
    print('The most frequent funder is: ' + str(funder_count.index[0]) +
          '('+str(funder_count[0]) + '). The second most is: ' +
           str(funder_count.index[1]) + '('+str(funder_count[1]) + ').')


    country_list = []
    for index, row in country_count.iterrows():
        countries = row['Countries[alpha-3]']
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

    print('The most frequent country beneficiary is : ' + str(country_count['Country'][0]) +
          '('+str(country_count['Count'][0]) + '). The second most is: ' +
           str(country_count['Country'][1]) + '('+str(country_count['Count'][1]) + ').')


    country_count = pd.read_csv(os.path.join(os.getcwd(), '..', '..',
                                             'data', 'intermediate',
                                             'ICS_countries_funders_manual.csv'))
    country_count = pd.merge(country_count,
                             df[['REF impact case study identifier', 'Cluster']],
                             how='left',
                             on = 'REF impact case study identifier')

    country_count = filter_cluster(country_count, cluster)

    country_list = []
    for index, row in country_count.iterrows():
        countries = row['Countries[region]']
        if countries is not np.nan:
            countries = countries.split(';')
            for country in countries:
                country_list.append(country.strip())
    country_count = pd.DataFrame(country_list)[0].value_counts()
    country_count = country_count.sort_values(ascending=False)
    country_count = country_count.reset_index()
    country_count = pd.DataFrame(country_count).rename({0: 'Count',
                                                        'index': 'Region'},
                                                       axis=1)

    print('The most frequent regional beneficiary is : ' + str(country_count['Region'][0]) +
          ' ('+str(country_count['Count'][0]) + '). The second most is: ' +
           str(country_count['Region'][1]) + ' ('+str(country_count['Count'][1]) + ').')

    df_for, for_list = make_and_clean_for(paper_level)

    print('The five most common interdisciplinarities are: ' +
          str(for_list.index[0][0]) + ' (' + str(for_list[0]) + '), ' +
          str(for_list.index[1][0]) + ' (' + str(for_list[1]) + '), ' +
          str(for_list.index[2][0]) + ' (' + str(for_list[2]) + '), ' +
          str(for_list.index[3][0]) + ' (' + str(for_list[3]) + '), ' +
          str(for_list.index[4][0]) + ' (' + str(for_list[4]) + ').')

    type_count = paper_level['type'].value_counts()/len(paper_level)*100
    type_count = type_count.round(2)

    print('The five most common types of underpinning research are: ' +
          str(type_count.index[0]) + ' (' + str(type_count[0]) + '%), ' +
          str(type_count.index[1]) + ' (' + str(type_count[1]) + '%), ' +
          str(type_count.index[2]) + ' (' + str(type_count[2]) + '%), ' +
          str(type_count.index[3]) + ' (' + str(type_count[3]) + '%), ' +
          str(type_count.index[4]) + ' (' + str(type_count[4]) + '%).')

    from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
    file = open(os.path.join(os.getcwd(), '..', '..', 'data', 'support', "custom_stopwords.txt"), "r")
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
    print('The five ten commonly seen concepts are: ' +
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


def make_author_level(paper_level):
    author_level = pd.DataFrame(columns=['Panel', 'UoA', 'ICS_uid',
                                         'pub_uid', 'first_name', 'gender'])
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
    return author_level


def make_geo_ax(country_count, ax, letter):
    country_list = []
    for index, row in country_count.iterrows():
        countries = row['Countries[alpha-3]']
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
    geo_df = gpd.read_file(os.path.join(os.getcwd(), '..', '..',
                                        'data', 'shapefiles',
                                        SHAPEFILE_head,
                                        SHAPEFILE_head + SHAPEFILE_base))
    geo_df = geo_df[['ADMIN', 'ADM0_A3', 'geometry']]
    geo_df.columns = ['country', 'country_code', 'geometry']
    geo_df = geo_df.drop(geo_df.loc[geo_df['country'] == 'Antarctica'].index)
    geo_df = pd.merge(left=geo_df, right=country_count, how='left',
                      left_on='country_code', right_on='Country')
    geo_df['Count'] = geo_df['Count'].fillna(0)
    col = 'Count'
    cmap = 'viridis'
    geo_df.plot(column=col, ax=ax, edgecolor='k', linewidth=0.25,
                cmap=cmap, scheme="natural_breaks",
                k=8, legend=True,
                legend_kwds={"loc": "lower left",
                             "frameon": True,
                             "edgecolor": 'k',
                             "ncols": 2,
                             "bbox_to_anchor": (0.015, 0.05),
                             "fmt": "{:.0f}",
                             "fontsize": 11,
                             "interval": True}
                )

    leg1 = ax.get_legend()
    leg1.set_title("Mentioned as Beneficiary", prop={'size': 14})
    ax.set_xticks([])
    ax.set_xticklabels([])
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.set_title(letter, loc='left', x=-0.05, fontsize=18, y=1.025)
    sns.despine(ax=ax, left=True, bottom=True)
    return ax


def make_wc_ax(paper_level, ax, letter):
    from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
    mask = np.array(Image.open(os.path.join(os.getcwd(), '..',
                                            '..', 'assets',
                                            'wordcloud_mask.png')))
    image_colors = ImageColorGenerator(mask)
    file = open(os.path.join(os.getcwd(), '..', '..', 'data', 'support', "custom_stopwords.txt"), "r")
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
    ax.set_title(letter, loc='left', x=-0.05, fontsize=18, y=1.025)
    sns.despine(ax=ax, left=True, bottom=True)


def make_inter_ax(df_for, ax, letter):
    plot_connectivity_circle(df_for.replace(0, np.nan).to_numpy(),
                             list(df_for.index), padding=5,
                             facecolor='white', node_width=12,
                             textcolor='black', node_linewidth=1,
                             linewidth=5, colormap='RdBu', vmin=None,
                             vmax=None, colorbar=True,
                             title=letter, fontsize_title=20,
                             node_colors=['w'], colorbar_size=0.75,
                             colorbar_pos=(.4, 0.5), ax=ax,
                             fontsize_names=14, fontsize_colorbar=13)
    ax.set_xticks([])
    ax.set_xticklabels([])
    ax.set_yticks([])
    ax.set_yticklabels([])
    #    ax.set_title(letter, loc='left', x=-0.0, fontsize=100, y=1.0)
    return ax


def make_sankey_ax(length, ax, cluster, letter):
    if cluster == '9.':
        flows = [('Home', 'Sports', 198 / length * 100, {'color': ba_rgb1[0], 'flow_color_mode': 'dest'}),
                 ('Home', 'Prevention', 132 / length * 100, {'color': ba_rgb1[0], 'flow_color_mode': 'dest'}),
                 ('Home', 'Detection', 131 / length * 100, {'color': ba_rgb1[0], 'flow_color_mode': 'dest'}),
                 ('Home', 'Diet', 32 / length * 100, {'color': ba_rgb1[0], 'flow_color_mode': 'dest'}),
                 ('Sports', ' Sport', 198 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Prevention', 'Efficiency', 70 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Prevention', 'Interventions', 19 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Prevention', 'Trials', 17 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Prevention', 'Funding', 13 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Prevention', 'Disease', 13 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Detection', 'Diagnosis', 28 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Detection', 'Autism', 27 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Detection', 'Wellbeing', 22 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Detection', 'Stroke', 16 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Detection', 'Mental Health', 14 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Detection', 'Death', 12 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Detection', 'Self-harm', 12 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Diet', 'Obesity', 19 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Diet', 'Disorders', 13 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'})
                 ]
    elif cluster == '2.':
        flows = [('Home', 'Archaelogy', 85 / length * 100, {'color': ba_rgb1[0], 'flow_color_mode': 'dest'}),
                 ('Home', 'Military', 58 / length * 100, {'color': ba_rgb1[0], 'flow_color_mode': 'dest'}),
                 ('Home', 'Cultural', 41 / length * 100, {'color': ba_rgb1[0], 'flow_color_mode': 'dest'}),
                 ('Home', 'Films', 48 / length * 100, {'color': ba_rgb1[0], 'flow_color_mode': 'dest'}),
                 ('Home', 'Arts', 46 / length * 100, {'color': ba_rgb1[0], 'flow_color_mode': 'dest'}),
                 ('Home', 'Participatory', 29 / length * 100, {'color': ba_rgb1[0], 'flow_color_mode': 'dest'}),
                 ('Home', 'Theology', 27 / length * 100, {'color': ba_rgb1[0], 'flow_color_mode': 'dest'}),
                 ('Archaelogy', 'Heritage', 32 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Archaelogy', 'Property', 16 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Archaelogy', 'Co-production', 13 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Archaelogy', 'Exhumation', 12 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Archaelogy', 'Public', 12 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Military', 'History', 30 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Military', 'Holocaust', 28 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Cultural', ' Cultural', 51 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Films', 'Film', 48 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Arts', 'Art', 46 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 (
                 'Participatory', 'Participation', 29 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Theology', ' Theology', 27 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ]
    elif cluster == '10.':
        flows = [('Home', 'Sustainability', 129 / length * 100,
                  {'color': ba_rgb1[0], 'flow_color_mode': 'dest', 'alpha': 0.05}),
                 ('Home', 'Housing', 71 / length * 100, {'color': ba_rgb1[0], 'flow_color_mode': 'dest'}),
                 ('Home', 'Biodiversity', 38 / length * 100, {'color': ba_rgb1[0], 'flow_color_mode': 'dest'}),
                 ('Home', 'Safety', 29 / length * 100, {'color': ba_rgb1[0], 'flow_color_mode': 'dest'}),
                 (
                 'Sustainability', 'Conservation', 71 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Sustainability', 'Renewable', 31 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Sustainability', 'Urban', 15 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ('Sustainability', 'Climate', 12 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ("Housing", "Local", 58 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ("Housing", "Efficiency", 13 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ("Biodiversity", "Farming", 23 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ("Biodiversity", "Food", 15 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ("Safety", "Preparedness", 18 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'}),
                 ("Safety", "Roads", 11 / length * 100, {'color': ba_rgb1[1], 'flow_color_mode': 'dest'})
                 ]
    nodes = Sankey.infer_nodes(flows)
    s = Sankey(flows=flows,
               node_opts=dict(label_format='{label} ({value:.2f}%)'),
               cmap=plt.cm.binary, alpha=0.05
               )
    s.find_node("Home")[0].label_format = ''
    s.draw(ax=ax)
    ax.set_ylim(0, 1)
    ax.set_title(letter, loc='left', x=-0.05, fontsize=18, y=1.025)
    return ax


def make_funder_ax(df, df1, ax, cluster, letter, letter2):
    funder_df = make_funder_df(cluster, df)
    edgecolors = ['k', 'w'] * 8
    ax.barh(width=funder_df['index'], y=funder_df[0],
            height=1, edgecolor=edgecolors, color=ba_rgb2[0])
    ax.set_ylabel('Instances of Funding', fontsize=16)
    ax.set_ylim(-0.5, 12.65)
    for i, yi in enumerate(funder_df[0]):
        if (i % 2) != 0:
            mystr = funder_df[0].to_list()[i].split(' [')[0].replace('_temp', '')
            ax.text(1, yi, mystr, horizontalalignment='left',
                    verticalalignment='center', fontsize=13)
        else:
            ax.text(1, yi, "{:.2%}".format(funder_df['index'].to_list()[i] / len(df)), fontsize=13,
                    horizontalalignment='left', verticalalignment='center',
                    color='w')
    ax.set_xticks([])
    ax.set_xticklabels([])
    ax.set_yticks([])
    ax.set_yticklabels([])
    sns.despine(ax=ax, left=True, bottom=True)
    ax.set_title(letter, loc='left', x=-0.05, fontsize=18, y=1.025)
    axin2 = inset_axes(ax, width="100%", height="100%", loc='lower right',
                       bbox_to_anchor=(0.715, 0, .315, .335),
                       bbox_transform=ax.transAxes)

    fem = df1['female'].sum() / len(df1['female']) * 100
    men = 100 - fem
    bar_container = axin2.bar(x=['Female', 'Male'], height=[fem, men],
                              color=[ba_rgb2[1], ba_rgb2[0]],
                              width=0.8, edgecolor='k')
    axin2.set_title(letter2, loc='left', x=-0.05, fontsize=18, y=1.025)
    axin2.tick_params(axis='both', which='major', labelsize=14)
    sns.despine(ax=axin2)
    axin2.set_ylabel('Gender of Authors', fontsize=14)
    axin2.bar_label(bar_container,
                    fmt='%.2f%%', padding=0.05, fontsize=14)
    fmt = '%.0f%%'
    yticks = mtick.FormatStrFormatter(fmt)
    axin2.yaxis.set_major_formatter(yticks)
    return ax


def make_funder_df(cluster, df):
    funder_count = pd.read_csv(os.path.join(os.getcwd(), '..', '..',
                                            'data', 'intermediate',
                                            'ICS_countries_funders_manual.csv'))
    funder_count = pd.merge(funder_count, df[['REF impact case study identifier',
                                              'Cluster']],
                            how='left', on='REF impact case study identifier')
    funder_count = filter_cluster(funder_count, cluster)
    funder_list = []
    for index, row in funder_count.iterrows():
        funders = row['Funders[full name]']
        if funders is not np.nan:
            funders = funders.split(';')
            for funder in funders:
                funder_list.append(funder.strip())
    funder_count = pd.DataFrame(funder_list)[0].value_counts()
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
    #    funder_df.at[15, 'index'] = 0
    funder_df['index'] = funder_df['index'].astype(int)
    return funder_df


def make_topic_file():
    topic_lookup = pd.read_csv(os.path.join(os.getcwd(), '..', '..',
                                            'data', 'topic_lookup',
                                            'topic_lookup.csv'))
    raw_data = pd.read_excel(os.path.join(os.getcwd(), '..', '..',
                                          'data', 'raw',
                                          'raw_ics_data.xlsx'))
    topic_model = pd.read_csv(os.path.join(os.getcwd(), '..', '..',
                                           'data', 'topic_lookup',
                                           'candidate_nn3nn7_trimmed.csv'))
    df = pd.merge(raw_data, topic_model,
                  how='left',
                  on='REF impact case study identifier')
    df = pd.merge(df, topic_lookup,
                  how='left',
                  left_on='BERT_topic',
                  right_on='BERT_topic')
    shape_mask = ((df['Main panel'] == 'C') |
                  (df['Main panel'] == 'D') |
                  (df['Unit of assessment number'] == 4))
    df = df[shape_mask]
    df['Title'] = df['Title'].apply(lambda val: unicodedata. \
                                    normalize('NFKD', val). \
                                    encode('ascii', 'ignore').decode())
    df.to_csv(os.path.join(os.getcwd(), '..', '..', 'data', 'topic_lookup',
                           'raw_with_topic_data.csv'),
              index=False)
    df = df[['REF impact case study identifier', 'Title',
             'Main panel', 'Unit of assessment number',
             'Unit of assessment name', 'BERT_topic', 'Topic Name',
             'Short Name', 'Charlie_Suggested', 'Hierarchical Grouping',
             'Cluster', 'Topic Notes']]
    df.to_csv(os.path.join(os.getcwd(), '..', '..',
                           'data', 'topic_lookup',
                           'ICS_topic_lookup.csv'),
              index=False)


def filter_cluster(df, cluster_number):
    df = df[df['Cluster'].notnull()]
    df = df[df['Cluster'].str.startswith(cluster_number)]
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

    df_for = df_for.rename({'Information And Computing Sciences': 'IT'}, axis=0)
    df_for = df_for.rename({'Information And Computing Sciences': 'IT'}, axis=1)
    df_for = df_for.rename({'Built Environment And Design': 'Urban'}, axis=0)
    df_for = df_for.rename({'Built Environment And Design': 'Urban'}, axis=1)
    df_for = df_for.rename({'Biological Sciences': 'Biology'}, axis=0)
    df_for = df_for.rename({'Biological Sciences': 'Biology'}, axis=1)
    df_for = df_for.rename({'Health Sciences': 'Health'}, axis=0)
    df_for = df_for.rename({'Health Sciences': 'Health'}, axis=1)
    df_for = df_for.rename({'Language, Communication And Culture': 'Language'}, axis=0)
    df_for = df_for.rename({'Language, Communication And Culture': 'Language'}, axis=1)
    df_for = df_for.rename({'Earth Sciences': 'Earth'}, axis=0)
    df_for = df_for.rename({'Earth Sciences': 'Earth'}, axis=1)
    df_for = df_for.rename({'Physical Sciences': 'Physics'}, axis=0)
    df_for = df_for.rename({'Physical Sciences': 'Physics'}, axis=1)
    df_for = df_for.rename({'Chemical Sciences': 'Chem'}, axis=0)
    df_for = df_for.rename({'Chemical Sciences': 'Chem'}, axis=1)
    df_for = df_for.rename({'Economics': 'Econ'}, axis=1)
    df_for = df_for.rename({'Economics': 'Econ'}, axis=1)
    df_for = df_for.rename({'Biomedical And Clinical Sciences': 'Biomedical'}, axis=0)
    df_for = df_for.rename({'Biomedical And Clinical Sciences': 'Biomedical'}, axis=1)
    df_for = df_for.rename({'Agricultural, Veterinary And Food Sciences': 'Agriculture'}, axis=0)
    df_for = df_for.rename({'Agricultural, Veterinary And Food Sciences': 'Agriculture'}, axis=1)
    df_for = df_for.rename({'History, Heritage And Archaeology': 'History'}, axis=0)
    df_for = df_for.rename({'History, Heritage And Archaeology': 'History'}, axis=1)
    df_for = df_for.rename({'Law And Legal Studies': 'Law'}, axis=0)
    df_for = df_for.rename({'Law And Legal Studies': 'Law'}, axis=1)
    df_for = df_for.rename({'Environmental Sciences': 'Environmental'}, axis=0)
    df_for = df_for.rename({'Environmental Sciences': 'Environmental'}, axis=1)
    df_for = df_for.rename({'Law And Legal Studies': 'Law'}, axis=0)
    df_for = df_for.rename({'Law And Legal Studies': 'Law'}, axis=1)
    df_for = df_for.rename({'Creative Arts And Writing': 'Creative'}, axis=0)
    df_for = df_for.rename({'Creative Arts And Writing': 'Creative'}, axis=1)
    df_for = df_for.rename({'Commerce, Management, Tourism And Services': 'Tourism'}, axis=0)
    df_for = df_for.rename({'Commerce, Management, Tourism And Services': 'Tourism'}, axis=1)
    df_for = df_for.rename({'Mathematical Sciences': 'Mathematics'}, axis=0)
    df_for = df_for.rename({'Mathematical Sciences': 'Mathematics'}, axis=1)
    df_for = df_for.rename({'Philosophy And Religious Studies': 'Religion'}, axis=0)
    df_for = df_for.rename({'Philosophy And Religious Studies': 'Religion'}, axis=1)
    df_for = df_for.rename({'Human Society': 'Society'}, axis=0)
    df_for = df_for.rename({'Human Society': 'Society'}, axis=1)
    return df_for, pd.DataFrame(for_list).value_counts()


def make_uoa_ax(df, ax, letter):
    uoa_list = []
    outer = [len(df[df['Main panel'] == 'C']),
             len(df[df['Main panel'] == 'D']),
             len(df[df['Unit of assessment number'] == 4])]
    #    a, b, c = [plt.cm.Blues, plt.cm.Reds, plt.cm.Greens]
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
    df_counts.plot(kind='bar', ax=ax, edgecolor='k', color=col)
    ax.set_ylabel('Number of ICS', fontsize=16)
    ax.set_xlabel('Unit of Assessment', fontsize=16)
    size = 0.3
    cmap = plt.colormaps["tab20c"]
    #    inner_colors = cmap([1, 2, 5, 6, 9, 10])
    axin2 = inset_axes(ax, width="100%", height="100%", loc='upper left',
                       bbox_to_anchor=(0.275, .35, .75, .75),
                       bbox_transform=ax.transAxes)
    axin2.pie(uoa_list, radius=1 - size, colors=col_list,
              wedgeprops={'width': size, 'edgecolor': 'w', 'alpha': 0.3, 'linewidth': 0.5})
    wedges, texts = axin2.pie(outer, radius=1,
                              colors=[ba_rgb2[0], ba_rgb2[1], ba_rgb2[2]],
                              wedgeprops=dict(width=size, edgecolor='k', linewidth=0.5))
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")
    recipe = ['Panel C', 'Panel D', 'UoA 4']
    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1) / 2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        axin2.annotate(recipe[i], xy=(x, y), xytext=(1.35 * np.sign(x), 1.4 * y),
                       horizontalalignment=horizontalalignment, fontsize=14,
                       **kw)
    ax.set_title(letter, loc='left', x=-0.05, fontsize=18, y=1.025)
    ax.tick_params(axis='both', which='major', labelsize=14)
    fmt = '%.0f%%'
    yticks = mtick.FormatStrFormatter(fmt)
    ax.yaxis.set_major_formatter(yticks)
    sns.despine(ax=ax)
    return ax


def make_figure_output(cluster):
    df = pd.read_csv(os.path.join(os.getcwd(), '..', '..', 'data',
                                  'topic_lookup',
                                  'raw_with_topic_data.csv'))
    dim_out = os.path.join(os.getcwd(), '..', '..',
                           'data', 'dimensions_returns')
    paper_level = return_paper_level(dim_out)
    paper_level = pd.merge(paper_level,
                           df[['REF impact case study identifier', 'Cluster']],
                           how='left',
                           right_on = 'REF impact case study identifier',
                           left_on='Key')
    country_count = pd.read_csv(os.path.join(os.getcwd(), '..', '..',
                                             'data', 'intermediate',
                                             'ICS_countries_funders_manual.csv'))
    country_count = pd.merge(country_count,
                             df[['REF impact case study identifier', 'Cluster']],
                             how='left',
                             on = 'REF impact case study identifier')
    country_count = filter_cluster(country_count, cluster)
    paper_level = filter_cluster(paper_level, cluster)
    df = filter_cluster(df, cluster)
    df_for, for_list = make_and_clean_for(paper_level)
    author_level = make_author_level(paper_level)
#    print('Beginning to make the cluster figure for cluster: ', cluster)
    fig = plt.figure(figsize=(16, 13), constrained_layout=True)
    spec = gridspec.GridSpec(ncols=18, nrows=8, figure=fig)
    ax1 = fig.add_subplot(spec[0:2, 0:6])
    ax2 = fig.add_subplot(spec[0:2, 6:12])
    ax3 = fig.add_subplot(spec[0:5, 12:18])
    ax4 = fig.add_subplot(spec[2:5, 0:12])
    ax5 = fig.add_subplot(spec[5:8, 0:10])
    ax6 = fig.add_subplot(spec[5:8, 9:17],  polar=True)
#    print('Making the UoA sub-figure for cluster: ', cluster)
    make_uoa_ax(df, ax1, 'a.')
#    print('Making the WC sub-figure for cluster: ', cluster)
    make_wc_ax(paper_level, ax2, 'b.')
#    print('Making the Sankey sub-figure for cluster: ', cluster)
    make_sankey_ax(len(df), ax3, cluster, 'c.')
#    print('Making the choropleth sub-figure for cluster: ', cluster)
    make_geo_ax(country_count, ax4, 'd.')
#    print('Making the Funder sub-figure for cluster: ', cluster)
    make_funder_ax(df, author_level, ax5, cluster, 'e.', 'f.')
#    print('Making the Interdisciplinarity sub-figure for cluster: ', cluster)
    make_inter_ax(df_for, ax6, 'g.')
#    print('Saving figure for cluster: ', cluster)
    filepath = os.path.join(os.getcwd(), '..', '..', 'figures',
                            'SHAPE', 'cluster_infographics')
    savefigures(fig, filepath, 'infographic_cluster_'+cluster[0:-1])


#def main():
#    make_topic_file()
#    make_figure_output('2.')
#    make_figure_output('9.')
#    make_figure_output('10.')
#
#if __name__ == "__main__":
#    main()
