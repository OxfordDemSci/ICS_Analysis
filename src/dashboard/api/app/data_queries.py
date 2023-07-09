from sqlalchemy import text
from collections import defaultdict
from geoalchemy2 import shape

from app import db

from app.models import (
    WebsiteText,
    ICS,
)
def get_topics():
    sql = text('''
        SELECT topic_name, topic_group, description, narrative from topics
    ''')

    query = db.session.execute(sql)
    topics = [{
        "topic_name": row.topic_name, 
        "topic_group": row.topic_group, 
        "description": row.description,
        "narrative": row.narrative} for row in query]
    topics.insert(0, {
        "topic_name": "All Topics", 
        "topic_group": None, 
        "description": None,
        "narrative": None,
    })
    return topics

def get_website_text():
    row = db.session.query(WebsiteText).first()

    website_text = {
        "all_topics_description": row.all_topics_description,
        "about": row.about,
        "instructions": row.instructions,
        "team": row.team,
        "contact": row.contact,
        "label_info_box": row.label_info_box,
        "label_top_left_box": row.label_top_left_box,
        "label_bottom_left_box": row.label_bottom_left_box,
        "label_top_right_box": row.label_top_right_box,
        "label_botton_right_box": row.label_botton_right_box,
    }
    return website_text

def get_ics_table(ics_ids=None):
    if ics_ids is None:
        rows = db.session.query(ICS).all()
    else:
        rows = db.session.query(ICS).filter(ICS.ics_id.in_(ics_ids)).all()
    ics_table = []
    for row in rows:
        ics_table.append({column.name: getattr(row, column.name) for column in ICS.__table__.columns})
    return ics_table

def get_ics_table_for_country(country, topic, threshold, postcode=None):
    ics_ids = get_ics_ids(topic, threshold, postcode)
    sql = text('''
               SELECT * FROM ics i
               JOIN countries c
               ON i.id = c.ics_table_id
               WHERE c.country = :country
               AND i.ics_id = ANY(:ics_ids)     
    ''')
    query = db.session.execute(sql, {"country": country, "ics_ids": ics_ids})
    ics_table = [{
        "id": row.id,
        "ukprn": row.ukprn,
        "postcode": row.postcode,
        "ics_id": row.ics_id,
        "uos": row.uoa
    } for row in query]
    return ics_table

def get_funders_counts(ics_ids=None):
    if ics_ids is None:
        sql = text('''
            SELECT funder.funder as funder, COUNT(*) AS funder_count FROM funder funder where funder is not NULL
            GROUP BY funder.funder order by funder_count desc;
        ''')
        query = db.session.execute(sql)
    else:
        sql = text('''
            SELECT f.funder AS funder, COUNT(*) AS funder_count
            FROM funder f
            JOIN ics i ON f.ics_table_id = i.id
            WHERE i.ics_id = ANY(:ics_ids)
            GROUP BY f.funder
            ORDER BY funder_count DESC
        ''')
        query = db.session.execute(sql, {"ics_ids": ics_ids})
    funders = [{
        "funder": row.funder,
        "funder_count": row.funder_count
    } for row in query]
    return funders


def get_countries_counts(ics_ids=None):
    if ics_ids is None:
        sql = text('''
            SELECT countries.country as country, count(*) as country_count from countries countries where not country is NULL
            GROUP BY countries.country order by country_count desc
        ''')
        query = db.session.execute(sql)
    else:
        sql = text('''
           SELECT c.country AS country, COUNT(*) AS country_count
            FROM countries c
            JOIN ics i ON c.ics_table_id = i.id
            WHERE i.ics_id = ANY(:ics_ids)
            GROUP BY c.country
            ORDER BY country_count DESC 
        ''')
        query = db.session.execute(sql, {"ics_ids": ics_ids})
    countries = [{
        "country": row.country,
        "country_count": row.country_count
    } for row in query]
    return countries

def get_uoa_counts(ics_ids=None):
    if ics_ids is None:
        sql = text('''
            SELECT ics.uoa as uoa, uoa.name as name, COUNT(*) AS uoa_count FROM ics ics JOIN uoa ON ics.uoa = uoa.uoa_id GROUP BY ics.uoa, 
            uoa.name ORDER BY uoa_count desc;
        ''')
        query = db.session.execute(sql)
        uoa = [{
            "name": row.name,
            "uoa_count": row.uoa_count
        } for row in query]
    elif len(ics_ids) > 0:
        sql = text('''
            SELECT ics.uoa AS uoa, uoa.name AS name, uoa.assessment_panel as assessment, COUNT(*) AS uoa_count
            FROM ics ics
            JOIN uoa uoa ON ics.uoa = uoa.uoa_id
            WHERE ics.ics_id IN (SELECT unnest(:ics_ids))
            GROUP BY ics.uoa, uoa.name, uoa.assessment_panel
            ORDER BY uoa_count DESC;
        ''')
        query = db.session.execute(sql, {"ics_ids": ics_ids})
        uoa = [{
            "name": row.name,
            "assessment": row.assessment,
            "uoa_count": row.uoa_count
        } for row in query]
    else:
        uoa = []
    return uoa


