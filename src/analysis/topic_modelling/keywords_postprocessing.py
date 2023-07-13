import os
import pandas as pd
from ast import literal_eval


def fun(x):
    return literal_eval(x)[0]


if __name__ == '__main__':

    # load topic keywords data
    topic_filename = 'BERT_keywords_full_text.csv'
    dat = pd.read_csv(os.path.join('texual_output', topic_filename))

    # subset only keyword columns
    cols = list(map(str, range(0, 10)))
    df = dat[cols].applymap(fun)

    # concatenate keywords into comma separated string
    dat['keywords'] = df.apply(lambda x: ', '.join(x.astype(str)), 1)

    # save to disk
    outdir = os.path.join('data', 'tmp')
    os.makedirs(outdir, exist_ok=True)

    dat.to_csv(os.path.join(outdir, topic_filename))
