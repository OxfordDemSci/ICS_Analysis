import requests
import os


def get_impact_data(raw_path):
    """ A function to get the raw ICS data"""
    url = "https://results2021.ref.ac.uk/impact/export-all"
    r = requests.get(url, allow_redirects=True)
    open(os.path.join(raw_path,  'raw_ics_data.xlsx'), 'wb').write(r.content)


def get_environmental_data(raw_path):
    """ A function to get the raw environmental data"""
    url = "https://results2021.ref.ac.uk/environment/export-all"
    r = requests.get(url, allow_redirects=True)
    open(os.path.join(raw_path,  'raw_environment_data.xlsx'), 'wb').write(r.content)


def get_output_data(raw_path):
    """ A function to get the raw output data"""
    url = "https://results2021.ref.ac.uk/outputs/export-all"
    r = requests.get(url, allow_redirects=True)
    open(os.path.join(raw_path,  'raw_outputs_data.xlsx'), 'wb').write(r.content)


def get_all_results(raw_path):
    """ A function to get the raw results data"""
    url = "https://results2021.ref.ac.uk/profiles/export-all"
    r = requests.get(url, allow_redirects=True)
    open(os.path.join(raw_path,  'raw_results_data.xlsx'), 'wb').write(r.content)


def main():
    raw_path = os.path.join(os.getcwd(), '..', '..', 'data', 'raw')
    get_impact_data(raw_path)
    get_environmental_data(raw_path)
    get_output_data(raw_path)
    get_all_results(raw_path)


if __name__ == "__main__":
    main()