def get_institution_counts(ics_ids=None):
    if ics_ids is None:
        sql = text('''
            SELECT ics.ukprn as ukprn, ics.postcode as postcode, ins.name as institution, COUNT(*) AS inst_count FROM ics 
            ics JOIN institution ins ON ics.ukprn = ins.ukprn GROUP BY ics.postcode,ics.ukprn, ins.name ORDER BY inst_count desc;
        ''')
        query = db.session.execute(sql)
    else:
        sql = text('''
            SELECT ics.ukprn as ukprn, ics.postcode as postcode, ins.name as institution, COUNT(*) AS inst_count FROM ics 
            ics JOIN institution ins ON ics.ukprn = ins.ukprn AND ics.ics_id = ANY(:ics_ids) GROUP BY ics.postcode,ics.ukprn, ins.name ORDER BY inst_count desc;
        ''')
        query = db.session.execute(sql, {"ics_ids": ics_ids})
    institutions = defaultdict(dict)
    for row in query:
        postcode = row.postcode
        institution = row.institution
        inst_count = row.inst_count
        institutions[postcode][institution] = inst_count
    for key in institutions.keys():
        inst_total = 0
        for _, value in institutions[key].items():
            inst_total += value
        institutions[key]['Total'] = inst_total
    return institutions

def get_topic_and_ics_above_threshold(topic, threshold, postcode):
    postcode_level_data = {}
    sql = text('''
        SELECT tw.ics_id FROM topic_weights tw 
        JOIN topics t ON tw.topic_id = t.topic_id
        JOIN ics i ON tw.ics_id = i.ics_id
        WHERE t.topic_name = :topic AND tw.probability >= :threshold
        AND i.postcode = :postcode;
    ''')
    query = db.session.execute(sql, {"topic": topic, "threshold": threshold, "postcode": postcode})
    ics_ids = [row.ics_id for row in query]
    postcode_level_data["countries_counts"] = get_countries_counts(ics_ids=ics_ids)
    postcode_level_data["funders_counts"] = get_funders_counts(ics_ids=ics_ids)
    postcode_level_data["uoa_counts"] = get_uoa_counts(ics_ids=ics_ids)
    postcode_level_data["institution_counts"] = get_institution_counts(ics_ids=ics_ids)
    return postcode_level_data

def query_dashboard_data(topic, threshold, postcode=None):
    data = {}
    ics_ids = get_ics_ids(topic, threshold, postcode)
    data["countries_counts"] = get_countries_counts(ics_ids=ics_ids)
    data["funders_counts"] = get_funders_counts(ics_ids=ics_ids)
    data["uoa_counts"] = get_uoa_counts(ics_ids=ics_ids)
    data["institution_counts"] = get_institution_counts(ics_ids=ics_ids)
    data["ics_table"] = get_ics_table(ics_ids=ics_ids)
    return data

def get_ics_ids(topic, threshold, postcode=None):
    sql = get_ics_sql(topic, postcode)
    query = db.session.execute(sql, {"topic": topic, "threshold": threshold, "postcode": postcode})
    ics_ids = [row.ics_id for row in query]
    return ics_ids

def get_ics_sql(topic, postcode=None):
    if (topic == "All Topics") and (postcode is not None):
        sql = text('''
        SELECT tw.ics_id FROM topic_weights tw 
        JOIN topics t ON tw.topic_id = t.topic_id
        JOIN ics i ON tw.ics_id = i.ics_id
        WHERE tw.probability >= :threshold
        AND i.postcode = :postcode;
    ''')
    elif (topic == "All Topics") and postcode is None:
        sql = text('''
        SELECT tw.ics_id FROM topic_weights tw 
        JOIN topics t ON tw.topic_id = t.topic_id
        JOIN ics i ON tw.ics_id = i.ics_id
        WHERE tw.probability >= :threshold;
    ''')
    elif (topic != "All Topics") and postcode is not None:
        sql = text('''
        SELECT tw.ics_id FROM topic_weights tw 
        JOIN topics t ON tw.topic_id = t.topic_id
        JOIN ics i ON tw.ics_id = i.ics_id
        WHERE t.topic_name = :topic AND tw.probability >= :threshold
        AND i.postcode = :postcode;
    ''')
    else:
        sql = text('''
        SELECT tw.ics_id FROM topic_weights tw 
        JOIN topics t ON tw.topic_id = t.topic_id
        JOIN ics i ON tw.ics_id = i.ics_id
        WHERE t.topic_name = :topic AND tw.probability >= :threshold
    ''')
    return sql
    