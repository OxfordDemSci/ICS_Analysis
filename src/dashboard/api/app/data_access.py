from typing import Dict, List, Tuple, Union

from .data_queries import (get_topic_groups, get_topics, get_website_text,
                           query_dashboard_data)
from .data_types import (BeneficiaryType, FunderType, PostCodeAreaType,
                         ThresholdType, TopicType, UKRegionType, UOAType)


def validate_params(
    threshold: float,
    topic: str | None = None,
    postcode_area: list | None = None,
    beneficiary: str | None = None,
    uk_region: str | None = None,
    uoa: str | None = None,
    funder: str | None = None,
) -> Tuple[
    float,
    Union[str, None],
    Union[list, None],
    Union[str, None],
    Union[str, None],
    Union[str, None],
]:
    threshold = ThresholdType(threshold).value
    topic = None if topic == "null" else TopicType(topic).value
    postcode_area = (
        None if postcode_area == "null" else PostCodeAreaType(postcode_area).value
    )
    beneficiary = None if beneficiary == "null" or uk_region is not None else BeneficiaryType(beneficiary).value
    uk_region = None if uk_region == "null" else UKRegionType(uk_region).value
    uoa = None if uoa == "null" else UOAType(uoa).value
    funder = None if funder == "null" else FunderType(funder).value
    return threshold, topic, postcode_area, beneficiary, uk_region, uoa, funder


def get_init() -> Dict[str, Union[dict, float]]:
    init_data: Dict[str, Union[dict, float]] = {}
    init_data["website_text"] = get_website_text()
    init_data["ics_threshold"] = 0.5
    init_data["topic_groups"] = get_topic_groups()
    init_data["topics"] = get_topics()
    return init_data


def get_ics_database_topics(topic: str | None = None) -> Dict[str, dict]:
    return get_topics(topic=topic)


def get_data(
    threshold: float,
    topic: str | None = None,
    postcode: list | None = None,
    beneficiary: str | None = None,
    uk_region: str | None = None,
    uoa: str | None = None,
    funder: str | None = None,
) -> Dict[str, List[Dict[str, str]]]:
    data = query_dashboard_data(threshold, topic, postcode, beneficiary, uk_region, uoa, funder)
    return data
