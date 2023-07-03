import pandas as pd
import os
import ast
import pandas as pd

def make_topic_table(table_path):
    raw = pd.read_csv(os.path.join(os.getcwd(),
                                   '..',
                                   '..',
                                   'data',
                                   'final',
                                   'raw_with_topics.csv'))
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
    df=pd.DataFrame(index=range(0, 94), columns = ['Topic Number',
                                                   'Panel C (%)',
                                                   'Panel D (%)',
                                                   'Modal UoA',
                                                   'Top Five Keywords',
                                                   'Modal Institution',
                                                   'Modal Type'])
    df['Topic Number'] = range(0, 94)
    counts = pd.DataFrame(raw['topic_top1'].value_counts()).reset_index()
    df = pd.merge(df, counts, how='left', left_on='Topic Number', right_on='index')
    df.drop('index', axis=1, inplace=True)
    df.rename({'topic_top1': 'Count'}, axis=1, inplace=True)
    df.set_index('Topic Number', inplace=True)
    for topic in range(0, 94):
        temp = raw[raw['topic_top1']==topic]
        pcC = len(temp[temp['Main panel']=='C'])/len(temp)
        pcD = len(temp[temp['Main panel']=='D'])/len(temp)
        df.at[topic, 'Panel C (%)'] = round(pcC*100, 2)
        df.at[topic, 'Panel D (%)'] = round(pcD*100, 2)
        df.at[topic, 'Modal UoA'] = int(temp['Unit of assessment number'].mode()[0])
        df.at[topic, 'Modal Institution'] = temp['Institution name'].mode()[0]
        df.at[topic, 'Modal Type'] = temp['Summary impact type'].mode()[0]
        word_list = ''
        for word in range(0, 5, 1):
            word_list = word_list + words.loc[topic, str(word)][0] + ', '
            word_list = word_list[:-1]
        df.at[topic, 'Top Five Keywords'] = word_list
    df = df[['Top Five Keywords',
             'Count',
             'Panel C (%)',
             'Panel D (%)',
             'Modal UoA',
             'Modal Institution',
             'Modal Type']]
    df.to_csv(os.path.join(table_path, 'All_Topics.csv'))
    return df


def grouper(df, uniq, filter_list, table_path, filename):
    """ Groupby helper to make aggregate tables"""
    grp = df.groupby(filter_list)['REF impact case study identifier'].count()
    grp = pd.DataFrame(grp)
    grp = grp.rename({'REF impact case study identifier': 'Number ICS'}, axis=1)
    grp['% Total ICS'] = ((grp['Number ICS']/grp['Number ICS'].sum())*100).round(2)
    grp = pd.merge(grp, uniq.groupby(filter_list)['fte'].sum(),
                   how = 'left', left_on = filter_list,
                   right_on = filter_list)
    grp = pd.merge(grp, uniq.groupby(filter_list)['num_doc_degrees_total'].sum(),
                   how = 'left', left_on = filter_list,
                   right_on = filter_list)
    grp = pd.merge(grp, uniq.groupby(filter_list)['tot_income'].sum(),
                   how = 'left', left_on = filter_list,
                   right_on = filter_list)
    grp['tot_income'] = (grp['tot_income']/1000000000).round(2)
    grp = grp.rename({'tot_income': 'Total Income (£bn)',
                      'fte': 'FTE',
                     'num_doc_degrees_total': 'Doctoral Degrees'}, axis=1,)
    grp = grp.reset_index()
    grp.to_csv(os.path.join(table_path, filename), index=False)
    return grp