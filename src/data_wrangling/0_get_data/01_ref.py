from os.path import join
from os import listdir
import requests
import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
load_dotenv()  # define "basedir" environment variable in ./.env file


def get_impact_data(raw_path):
    """Grab raw REF Impact Data"""
    """ A function to get the raw ICS data"""
    url = "https://results2021.ref.ac.uk/impact/export-all"
    r = requests.get(url, allow_redirects=True)
    open(os.path.join(raw_path,  'raw_ref_ics_data.xlsx'), 'wb').write(r.content)


def get_environmental_data(raw_path):
    """Grab raw REF Environment Data"""
    """ A function to get the raw environmental data"""
    url = "https://results2021.ref.ac.uk/environment/export-all"
    r = requests.get(url, allow_redirects=True)
    open(os.path.join(raw_path,  'raw_ref_environment_data.xlsx'), 'wb').write(r.content)


def get_all_results(raw_path):
    """Grab raw REF Results Data"""
    """ A function to get the raw results data"""
    url = "https://results2021.ref.ac.uk/profiles/export-all"
    r = requests.get(url, allow_redirects=True)
    open(os.path.join(raw_path,  'raw_ref_results_data.xlsx'), 'wb').write(r.content)


def get_output_data(raw_path):
    """Grab raw REF OutPut Data"""
    """ A function to get the raw output data"""
    url = "https://results2021.ref.ac.uk/outputs/export-all"
    r = requests.get(url, allow_redirects=True)
    open(os.path.join(raw_path,  'raw_ref_outputs_data.xlsx'), 'wb').write(r.content)



def main():
    raw_path = os.path.join(os.getenv('basedir'), 'data', 'raw')
    data_files = [f for f in listdir(raw_path)]
    
    if ~('raw_ref_environment_data.xlsx' in data_files):
        get_environmental_data(raw_path)
    if ~('raw_ref_ics_data.xlsx' in data_files):
        get_impact_data(raw_path)
    if ~('raw_ref_results_data.xlsx' in data_files):
        get_all_results(raw_path)
    if ~('raw_ref_outputs_data.xlsx' in data_files):
        get_output_data(raw_path)


if __name__ == "__main__":
    main()