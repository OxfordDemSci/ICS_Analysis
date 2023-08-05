import json
from pathlib import Path
import typing
from flask import abort, make_response
from flask_limiter.util import get_remote_address

from .data_access import get_init, get_data, get_country_ics_data, get_ics_database_topics, validate_params
from .data_queries import download_ics_table, get_pdf_data
from .generate_report import report_pdf
from .generate_pdf_report import pdf_report

BASE = Path(__file__).resolve().parent

def read_init()-> dict:
    init_data = get_init()
    return init_data

def get_ics_topics()-> dict:
    data = get_ics_database_topics()
    return data

def get_ics_data(
        threshold: float,
        topic: str | None = None,
        postcode_area: str | None = None,
        beneficiary: str | None = None,
        uoa: str | None = None,
        funder: str | None = None,) -> dict:
    try:
        threshold, topic, postcode_area, beneficiary, uoa, funder = validate_params(
                                                                                    threshold,
                                                                                    topic,
                                                                                    postcode_area,
                                                                                    beneficiary,
                                                                                    uoa,
                                                                                    funder)
            
    except ValueError as e:
        abort(400, str(e))
    data = get_data(threshold, topic, postcode_area, beneficiary, uoa, funder)
    if all(not value for value in data.values()):
        return make_response("", 204)
    return data

def get_ics_data_country(threshold, topic=None, postcode_area=None, beneficiary=None, uoa=None, funder=None):
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
    data = get_country_ics_data(threshold, topic, postcode_area, beneficiary, uoa, funder)
    return data

def download_ics_as_csv(threshold, topic=None, postcode_area=None, beneficiary=None, uoa=None, funder=None):
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
    data = download_ics_table(threshold, topic, postcode_area, beneficiary, uoa, funder)
    return data

def download_ics_report_as_pdf(threshold, topic=None, postcode_area=None, beneficiary=None, uoa=None, funder=None):
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
    pdf_data = get_pdf_data(threshold, topic, postcode_area, beneficiary, uoa, funder)
    data = pdf_report(pdf_data, threshold, topic, postcode_area, beneficiary, uoa, funder)
    return data



