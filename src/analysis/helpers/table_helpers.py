import pandas as pd
import os


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