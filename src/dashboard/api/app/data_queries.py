from sqlalchemy import text
from collections import defaultdict
from geoalchemy2 import shape
from flask import make_response
from io import StringIO
import csv

from app import db

from app.models import (
    WebsiteText,
    ICS,
)
def get_topics(topic=None):
    if topic is None:
        sql = text('''
            SELECT topic_name, topic_group, description, narrative from topics
        ''')
    else:
        sql = text('''
            SELECT topic_name, topic_group, description, narrative from topics 
                   WHERE topic_name = :topic
        ''')
    params = {"topic": topic}
    query = db.session.execute(sql, params)
    topics = [{
        "topic_name": row.topic_name, 
        "topic_group": row.topic_group, 
        "description": row.description,
        "narrative": row.narrative} for row in query]
    if (topic is None):
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
        "label_bottom_right_box": row.label_bottom_right_box,
    }
    return website_text

def get_pdf_data(threshold, topic=None, postcode_area=None, beneficiary=None, uoa=None, funder=None):
    pdf_data = {}
    pdf_data["topic"] = get_topics(topic)
    pdf_data["background_text"] = get_website_text()
    pdf_data["ics_data"] = query_dashboard_data(threshold,
                                                topic,
                                                postcode_area,
                                                beneficiary,
                                                uoa,
                                                funder)
    return pdf_data

def get_ics_table(ics_ids=None, limit=None):
    if ics_ids is None:
        if limit is None:   
            rows = db.session.query(ICS).all()
        else:
            rows = db.session.query(ICS).limit(limit).all()
    else:
        if limit is None:
            rows = db.session.query(ICS).filter(ICS.ics_id.in_(ics_ids)).all()
        else:
            rows =  db.session.query(ICS).filter(ICS.ics_id.in_(ics_ids)).limit(limit).all()
    ics_table = []
    for row in rows:
        ics_table.append({column.name: getattr(row, column.name) for column in ICS.__table__.columns})
    return ics_table

