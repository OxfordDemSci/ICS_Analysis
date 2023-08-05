from typing import Tuple, Union
from .models import ICS, UOA, Institution, Countries, Topics, Funder
from .data_queries import (
    get_topics, 
    get_topic_groups,
    get_funders_counts, 
    get_countries_counts, 
    get_uoa_counts, 
    get_institution_counts,
    get_website_text,
    query_dashboard_data,
    get_ics_table_for_country,
    )

from .data_types import (
    ThresholdType,
    TopicType,
    PostCodeAreaType,
    BeneficiaryType,
    UOAType,
    FunderType    
)

def validate_params(
        threshold: float,
        topic: str | None = None,
        postcode_area: str | None = None,
        beneficiary: str | None = None,
        uoa: str | None = None,
        funder: str | None = None,
        ) -> Tuple[float, Union[str, None], Union[str, None], Union[str, None], Union[str, None], Union[str, None]]:
    threshold = ThresholdType(threshold).value
    topic = None if topic == "null" else TopicType(topic).value
    postcode_area = None if postcode_area == "null" else PostCodeAreaType(postcode_area).value
    beneficiary = None if beneficiary == "null" else BeneficiaryType(beneficiary).value
    uoa = None if uoa == "null" else UOAType(uoa).value
    funder = None if funder == "null" else FunderType(funder).value
    return threshold, topic, postcode_area, beneficiary, uoa, funder





def get_init():
    init_data = {}
    init_data["website_text"] = get_website_text()    
    init_data["ics_threshold"] = 0.5
    init_data["topic_groups"] = get_topic_groups()
    init_data['topics'] = get_topics()
    return init_data

def get_ics_database_topics(topic=None):
    return get_topics(topic=topic)

def get_data(threshold, topic=None, postcode=None, beneficiary=None, uoa=None, funder=None):
    data = query_dashboard_data(threshold, topic, postcode, beneficiary, uoa, funder)
    return data

def get_country_ics_data(threshold, topic=None, postcode_area=None, beneficiary=None, uoa=None, funder=None):
    data = get_ics_table_for_country(threshold, topic, postcode_area, beneficiary, uoa, funder, limit=500)
    return data




