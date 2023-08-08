from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String, ARRAY, Float, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ICS(Base):
    __tablename__ = "ics"

    id = Column(Integer, primary_key=True)
    ukprn = Column(Integer)
    institution_name = Column(String)
    main_panel = Column(String)
    unit_of_assessment_number = Column(String)
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
    uoa = Column(Integer)
    countries_iso3 = Column(String)
    inst_postcode = Column(String)
    inst_postcode_district = Column(String)
    postcode = Column(String)
    ics_url = Column(String)

    __table_args__ = (Index("idx_ics_id", "id", "ics_id"),)


class Topics(Base):
    __tablename__ = "topics"

    topic_id = Column(Integer, primary_key=True)
    group_id = Column(Integer)
    topic_group = Column(String)
    topic_name = Column(String)
    description = Column(String)
    narrative = Column(String)
    keywords = Column(String)
    charlie_suggested = Column(String)
    topic_name_long = Column(String)
    hierarchical_grouping = Column(String)
    cluster_name = Column(String)
    cluster = Column(String)
    topic_notes = Column(String)

    __table_args__ = (Index("idx_topics_id", "topic_id", unique=True),)


class TopicWeights(Base):
    __tablename__ = "topic_weights"

    id = Column(Integer, primary_key=True)
    ics_id = Column(String)
    topic_id = Column(Integer)
    probability = Column(Float)

    __table_args__ = (Index("idx_topic_weights_id", "id", unique=True),)


class TopicGroups(Base):
    __tablename__ = "topic_groups"

    group_id = Column(Integer, primary_key=True)
    topic_group = Column(String)
    description = Column(String)
    narrative = Column(String)

    __table__args = (Index("idx_topic_groups", "group_id", unique=True),)


class Funder(Base):
    __tablename__ = "funder"

    id = Column(Integer, primary_key=True)
    ics_table_id = Column(Integer)
    funder = Column(String)

    __table_args__ = (Index("idx_funder_id", "id", unique=True),)


class UOA(Base):
    __tablename__ = "uoa"

    id = Column(Integer, primary_key=True)
    uoa_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    assessment_panel = Column(String(1), nullable=False)
    assessment_group = Column(String(5), nullable=False)

    __table_args__ = (Index("idx_uoa_id", "id", unique=True),)


class Institution(Base):
    __tablename__ = "institution"

    id = Column(Integer, primary_key=True)
    ukprn = Column(Integer)
    name = Column(String)
    postcode = Column(String(8))


class Countries(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    ics_table_id = Column(Integer)
    country = Column(String(3))

    __table_args__ = (Index("idx_countries_id", "id", unique=True),)


class WebsiteText(Base):
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
    uk_map_colourramp = Column(ARRAY(String))
    global_colourramp = Column(ARRAY(String))
    funders_bar_colour = Column(String)
