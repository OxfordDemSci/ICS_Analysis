from sqlalchemy import ARRAY, Column, Float, Index, Integer, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()  # type: ignore


class ICS(Base):  # type: ignore
    __tablename__ = "ics"

    id = Column(Integer, primary_key=True)
    ukprn = Column(Integer)
    institution_name = Column(String)
    main_panel = Column(String)
    uoa = Column(String)
    unit_of_assessment_name = Column(String)
    multiple_submission_letter = Column(String)
    multiple_submission_name = Column(String)
    joint_submission = Column(String)
    ics_id = Column(String)
    title = Column(String)
    is_continued_from_2014 = Column(String)
    summary_impact_type = Column(String)
    countries = Column(String)
    formal_partners = Column(String)
    funding_programmes = Column(String)
    global_research_identifiers = Column(String)
    name_of_funders = Column(String)
    researcher_orcids = Column(String)
    grant_funding = Column(String)
    summary_of_the_impact = Column(String)
    underpinning_research = Column(String)
    references_to_the_research = Column(String)
    details_of_the_impact = Column(String)
    sources_to_corroborate_the_impact = Column(String)
    covid_statement = Column(String)
    fte = Column(String)
    num_doc_degrees_total = Column(String)
    av_income = Column(String)
    tot_income = Column(String)
    tot_inc_kind = Column(String)
    ics_gpa = Column(String)
    environment_gpa = Column(String)
    output_gpa = Column(String)
    overall_gpa = Column(String)
    post_code = Column(String)
    inst_postcode_district = Column(String)
    postcode = Column(String)
    ics_url = Column(String)
    countries_iso3 = Column(String)
    countries_specific_extracted = Column(String)   
    region_extracted = Column(String)
    countries_region_extracted = Column(String)
    union_extracted = Column(String)
    countries_union_extracted = Column(String)
    funders_extracted = Column(String)
    underpinning_research_subject_tag_values = Column(String)
    underpinning_research_subject_tag_group = Column(String)
    uk_region_tag_values = Column(String)
    uk_region_tag_group = Column(String)
    scientometric_data = Column(String)
    bert_topic = Column(String)
    bert_prob = Column(String)
    bert_topic_terms = Column(String)
    bert_topic_term_1 = Column(String)
    bert_topic_term_2 = Column(String)
    bert_topic_term_3 = Column(String)
    bert_topic_term_4 = Column(String)
    bert_topic_term_5 = Column(String)
    bert_topic_term_6 = Column(String)
    bert_topic_term_7 = Column(String)
    bert_topic_term_8 = Column(String)
    bert_topic_term_9 = Column(String)
    bert_topic_term_10 = Column(String)
    max_prob = Column(String)
    reassigned = Column(String)
    reassignment = Column(String)
    final_topic = Column(String)
    reassignment_notes = Column(String)
    topic_id = Column(String)
    cluster_id = Column(String)
    topic_name = Column(String)
    topic_name_short = Column(String)
    cluster_name = Column(String)
    cluster_name_short = Column(String)
    topic_description = Column(String)
    s1_flesch_score = Column(String)
    s2_flesch_score = Column(String)
    s3_flesch_score = Column(String)
    s4_flesch_score = Column(String)
    s5_flesch_score = Column(String)
    flesch_score = Column(String)
    s1_np_count = Column(String)
    s1_vp_count = Column(String)
    s2_np_count = Column(String)
    s2_vp_count = Column(String)
    s3_np_count = Column(String)
    s3_vp_count = Column(String)
    s4_np_count = Column(String)
    s4_vp_count = Column(String)
    s5_np_count = Column(String)
    s5_vp_count = Column(String)
    s1_sentiment_score = Column(String)
    s2_sentiment_score = Column(String)
    s3_sentiment_score = Column(String)
    s4_sentiment_score = Column(String)
    s5_sentiment_score = Column(String)
    sentiment_score = Column(String)

    __table_args__ = (Index("idx_ics_id", "id", "ics_id"),)


class Topics(Base):  # type: ignore
    __tablename__ = "topics"

    topic_id = Column(Integer, primary_key=True)
    group_id = Column(Integer)
    topic_group = Column(String)
    topic_name = Column(String)
    topic_name_long = Column(String)
    description = Column(String)
    narrative = Column(String)
    keywords = Column(String)

    __table_args__ = (Index("idx_topics_id", "topic_id", unique=True),)


class TopicWeights(Base):  # type: ignore
    __tablename__ = "topic_weights"

    id = Column(Integer, primary_key=True)
    ics_id = Column(String)
    topic_id = Column(Integer)
    probability = Column(Float)

    __table_args__ = (Index("idx_topic_weights_id", "id", unique=True),)


class TopicGroups(Base):  # type: ignore
    __tablename__ = "topic_groups"

    group_id = Column(Integer, primary_key=True)
    topic_group = Column(String)
    topic_group_long = Column(String)
    description = Column(String)
    narrative = Column(String)

    __table__args = (Index("idx_topic_groups", "group_id", unique=True),)


class Funder(Base):  # type: ignore
    __tablename__ = "funder"

    id = Column(Integer, primary_key=True)
    ics_table_id = Column(Integer)
    funder = Column(String)

    __table_args__ = (Index("idx_funder_id", "id", unique=True),)


class UOA(Base):  # type: ignore
    __tablename__ = "uoa"

    id = Column(Integer, primary_key=True)
    uoa_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    assessment_panel = Column(String(1), nullable=False)
    assessment_group = Column(String(5), nullable=False)

    __table_args__ = (Index("idx_uoa_id", "id", unique=True),)


class Institution(Base):  # type: ignore
    __tablename__ = "institution"

    id = Column(Integer, primary_key=True)
    ukprn = Column(Integer)
    name = Column(String)
    postcode = Column(String(8))


class Countries(Base):  # type: ignore
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    ics_table_id = Column(Integer)
    country = Column(String(3))

    __table_args__ = (Index("idx_countries_id", "id", unique=True),)


class UKRegions(Base):  # type: ignore
    __tablename__ = "uk_regions"

    id = Column(Integer, primary_key=True)
    ics_table_id = Column(Integer)
    uk_region_tag_values = Column(String)

    __table_args__ = (Index("idx_uk_regions_id", "id", unique=True),)


class RegionsGeometry(Base):  # type: ignore
    __tablename__ = "regions_geometry"

    id = Column(Integer)
    placename = Column(String, primary_key=True)
    regions_wkt = Column(String)

    __table_args__ = (Index("idx_regions_geom_idx", "placename", unique=True),)


class WebsiteText(Base):  # type: ignore
    """One row table with place holders for text to be shown on the page."""

    __tablename__ = "websitetext"

    id = Column(Integer, primary_key=True, autoincrement=True)
    all_topics_description = Column(String)
    about = Column(String)
    instructions = Column(String)
    team = Column(String)
    contact = Column(String)
    label_info_box = Column(String)
    label_top_left_box = Column(String)
    label_bottom_left_box = Column(String)
    label_top_right_box = Column(String)
    label_bottom_right_box = Column(String)
    uk_map_colourramp = Column(ARRAY(String))  # type: ignore
    global_colourramp = Column(ARRAY(String))  # type: ignore
    funders_bar_colour = Column(String)
    uoa_bar_colours = Column(JSON)  # type ignore
