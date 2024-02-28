import re
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pathlib import Path
import json
import time

# Paths
current_file = Path(__file__).resolve()
project_root = current_file.parent
while not (project_root / '.git').exists():
    project_root = project_root.parent

data_path = project_root / 'data'
output_path = data_path /  'ics_pdfs'

# Set up Chrome options
chrome_options = Options()
prefs = {"download.default_directory" : str(output_path)}
chrome_options.add_experimental_option("prefs", prefs)

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Read data
data = pd.read_csv(data_path / 'final' / 'enhanced_ref_data.csv')
keys = data['REF impact case study identifier']

# urls
head = 'https://results2021.ref.ac.uk/impact/'

grant_dict = dict()
aux_dict = dict()

for key in keys:
    print(key)
    url = head + key
    driver.get(url)
    
    time.sleep(1)
    potential_elements = driver.find_elements(By.TAG_NAME, 'a')
    
    pattern = re.compile(r"Download case study PDF")
    
    button = [p for p in potential_elements if pattern.search(p.text)][0]
    button.click()
    
    
    try:
        secondary_table = driver.find_elements(By.CLASS_NAME, "impact-metadata")
        element = secondary_table[1]
        
        # Find all <dt> elements within the <dl> element
        dt_elements = element.find_elements(By.TAG_NAME, 'dt')

        # Initialize a list to hold the text of each <dt> element
        dt_texts = [dt.text for dt in dt_elements]
        
        # Find all <dd> elements within the <dl> element
        dd_elements = element.find_elements(By.TAG_NAME, 'dd')

        # Initialize a list to hold the text of each <dd> element
        dd_texts = [dd.text for dd in dd_elements]
        
        aux_dict[key] = dict(zip(dt_texts, dd_texts))
        
    except:
        aux_dict[key] = "None"
    
    try:
        grant_funding_table = driver.find_element(By.XPATH, "//h4[text()='Grant funding']/following-sibling::table")
        grant_dict[key] = grant_funding_table.text
    except:
        grant_dict[key] = "None"
    

with open(output_path / 'aux_data.jsonl', 'w') as file:
    for key, value in aux_dict.items():
        json_line = json.dumps({key: value})
        file.write(json_line + '\n')

        
with open(output_path / 'grant_data.jsonl', 'w') as file:
    for key, value in grant_dict.items():
        json_str = json.dumps({key: value})
        file.write(json_str + '\n')