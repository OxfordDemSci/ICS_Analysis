from pathlib import Path
from typing import Dict, List, Union

from flask import abort, make_response
from flask.wrappers import Response

from .data_access import (get_data, get_ics_database_topics, get_init,
                          validate_params)
from .data_queries import download_ics_table, get_pdf_data
from .generate_pdf_report import pdf_report

BASE = Path(__file__).resolve().parent


def read_init() -> Dict[str, Union[dict, float]]:
    init_data = get_init()
    return init_data


def get_ics_topics() -> Dict[str, dict]:
    data = get_ics_database_topics()
    return data


def get_ics_data(
    threshold: float,
    table_page: int = 1,
    items_per_page: int = 500, 
    topic: str | None = None,
    postcode_area: list | None = None,
    beneficiary: str | None = None,
    uk_region: str | None = None,
    uoa: str | None = None,
    uoa_name: str | None = None,
    funder: str | None = None,
) -> Union[Dict[str, List[Dict[str, str]]], Response]:
    try:
        if not (isinstance(table_page, int) or None) or not (isinstance(items_per_page, int) or None):
            raise ValueError("table_page and items_per_page should be null or type integer")
        threshold, topic, postcode_area, beneficiary, uk_region, uoa, uoa_name, funder = validate_params(
            threshold, topic, postcode_area, beneficiary, uk_region, uoa, uoa_name, funder
        )

    except ValueError as e:
        abort(400, str(e))
    data = get_data(threshold, table_page, items_per_page, topic, postcode_area, beneficiary, uk_region, uoa, uoa_name, funder)
    if all(not value for value in data.values()):
        return make_response("", 204)
    return data


def download_ics_as_csv(
    threshold: float,
    topic: str | None = None,
    postcode_area: list | None = None,
    beneficiary: str | None = None,
    uk_region: str | None = None,
    uoa: str | None = None,
    uoa_name: str | None = None,
    funder: str | None = None,
) -> Response:
    try:
        threshold, topic, postcode_area, beneficiary, uk_region, uoa, uoa_name, funder = validate_params(
            threshold, topic, postcode_area, beneficiary, uk_region, uoa, uoa_name, funder
        )

    except ValueError as e:
        abort(400, str(e))
    data = download_ics_table(threshold, topic, postcode_area, beneficiary, uk_region, uoa, uoa_name, funder)
    return data


def download_ics_report_as_pdf(
    threshold: float,
    topic: str | None = None,
    postcode_area: list | None = None,
    beneficiary: str | None = None,
    uk_region: str | None = None,
    uoa: str | None = None,
    uoa_name: str | None = None,
    funder: str | None = None,
) -> Dict[str, dict]:
    try:
        threshold, topic, postcode_area, beneficiary, uk_region, uoa, uoa_name, funder = validate_params(
            threshold, topic, postcode_area, beneficiary, uk_region, uoa, uoa_name, funder
        )

    except ValueError as e:
        abort(400, str(e))
    pdf_data = get_pdf_data(threshold, topic, postcode_area, beneficiary, uk_region, uoa, uoa_name, funder)
    data = pdf_report(
        pdf_data, threshold, topic, postcode_area, beneficiary, uk_region, uoa, uoa_name, funder
    )
    return data
