import re
from dataclasses import dataclass, field
from typing import Set, List
from urllib.parse import urlparse

import pandas
import pycountry
from loguru import logger


def search_add_country(country_name: str, country_set: Set):
    country_name = country_name.strip().lower()
    # country_name = re.sub('\W$', '', country_name)
    if ',' in country_name:
        for cn in re.split(r'[,&]', country_name):
            country_set = search_add_country(cn, country_set)
    else:
        match country_name:
            case 'england' | 'wales' | 'scotland' | 'northern ireland' | 'uk' | 'u.k.' | 'great britain' | \
                 'cymru' | 'uk: united kingdom' | \
                 'european travellers to wales database users in order of frequency (14/01/2021): wales' | 'northern ireland/' | \
                 'uk (england)' | 'g3.1) uk: england' | 'g3.2) uk: england' | 'g3.3) uk: england' | 'midlothian':
                country_set.add('GBR')
            case 'eu' | 'europe' | 'european' | 'european union' | 'eu27' | 'eu countries' | 'eu28 (2013-2020)' | \
                 'europe wide' | 'europe – 28 member states':
                country_set.add('EU')
            case 'global' | 'worldwide' | 'worldwide (mainly across 140 countries where ielts is administered)' | \
                 'taiwan and 27 countries where gept scores are recognised' | 'international' | \
                 'worldwide (encompassing 112 countries)' | 'global (by informing food and agriculture organization policy that is applied globally)':
                country_set.add('GLOBAL')
            case 'north america':
                country_set.add('NORTH AMERICA')
            case 'latin america':
                country_set.add('LATIN AMERICA')
            case 'uk and worldwide':
                country_set.add('GBR')
                country_set.add('GLOBAL')
            case 'the netherlands' | 'netherlands (the)':
                country_set.add('NLD')
            case 'columbia':
                country = pycountry.countries.lookup('colombia')
                country_set.add(country.alpha_3)
            case 'democratic republic of congo' | 'democratic republic of the congo':
                country = pycountry.countries.lookup('COD')
                country_set.add(country.alpha_3)
            case 'côte d’ivoire' | 'cote d’ivoire':
                country = pycountry.countries.lookup('CIV')
                country_set.add(country.alpha_3)
            case 'russia' | 'russian federation (the)':
                country_set.add('RUS')
            case 'iran':
                country_set.add('IRN')
            case 'africa':
                country_set.add('AFRICA')
            case 'the maldives':
                country_set.add('MDV')
            case 'canada and malta':
                country_set.add('CAN')
                country_set.add('MLT')
            case 'republic of ireland':
                country_set.add('IRL')
            case 'un-habitat':
                for c in ['Algeria', 'Benin', 'Burkina Faso', 'Central African Republic', 'Congo', 'Gabon', 'Lesotho', 'Madagascar', 'Mali', 'Morocco', 'Mozambique', 'Nigeria', 'Somalia', 'South Africa', 'Uganda', 'United Republic of Tanzania', 'Finland', 'France', 'Germany', 'Israel', 'Italy', 'Norway', 'Spain', 'Sweden', 'Turkey', 'United States of America', 'Antigua and Barbuda', 'Argentina', 'Brazil', 'Chile', 'Colombia', 'El Salvador', 'Grenada', 'Haiti', 'Mexico', 'Venezuela', 'Bahrain', 'Bangladesh', 'China', 'India', 'Indonesia', 'Iran', 'Japan', 'Jordan', 'Pakistan', 'Republic of Korea', 'Saudi Arabia', 'Sri Lanka', 'Thailand', 'Albania', 'Belarus', 'Romania', 'Russian Federation']:
                    country_set = search_add_country(c, country_set)
            case 'republic of korea' | 'korea':
                country_set.add('KOR')
            case 'uk and south africa':
                country_set.add('GBR')
                country_set.add('ZAF')
            case 'austrailia':
                country_set.add('AUS')
            case 'uk eu usa china':
                country_set.add('GBR')
                country_set.add('EU')
                country_set.add('USA')
                country_set.add('CHN')
            case 'palestine':
                country_set.add('PSE')
            case 'tajikstan':
                country_set.add('TJK')
            case 'india and the uk':
                country_set.add('GBR')
                country_set.add('IND')
            case 'u s a':
                country_set.add('USA')
            case _:
                try:
                    country = pycountry.countries.lookup(country_name)
                    country_set.add(country.alpha_3)
                except Exception as e:
                    logger.error(e)
    return country_set


def clean_countries(ref_countries):
    if pandas.isna(ref_countries) or not ref_countries:
        return set()
    ref_countries = re.sub("[\[\]]", "", ref_countries).split(";")
    results = set()
    for c in ref_countries:
        results = search_add_country(c, results)
    return results


def clean_list(text):
    if pandas.isna(text) or not text:
        return set()
    return set(re.sub("[\[\]]", "", text).split(";"))


def check_doi(url):
    domain = urlparse(url).netloc
    return domain.lower() == 'doi.org'


@dataclass
class ImpactUrl:
    url: str
    is_doi: bool


@dataclass
class ImpactDetail:
    section: str
    text: str = ''
    urls: List[ImpactUrl] = field(default_factory=list)


@dataclass
class ImpactSubmission:
    institution_ukprn_code: int
    institution_name: str
    main_panel: str
    unit_of_assessment_number: str
    unit_of_assessment_name: str
    multiple_submission_letter: str
    multiple_submission_name: str
    joint_submission: str
    ref_impact_case_study_identifier: str
    title: str
    is_continued_from_2014: bool
    summary_impact_type: str
    countries_iso3: Set = field(default_factory=set)
    formal_partners: Set = field(default_factory=set)
    funding_programmes: Set = field(default_factory=set)
    global_research_identifiers: Set = field(default_factory=set)
    name_of_funders: Set = field(default_factory=set)
    researcher_orcids: Set = field(default_factory=set)
    grant_funding: Set = field(default_factory=set)
    details: List[ImpactDetail] = field(default_factory=list)

    @classmethod
    def from_dataframe_row(cls, row):
        return cls(
            institution_ukprn_code=row["Institution UKPRN code"],
            institution_name=row["Institution name"],
            main_panel=row["Main panel"],
            unit_of_assessment_number=row["Unit of assessment number"],
            unit_of_assessment_name=row["Unit of assessment name"],
            multiple_submission_letter=row["Multiple submission letter"],
            multiple_submission_name=row["Multiple submission name"],
            joint_submission=row["Joint submission"],
            ref_impact_case_study_identifier=row["REF impact case study identifier"],
            title=row["Title"],
            is_continued_from_2014=row["Is continued from 2014"],
            summary_impact_type=row["Summary impact type"],
            countries_iso3={row["Countries"]},
            formal_partners=clean_list(row["Formal partners"]),
            funding_programmes=clean_list(row["Funding programmes"]),
            global_research_identifiers=clean_list(row["Global research identifiers"]),
            name_of_funders=clean_list(row["Name of funders"]),
            researcher_orcids=clean_list(row["Researcher ORCIDs"]),
            grant_funding=clean_list(row["Grant funding"]),
        )
