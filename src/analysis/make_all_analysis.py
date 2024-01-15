import os
import pandas as pd
import matplotlib as mpl
from figure_plotters.make_figure_two import make_figure_two
from figure_plotters.make_figure_three import make_figure_three
from figure_plotters.make_figure_fourteen import make_figure_fourteen
from figure_plotters.make_figure_fifteen import make_figure_fifteen
from figure_plotters.make_figure_sixteen import make_figure_sixteen
from figure_plotters.make_figure_seventeen import make_figure_seventeen
from figure_plotters.make_figure_eighteen import make_figure_eighteen
from figure_plotters.make_figure_nineteen import make_figure_nineteen
from helpers.cluster_by_cluster import (make_cluster_figure,
                                        make_descriptives)
from table_makers.table_makers import (make_table_one,
                                       make_table_two,
                                       make_table_four,
                                       make_table_five,
                                       make_table_six)

def prep_data():
    df_ref = pd.read_csv(os.path.join(os.getcwd(),
                                      '..',
                                      '..',
                                      'data',
                                      'final',
                                      'enhanced_ref_data.csv'),
                         usecols=['Unit of assessment name',
                                  'fte',
                                  'num_doc_degrees_total',
                                  'tot_income',
                                  'REF impact case study identifier',
                                  'funders_extracted',
                                  'countries_extracted',
                                  'cluster_id',
                                  'Main panel',
                                  'Unit of assessment number',
                                  'topic_name_short'])
    df_paper = pd.read_excel(os.path.join(os.getcwd(),
                                          '..',
                                          '..',
                                          'data',
                                          'dimensions_returns',
                                          'merged_dimensions.xlsx')
                             )
    df_paper = pd.merge(df_paper,
                        df_ref[['REF impact case study identifier',
                                'cluster_id',
                                'Main panel',
                                'Unit of assessment number']],
                        how='left',
                        right_on='REF impact case study identifier',
                        left_on='Key')
    df_ref = df_ref[df_ref['cluster_id'].notnull()]
    df_ref['cluster_id'] = df_ref['cluster_id'].astype(int)
    return df_ref, df_paper


if __name__ == "__main__":
    mpl.use('Agg')
#    print('Making all Figures: Beginning!')
#    make_figure_two()
#    make_figure_three()
#    df, paper_level = prep_data()
    make_table_one(os.path.join('..', '..', 'tables'))
    make_table_two(os.path.join('..', '..', 'tables'))

#    for cluster in range(1, 11):
#        make_cluster_figure(df, paper_level, int(cluster))
#        make_descriptives(df, paper_level, int(cluster))
    make_table_four(os.path.join('..', '..', 'tables'))
#    make_figure_fourteen()
    make_table_five(os.path.join('..', '..', 'tables'))
#    make_figure_fifteen()
    make_table_six(os.path.join('..', '..', 'tables'))
#    make_figure_sixteen()
#    make_figure_seventeen()
#    make_figure_eighteen()
#    make_figure_nineteen()