def download_ics_table(threshold, topic=None, postcode=None, country=None, uoa=None, funder=None, limit=None):
    ics_ids = get_ics_ids(threshold, topic, postcode, country, uoa, funder)
    rows = db.session.query(ICS).filter(ICS.ics_id.in_(ics_ids)).all()
    csv_data = StringIO()
    writer = csv.writer(csv_data)
    header = [column.name for column in ICS.__table__.columns]
    writer.writerow(header)
    for row in rows:
        data = [str(getattr(row, column.name)) for column in ICS.__table__.columns]
        writer.writerow(data)
    response = make_response(csv_data.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=ICSTable.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response



def get_ics_table_for_country(threshold, topic=None, postcode=None, country=None, uoa=None, funder=None, limit=None):
    ics_ids = get_ics_ids(threshold, topic, postcode, country, uoa, funder)
    sql = text('''
               SELECT * FROM ics i
               JOIN countries c
               ON i.id = c.ics_table_id
               WHERE c.country = :country
               AND i.ics_id = ANY(:ics_ids)     
    ''')
    if limit is None:
        query = db.session.execute(sql, {"country": country, "ics_ids": ics_ids})
    else:
        query = db.session.execute(sql, {"country": country, "ics_ids": ics_ids}).fetchmany(limit)
    ics_table = []
    for row in query:
        ics_table.append({column.name: getattr(row, column.name) for column in ICS.__table__.columns})
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
            SELECT ics.uoa as uoa, uoa.name as name, uoa.assessment_panel as assessment_panel, uoa.assessment_group as
                assessment_group, COUNT(*) AS uoa_count FROM ics ics JOIN uoa ON ics.uoa = uoa.uoa_id GROUP BY ics.uoa,
                uoa.name, uoa.assessment_panel, uoa.assessment_group ORDER BY uoa_count desc;
        ''')
        query = db.session.execute(sql)
        uoa = [{
            "name": row.name,
            "assessment_panel": row.assessment_panel,
            "assessment_group": row.assessment_group,
            "uoa_count": row.uoa_count
        } for row in query]
    elif len(ics_ids) > 0:
        sql = text('''
            SELECT ics.uoa AS uoa, uoa.name AS name, uoa.assessment_panel as assessment_panel, uoa.assessment_group as assessment_group, COUNT(*) AS uoa_count
            FROM ics ics
            JOIN uoa uoa ON ics.uoa = uoa.uoa_id
            WHERE ics.ics_id = ANY(:ics_ids)
            GROUP BY ics.uoa, uoa.name, uoa.assessment_panel, uoa.assessment_group
            ORDER BY uoa_count DESC;
        ''')
        query = db.session.execute(sql, {"ics_ids": ics_ids})
        uoa = [{
            "name": row.name,
            "assessment_panel": row.assessment_panel,
            "assessment_group": row.assessment_group,
            "uoa_count": row.uoa_count
        } for row in query]
    else:
        uoa = []
    return uoa


def nested_defaultdict():
    return defaultdict(nested_defaultdict)


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
    #institutions = defaultdict(dict)
    institutions = defaultdict(nested_defaultdict)
    for row in query:
        postcode = row.postcode
        institution = row.institution
        inst_count = row.inst_count
        institutions[postcode]['institution_counts'][institution] = inst_count
    for key in institutions.keys():
        inst_total = 0
        for _, value in institutions[key]['institution_counts'].items():
            inst_total += value
        institutions[key]['postcode_total'] = inst_total
    return institutions


def query_dashboard_data(threshold, topic=None, postcode=None, beneficiary=None, uoa=None, funder=None):
    data = {}
    ics_ids = get_ics_ids(threshold, topic, postcode, beneficiary, uoa, funder)
    data["countries_counts"] = get_countries_counts(ics_ids=ics_ids)
    data["funders_counts"] = get_funders_counts(ics_ids=ics_ids)
    data["uoa_counts"] = get_uoa_counts(ics_ids=ics_ids)
    data["institution_counts"] = get_institution_counts(ics_ids=ics_ids)
    data["ics_table"] = get_ics_table(ics_ids=ics_ids, limit=500)
    return data

def get_ics_ids(threshold, topic=None, postcode=None, beneficiary=None, uoa=None, funder=None):
    sql = get_ics_sql(topic, postcode, beneficiary, uoa, funder)
    argument_names = ["threshold", "topic", "postcode", "beneficiary", "uoa", "funder"]
    arguments = [threshold, topic, postcode, beneficiary, uoa, funder]
    params = {arg_name: arg_val for arg_name, arg_val in zip(argument_names, arguments) if arg_val is not None}
    query = db.session.execute(sql, params)
    ics_ids = [row.ics_id for row in query]
    return ics_ids

def get_ics_sql(topic=None, postcode=None, beneficiary=None, uoa=None, funder=None):
    sql_str = ('''
        SELECT DISTINCT(tw.ics_id) FROM topic_weights tw 
        JOIN topics t ON tw.topic_id = t.topic_id
        JOIN ics i ON tw.ics_id = i.ics_id
        JOIN uoa u ON u.uoa_id = i.uoa
        JOIN funder f ON f.ics_table_id = i.id
        JOIN countries c ON c.ics_table_id = i.id
        WHERE tw.probability >= :threshold
    ''')
    if topic is not None:
        sql_str += " AND t.topic_name = :topic"
    if postcode is not None:
        sql_str += " AND i.postcode = :postcode"
    if beneficiary is not None:
        sql_str += " AND c.country = :beneficiary"
    if uoa is not None:
        if uoa in ["A", "B", "C", "D"]:
            sql_str += " AND u.assessment_panel = :uoa"
        elif uoa in ["STEM", "SHAPE"]:
            sql_str += " AND u.assessment_group = :uoa"
    if funder is not None:
        sql_str += " AND f.funder = :funder"

        


    print(sql_str)
    # if (topic == "All Topics") and (postcode is not None):
    #     sql = text('''
    #     SELECT tw.ics_id FROM topic_weights tw 
    #     JOIN topics t ON tw.topic_id = t.topic_id
    #     JOIN ics i ON tw.ics_id = i.ics_id
    #     WHERE tw.probability >= :threshold
    #     AND i.postcode = :postcode;
    # ''')
    # elif (topic == "All Topics") and postcode is None:
    #     sql = text('''
    #     SELECT tw.ics_id FROM topic_weights tw 
    #     JOIN topics t ON tw.topic_id = t.topic_id
    #     JOIN ics i ON tw.ics_id = i.ics_id
    #     WHERE tw.probability >= :threshold;
    # ''')
    # elif (topic != "All Topics") and postcode is not None:
    #     sql = text('''
    #     SELECT tw.ics_id FROM topic_weights tw 
    #     JOIN topics t ON tw.topic_id = t.topic_id
    #     JOIN ics i ON tw.ics_id = i.ics_id
    #     WHERE t.topic_name = :topic AND tw.probability >= :threshold
    #     AND i.postcode = :postcode;
    # ''')
    # else:
    #     sql = text('''
    #     SELECT tw.ics_id FROM topic_weights tw 
    #     JOIN topics t ON tw.topic_id = t.topic_id
    #     JOIN ics i ON tw.ics_id = i.ics_id
    #     WHERE t.topic_name = :topic AND tw.probability >= :threshold
    # ''')
    sql = text(sql_str)
    return sql
    