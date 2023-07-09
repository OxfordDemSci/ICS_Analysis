import json
from pathlib import Path

from .data_access import get_init, get_postcode_level_data, get_data

BASE = Path(__file__).resolve().parent

def read_init():
    init_data = get_init()
    return init_data

def get_ics_data(topic, threshold, postcode_area=None):
    data = get_data(topic, threshold, postcode_area)
    return data

def get_postcode_data(postcode_area, topic, threshold): 
    postcode_data = get_postcode_level_data(postcode_area, topic, threshold)
    return postcode_data
    


