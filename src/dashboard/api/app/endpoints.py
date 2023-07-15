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

def get_ics_data(threshold, topic=None, postcode_area=None, beneficiary=None, uoa=None, funder=None):
    if topic == "null":
        topic = None
    if postcode_area == "null":
        postcode_area = None
    if beneficiary == "null":
        beneficiary = None
    if uoa == "null":
        uoa = None
    if funder == "null":
        funder = None
    data = get_data(threshold, topic, postcode_area, beneficiary, uoa, funder)
    return data

def get_ics_data_country(country, topic, threshold, postcode_area=None):
    data = get_country_ics_data(country, topic, threshold, postcode_area)
    return data



