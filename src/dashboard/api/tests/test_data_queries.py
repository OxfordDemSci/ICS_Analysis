import pytest
import pandas as pd
from pathlib import Path

from app.data_queries import (
    get_topics,
)

TEST_DATA = Path(__file__).resolve().parent.joinpath('test_data')

@pytest.fixture
def topics_df():
    df = pd.read_csv(TEST_DATA.joinpath('TOPICS_TABLE.csv'))
    yield df

@pytest.mark.parametrize("topic", [
    (None),
    ("Body Image & Media"),
    ("Health & Wellbeing"),
    ("Gaelic Preservation"),
    ("Cultural Engagement")
])
def test_get_topics(session, topics_df, topic):
    topics = get_topics(topic=topic)
    if topic is not None:
        topics_df = topics_df[topics_df.topic_name == topic]
    topic_names = [x['topic_name'] for x in topics if not x['topic_name'] == "All Topics"]
    topic_groups = [x['topic_group'] for x in topics if not x['topic_name'] == "All Topics"]
    topic_keywords = [x['keywords'] for x in topics if not x['topic_name'] == "All Topics"]
    assert sorted(topic_names) == sorted(topics_df.topic_name.tolist())
    assert sorted(topic_groups) == sorted(topics_df.topic_group.tolist())
    assert sorted(topic_keywords) == sorted(topics_df.keywords.tolist())
    if topic is None:
        assert "All Topics" in [x["topic_name"] for x in topics]



