# This is the opposite of above, and needs to convert field names when reading from the 
# csv and writing to the database - This should be used in ../scripts/
COLUMN_CONVERSION_MAP_FROM_CSV = {
    "inst_id": "ukprn",
    "Institution name": "institution_name",
    "Main panel": "main_panel",
    "Unit of assessment number": "uoa",
    "Unit of assessment name": "unit_of_assessment_name",
    "Multiple submission letter": "multiple_submission_letter",
    "Multiple submission name": "multiple_submission_name",
    "Joint submission": "joint_submission",
    "REF impact case study identifier": "ics_id",
    "Title": "title",
    "Is continued from 2014": "is_continued_from_2014",
    "Summary impact type": "summary_impact_type",
    "Countries": "countries",
    "Formal partners": "formal_partners",
    "Funding programmes": "funding_programmes",
    "Global research identifiers": "global_research_identifiers",
    "Name of funders": "name_of_funders",
    "Researcher ORCIDs": "researcher_orcids",
    "Grant funding": "grant_funding",
    "1. Summary of the impact": "summary_of_the_impact",
    "2. Underpinning research": "underpinning_research",
    "3. References to the research": "references_to_the_research",
    "4. Details of the impact": "details_of_the_impact",
    "5. Sources to corroborate the impact": "sources_to_corroborate_the_impact",
    "COVID-19 Statement": "covid_statement",
    "fte": "fte",
    "num_doc_degrees_total": "num_doc_degrees_total",
    "av_income": "av_income",
    "tot_income": "tot_income",
    "tot_inc_kind": "tot_inc_kind",
    "ICS_GPA": "ics_gpa",
    "Environment_GPA": "environment_gpa",
    "Output_GPA": "output_gpa",
    "Overall_GPA": "overall_gpa",
    "Post Code": "post_code",
    "inst_postcode_district": "inst_postcode_district",
    "inst_postcode_area": "postcode",
    "ics_url": "ics_url",
    "countries_extracted": "countries_iso3",
    "region_extracted": "region_extracted",
    "union_extracted": "union_extracted",
    "funders_extracted": "funders_extracted",
    "Underpinning research subject tag values": "underpinning_research_subject_tag_values",
    "Underpinning research subject tag group": "underpinning_research_subject_tag_group",
    "UK Region tag values": "uk_region_tag_values",
    "UK Region tag group": "uk_region_tag_group",
    "scientometric_data": "scientometric_data",
    "BERT_topic": "bert_topic",
    "BERT_prob": "bert_prob",
    "BERT_topic_terms": "bert_topic_terms",
    "BERT_topic_term_1": "bert_topic_term_1",
    "BERT_topic_term_2": "bert_topic_term_2",
    "BERT_topic_term_3": "bert_topic_term_3",
    "BERT_topic_term_4": "bert_topic_term_4",
    "BERT_topic_term_5": "bert_topic_term_5",
    "BERT_topic_term_6": "bert_topic_term_6",
    "BERT_topic_term_7": "bert_topic_term_7",
    "BERT_topic_term_8": "bert_topic_term_8",
    "BERT_topic_term_9": "bert_topic_term_9",
    "BERT_topic_term_10": "bert_topic_term_10",
    "max_prob": "max_prob",
    "reassigned": "reassigned",
    "reassignment": "reassignment",
    "final_topic": "final_topic",
    "reassignment_notes": "reassignment_notes",
    "topic_id": "topic_id",
    "cluster_id": "cluster_id",
    "topic_name": "topic_name",
    "topic_name_short": "topic_name_short",
    "cluster_name": "cluster_name",
    "cluster_name_short": "cluster_name_short",
    "topic_description": "topic_description",
    "s1_flesch_score": "s1_flesch_score",
    "s2_flesch_score": "s2_flesch_score",
    "s3_flesch_score": "s3_flesch_score",
    "s4_flesch_score": "s4_flesch_score",
    "s5_flesch_score": "s5_flesch_score",
    "flesch_score": "flesch_score",
    "s1_np_count": "s1_np_count",
    "s1_vp_count": "s1_vp_count",
    "s2_np_count": "s2_np_count",
    "s2_vp_count": "s2_vp_count",
    "s3_np_count": "s3_np_count",
    "s3_vp_count": "s3_vp_count",
    "s4_np_count": "s4_np_count",
    "s4_vp_count": "s4_vp_count",
    "s5_np_count": "s5_np_count",
    "s5_vp_count": "s5_vp_count",
    "s1_sentiment_score": "s1_sentiment_score",
    "s2_sentiment_score": "s2_sentiment_score",
    "s3_sentiment_score": "s3_sentiment_score",
    "s4_sentiment_score": "s4_sentiment_score",
    "s5_sentiment_score": "s5_sentiment_score",
    "sentiment_score": "sentiment_score"
}


