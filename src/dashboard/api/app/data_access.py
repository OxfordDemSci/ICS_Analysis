
from .models import ICS, UOA, Institution, Countries, Topics, Funder
from .data_queries import (
    get_topics, 
    get_funders_counts, 
    get_countries_counts, 
    get_uoa_counts, 
    get_institution_counts,
    get_website_text,
    query_dashboard_data,
    get_ics_table_for_country,
    )

def get_init():
    init_data = {}
    init_data["website_text"] = get_website_text()    
    init_data["ics_threshold"] = 0.5
    init_data['topics'] = get_topics()
    return init_data

def get_ics_database_topics():
    return get_topics()

def get_data(threshold, topic=None, postcode=None, beneficiary=None, uoa=None, funder=None):
    data = query_dashboard_data(threshold, topic, postcode, beneficiary, uoa, funder)
    return data

def get_country_ics_data(country, topic, threshold, postcode=None):
    data = get_ics_table_for_country(country, topic, threshold, postcode)
    return data




