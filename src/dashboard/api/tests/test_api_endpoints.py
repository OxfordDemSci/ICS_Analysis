import pytest
import json

def test_get_init(session, app):
    with app.test_client() as client:
        response = client.get("/api/init")
        data = json.loads(response.data)
        assert response.status_code == 200
        assert isinstance(data["website_text"]["global_colourramp"], list)

def test_get_topics(session, app):
    with app.test_client() as client:
        response = client.get("/api/get_topics")
        data = json.loads(response.data)
        assert response.status_code == 200
        assert isinstance(data, list)
        topic_elements = data[0].keys()
        assert "topic_name" in topic_elements
        assert "topic_group" in topic_elements
        assert "description" in topic_elements
        assert "narrative" in topic_elements
        assert "keywords" in topic_elements
        assert data[0]["topic_name"] == "All Topics"

def test_download_csv(session, app):
    with app.test_client() as client:
        response = client.get("/api/download_csv?threshold=0.5")
        assert response.status_code == 200
        assert response.mimetype == "text/csv"

def test_ics_data(session, app):
    with app.test_client() as client:
        response = client.get("/api/get_ics_data?threshold=0.5")
        data = json.loads(response.data)
        assert response.status_code == 200
        assert sorted(data.keys()) == sorted([
                                            "countries_counts",
                                            "funders_counts",
                                            "uoa_counts",
                                            "institution_counts",
                                            "ics_table"
                                        ])