GLOBAL_ISOS = [
    'CUB',
    'DOM',
    'NIC',
    'GTM',
    'MAF',
    'SXM',
    'HTI',
    'CRI',
    'SLV',
    'BLZ',
    'PAN',
    'GRL',
    'HND',
    'CUW',
    'ABW',
    'MEX',
    'BHS',
    'CAN',
    'USA',
    'SPM',
    'TTO',
    'TCA',
    'GRD',
    'BRB',
    'LCA',
    'VCT',
    'DMA',
    'BLM',
    'MSR',
    'KNA',
    'AIA',
    'VIR',
    'JAM',
    'ATG',
    'PRI',
    'VGB',
    'CYM',
    'BOL',
    'CHL',
    'BMU',
    'GUY',
    'SUR',
    'PER',
    'ARG',
    'BRA',
    'ECU',
    'PRY',
    'URY',
    'COL',
    'FLK',
    'VEN',
    'CYP',
    'IDN',
    'ISR',
    'IND',
    'MYS',
    'PSE',
    'CHN',
    'LBN',
    'SYR',
    'PRK',
    'KOR',
    'BTN',
    'OMN',
    'KAZ',
    'MNG',
    'UZB',
    'VNM',
    'KHM',
    'TJK',
    'AZE',
    'GEO',
    'ARE',
    'LAO',
    'ARM',
    'IRQ',
    'TUR',
    'KGZ',
    'QAT',
    'IRN',
    'SAU',
    'TLS',
    'THA',
    'KWT',
    'PAK',
    'BRN',
    'MMR',
    'BGD',
    'TKM',
    'JOR',
    'AFG',
    'HKG',
    'NPL',
    'CYN',
    'YEM',
    'KAS',
    'PHL',
    'LKA',
    'AU1',
    'SGP',
    'JPN',
    'BHR',
    'TWN',
    'MAC',
    'SOM',
    'SSD',
    'ETH',
    'KEN',
    'MWI',
    'SOL',
    'MAR',
    'TZA',
    'ESH',
    'COG',
    'NAM',
    'ZAF',
    'TUN',
    'ZMB',
    'GIN',
    'SLE',
    'COD',
    'LBR',
    'CAF',
    'LBY',
    'SDN',
    'DJI',
    'ERI',
    'AGO',
    'SEN',
    'MLI',
    'BEN',
    'NGA',
    'CIV',
    'TCD',
    'DZA',
    'BWA',
    'BDI',
    'MOZ',
    'RWA',
    'UGA',
    'ZWE',
    'SWZ',
    'LSO',
    'GAB',
    'CMR',
    'NER',
    'TGO',
    'EGY',
    'GNB',
    'BFA',
    'GHA',
    'MRT',
    'GNQ',
    'COM',
    'STP',
    'MDG',
    'GMB',
    'CPV',
    'BLR',
    'FRA',
    'LTU',
    'DEU',
    'EST',
    'SWE',
    'LVA',
    'CZE',
    'FIN',
    'NOR',
    'LUX',
    'BEL',
    'MKD',
    'ALB',
    'XXK',
    'ESP',
    'SVK',
    'DNK',
    'HUN',
    'ROU',
    'GBR',
    'POL',
    'AUT',
    'IRL',
    'ITA',
    'GRC',
    'CHE',
    'HRV',
    'NLD',
    'LIE',
    'SRB',
    'BGR',
    'SVN',
    'MCO',
    'AND',
    'SMR',
    'PRT',
    'BIH',
    'VAT',
    'MNE',
    'MDA',
    'ISL',
    'JEY',
    'GGY',
    'MLT',
    'IMN',
    'FRO',
    'PNG',
    'AUS',
    'FJI',
    'ALA',
    'NZL',
    'NCL',
    'PCN',
    'PYF',
    'COK',
    'MHL',
    'NFK',
    'TON',
    'KIR',
    'WSM',
    'WLF',
    'SLB',
    'TUV',
    'NRU',
    'FSM',
    'ASM',
    'NIU',
    'PLW',
    'VUT',
    'GUM',
    'ATC',
    'MNP',
    'RUS',
    'UKR',
    'MDV',
    'MUS',
    'SYC']

