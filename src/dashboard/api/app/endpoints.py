import json
from pathlib import Path

from .data_access import get_init, get_data, get_country_ics_data, get_ics_database_topics

BASE = Path(__file__).resolve().parent

def read_init():
    init_data = get_init()
    return init_data

def get_ics_topics():
    data = get_ics_database_topics()
    return data

def get_ics_data(topic, threshold, postcode_area=None):
    data = get_data(topic, threshold, postcode_area)
    return data

def get_ics_data_country(country, topic, threshold, postcode_area=None):
    data = get_country_ics_data(country, topic, threshold, postcode_area)
    return data



