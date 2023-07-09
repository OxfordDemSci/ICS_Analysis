
from .models import ICS, UOA, Institution, Countries, Topics, Funder
from .data_queries import (
    get_topics, 
    get_funders_counts, 
    get_countries_counts, 
    get_uoa_counts, 
    get_institution_counts,
    get_topic_and_ics_above_threshold,
    get_website_text,
    query_dashboard_data,
    )

def get_init():
    init_data = {}
    init_data["website_text"] = get_website_text()
    init_data['topics'] = get_topics()
    # init_data['funders_counts'] = get_funders_counts()
    # init_data['countries_counts'] = get_countries_counts()
    # init_data['uoa_counts'] = get_uoa_counts()
    # init_data['institution_counts'] = get_institution_counts()    
    # init_data["ics_table"] = get_full_ics_table()
    return init_data

def get_data(topic, threshold, postcode=None):
    data = query_dashboard_data(topic, threshold, postcode)
    return data


def get_postcode_level_data(postcode, topic, threshold):
    data = get_topic_and_ics_above_threshold(topic, threshold, postcode)
    return data