EU_COUNTRIES = [
    "AUT",  # Austria
    "BEL",  # Belgium
    "BGR",  # Bulgaria
    "HRV",  # Croatia
    "CYP",  # Cyprus
    "CZE",  # Czech Republic
    "DNK",  # Denmark
    "EST",  # Estonia
    "FIN",  # Finland
    "FRA",  # France
    "DEU",  # Germany
    "GRC",  # Greece
    "HUN",  # Hungary
    "IRL",  # Ireland
    "ITA",  # Italy
    "LVA",  # Latvia
    "LTU",  # Lithuania
    "LUX",  # Luxembourg
    "MLT",  # Malta
    "NLD",  # Netherlands
    "POL",  # Poland
    "PRT",  # Portugal
    "ROU",  # Romania
    "SVK",  # Slovakia
    "SVN",  # Slovenia
    "ESP",  # Spain
    "SWE",  # Sweden
]

ALL_EUROPE_COUNTRIES = [
    "ALB",  # Albania
    "AND",  # Andorra
    "ARM",  # Armenia
    "AUT",  # Austria
    "AZE",  # Azerbaijan
    "BLR",  # Belarus
    "BEL",  # Belgium
    "BIH",  # Bosnia and Herzegovina
    "BGR",  # Bulgaria
    "HRV",  # Croatia
    "CYP",  # Cyprus
    "CZE",  # Czech Republic
    "DNK",  # Denmark
    "EST",  # Estonia
    "FIN",  # Finland
    "FRA",  # France
    "GEO",  # Georgia
    "DEU",  # Germany
    "GRC",  # Greece
    "HUN",  # Hungary
    "ISL",  # Iceland
    "IRL",  # Ireland
    "ITA",  # Italy
    "KAZ",  # Kazakhstan
    "KOS",  # Kosovo
    "LVA",  # Latvia
    "LIE",  # Liechtenstein
    "LTU",  # Lithuania
    "LUX",  # Luxembourg
    "MKD",  # North Macedonia
    "MLT",  # Malta
    "MCO",  # Monaco
    "MNE",  # Montenegro
    "NLD",  # Netherlands
    "NOR",  # Norway
    "POL",  # Poland
    "PRT",  # Portugal
    "ROU",  # Romania
    "RUS",  # Russia
    "SMR",  # San Marino
    "SRB",  # Serbia
    "SVK",  # Slovakia
    "SVN",  # Slovenia
    "ESP",  # Spain
    "SWE",  # Sweden
    "CHE",  # Switzerland
    "TUR",  # Turkey
    "UKR",  # Ukraine
    "GBR",  # United Kingdom
    "VAT",  # Vatican City (Holy See)
]