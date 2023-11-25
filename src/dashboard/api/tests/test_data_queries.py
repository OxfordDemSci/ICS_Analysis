import json
from pathlib import Path

import pandas as pd  # type: ignore
import pytest

from app.data_queries import (get_ics_ids, get_topic_groups, get_topics,
                              get_website_text, query_dashboard_data)

from .make_test_data import make_query_table

TEST_DATA = Path(__file__).resolve().parent.joinpath("test_data")


@pytest.fixture
def dataframes():
    dfs = {}
    for csv in TEST_DATA.iterdir():
        dfs[csv.stem] = pd.read_csv(csv)
    yield dfs


@pytest.mark.parametrize(
    "topic",
    [
        (None),
        ("Body Image & Media"),
        ("Health & Wellbeing"),
        ("Gaelic Preservation"),
        ("Cultural Engagement"),
    ],
)
def test_get_topics(session, dataframes, topic):
    topics_df = dataframes["TOPICS_TABLE"]
    topics = get_topics(topic=topic)
    if topic is not None:
        topics_df = topics_df[topics_df.topic_name == topic]
    topic_names = [
        x["topic_name"] for x in topics if not x["topic_name"] == "All Topics"
    ]
    topic_groups = [
        x["topic_group"] for x in topics if not x["topic_name"] == "All Topics"
    ]
    topic_keywords = [
        x["keywords"] for x in topics if not x["topic_name"] == "All Topics"
    ]
    assert sorted(topic_names) == sorted(topics_df.topic_name.tolist())
    assert sorted(topic_groups) == sorted(topics_df.topic_group.tolist())
    assert sorted(topic_keywords) == sorted(topics_df.keywords.tolist())
    if topic is None:
        assert "All Topics" in [x["topic_name"] for x in topics]


def test_get_topic_groups(session, dataframes):
    topic_groups_df = dataframes["TOPIC_GROUPS_TABLE"]
    topic_groups = get_topic_groups()
    topic_groups = [x["topic_group"] for x in topic_groups]
    assert sorted(topic_groups) == sorted(topic_groups_df.topic_group.tolist())


def test_get_website_text(session, dataframes):
    text_df = dataframes["WEBSITE_TEXT"]
    text = get_website_text()
    assert sorted(text.keys()) == sorted([x for x in text_df.columns if not x == "id"])


@pytest.mark.parametrize(
    "threshold, topic, postcode, beneficiary, uoa, funder",
    [
        (0.5, None, None, None, None, None),
        (0.1, None, None, None, None, None),
        (0.9, None, None, None, None, None),
        (0, None, None, None, None, None),
        (1, None, None, None, None, None),
    ],
)
def test_get_ics_ids_with_threshold_only(
    session, dataframes, threshold, topic, postcode, beneficiary, uoa, funder
):
    df_weights = dataframes["TOPIC_WEIGHTS_TABLE"]
    df_weights = df_weights[df_weights.probability >= threshold]
    ics_ids = get_ics_ids(threshold, topic, postcode, beneficiary, uoa, funder)
    assert sorted(ics_ids) == sorted(df_weights.ics_id.unique().tolist())


@pytest.mark.parametrize(
    "threshold, topic",
    [
        (0.5, "Body image & Media"),
        (0.1, "Literature"),
        (0.9, "Music"),
        (0.3, "Business & Entrepreneurialism"),
        (0.4, "Conservation"),
    ],
)
def test_get_ics_ids_with_topic(session, dataframes, threshold, topic):
    df_weights = dataframes["TOPIC_WEIGHTS_TABLE"]
    df_topics = dataframes["TOPICS_TABLE"]
    # breakpoint()
    try:
        topic_id = df_topics.loc[df_topics["topic_name"] == topic, "topic_id"].values[0]
        df_weights = df_weights[
            (df_weights.probability >= threshold) & (df_weights.topic_id == topic_id)
        ]
        ics_expected = sorted(df_weights.ics_id.unique().tolist())
    except KeyError:
        ics_expected = []
    ics_ids = sorted(get_ics_ids(threshold=threshold, topic=topic))
    assert ics_ids == ics_expected


@pytest.mark.parametrize(
    "threshold, beneficiary", [(0.5, "GBR"), (0.1, "FRA"), (0.9, "IDN"), (0.6, "IND")]
)
def test_get_ics_ids_with_beneficiary(session, dataframes, threshold, beneficiary):
    df_weights = dataframes["TOPIC_WEIGHTS_TABLE"]
    ics = dataframes["ICS_DATABASE_TABLE"]
    countries = dataframes["ICS_TO_COUNTRY_LOOKUP_TABLE"]
    countries_ics_ids = (
        countries[countries.country == beneficiary].ics_table_id.unique().tolist()
    )
    ics_ids_from_weights = (
        df_weights[df_weights.probability >= threshold].ics_id.unique().tolist()
    )
    ics_ids_expected = sorted(
        ics[ics.id.isin(countries_ics_ids)].ics_id.unique().tolist()
    )
    ics_expected_union = [x for x in ics_ids_expected if x in ics_ids_from_weights]
    ics_ids = sorted(get_ics_ids(threshold=threshold, beneficiary=beneficiary))
    assert ics_ids == ics_expected_union


@pytest.mark.parametrize("threshold", [(0.5), (0.1), (0.8)])
def test_get_ics_ids_with_merged_df(session, dataframes, threshold):
    filtered_df = make_query_table(dataframes, threshold)
    ics_ids = sorted(get_ics_ids(threshold=threshold))
    ics_ids_expected = sorted(filtered_df.ics_id.unique().tolist())
    assert ics_ids == ics_ids_expected


@pytest.mark.parametrize(
    "threshold, topic",
    [
        (0.5, "Body Image & Media"),
        (0.1, "Literature"),
        (0.9, "Music & Acoustics"),
        (0.3, "Business & Industry"),
        (0.4, "Conservation"),
    ],
)
def test_get_ics_ids_with_different_parameters(session, dataframes, threshold, topic):
    filtered_df = make_query_table(dataframes, threshold=threshold, topic=topic)
    ics_ids = sorted(get_ics_ids(threshold=threshold, topic=topic))
    ics_ids_expected = sorted(filtered_df.ics_id.unique().tolist())
    assert ics_ids == ics_ids_expected


@pytest.mark.parametrize(
    "threshold",
    [
        (0.1),
        (0.2),
        (0.3),
        (0.4),
        (0.5),
        (0.6),
        (0.7),
        (0.8),
        (0.9),
        (1.0),
    ],
)
def test_query_dashboard_data(session, dataframes, threshold):
    data = query_dashboard_data(threshold)
    ics_ids = get_ics_ids(threshold)
    filtered_df = make_query_table(dataframes, threshold)
    filtered_df = filtered_df[filtered_df.ics_id.isin(ics_ids)].drop_duplicates(
        subset=["country", "ics_id"]
    )
    data_expected = {}
    data_expected["countries_counts"] = filtered_df["country"].value_counts().to_dict()
    data_expected["funders_counts"] = filtered_df["funder"].value_counts().to_dict()
    data_expected["uoa_counts"] = filtered_df["name_x"].value_counts().to_dict()
    data_expected["institution_counts"] = (
        filtered_df["inst_name"].value_counts().to_dict()
    )
    country_counts = {
        x["country"]: x["country_count"] for x in data["countries_counts"]
    }
    del country_counts[""]
    assert json.dumps(country_counts, sort_keys=True) == json.dumps(
        data_expected["countries_counts"], sort_keys=True
    )
    assert True
    assert len(ics_ids) == len(filtered_df.drop_duplicates(subset="ics_id"))
