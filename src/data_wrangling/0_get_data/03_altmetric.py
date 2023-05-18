import pandas as pd
import os
import random
from dotenv import load_dotenv
load_dotenv()  # define "basedir" environment variable in ./.env file

## PLACEHOLDER SIMULATION DATA
raw_path = os.path.join(os.getenv('basedir'), 'data', 'raw')

output_data = pd.read_excel(os.path.join(raw_path,'raw_dimensions_data.xlsx'))

## Subset relevant columns
rel_set = output_data[['doi', 'inst_id', 'uoa_id']]

## Simulate altmetric
rel_set['altmetric'] = [random.randint(0, 5000) for i in range(rel_set.shape[0])]

rel_set.to_excel(os.path.join(raw_path, 'raw_altmetric_data.xlsx'))