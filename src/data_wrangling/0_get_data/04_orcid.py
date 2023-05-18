import pandas as pd
import os
import random
import string
from dotenv import load_dotenv
load_dotenv()  # define "basedir" environment variable in ./.env file

## PLACEHOLDER SIMULATION DATA
raw_path = os.path.join(os.getenv('basedir'), 'data', 'raw')

output_data = pd.read_excel(os.path.join(raw_path, 'raw_dimensions_data.xlsx'))

## Subset relevant columns
rel_set = output_data[['doi', 'inst_id', 'uoa_id']]

# generate a list of 1000 unique random author names
candidate_authors = [
    ''.join(random.choices(string.ascii_uppercase,
                           k=random.randint(5, 10))) for i in range(1000)]

# add a new column sampling 1-5 authors from the list of author names
rel_set['authors'] = rel_set.\
    apply(lambda row: [candidate_authors[random.randint(0, 999)]
                       for i in range(random.randint(1,5))], axis=1)

## save data
rel_set.to_excel(os.path.join(raw_path, 'raw_orcid_data.xlsx'))