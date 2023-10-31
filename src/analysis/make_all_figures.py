import os
import pandas as pd
import matplotlib as mpl
from figure_plotters.make_figure_two import make_figure_two
from figure_plotters.make_figure_thirteen import make_figure_thirteen
from figure_plotters.make_figure_fourteen import make_figure_fourteen
from figure_plotters.make_figure_fifteen import make_figure_fifteen
from figure_plotters.make_figure_sixteen import make_figure_sixteen
from figure_plotters.make_figure_seventeen import make_figure_seventeen
from figure_plotters.make_figure_eighteen import make_figure_eighteen
from helpers.cluster_by_cluster import (make_cluster_figure,
                                        make_descriptives)
mpl.rcParams['font.family'] = 'Graphik'


def prep_data():
    df_ref = pd.read_csv(os.path.join(os.getcwd(),
                                      '..',
                                      '..',
                                      'data',
                                      'final',
                                      'enhanced_ref_data.csv')
                         )
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
    print('Making all Figures: Beginning!')
    make_figure_two()
    df, paper_level = prep_data()
    for cluster in range(1, 11):
        make_cluster_figure(df, paper_level, int(cluster))
        make_descriptives(df, paper_level, int(cluster))
    make_figure_thirteen()
    make_figure_fourteen()
#   @TODO: still '.'s in funder_extracted
    make_figure_fifteen()
    make_figure_sixteen()
    make_figure_seventeen()
    make_figure_eighteen()