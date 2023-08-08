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
        
@pytest.mark.parametrize("url, code", [
    ("/api/get_ics_data?threshold=0.9", 200),
    ("/api/get_ics_data", 400),
    ("/api/get_ics_data?thresholds=0.1", 400),
    ("/api/get_ics_data?threshold=-1", 400),
    ("/api/get_ics_data?threshold=2", 400),
    ("/api/get_ics_data?theshold=big", 400),
    ("/api/get_ics_data?threshold=0.5&topic=Not_a_topic", 400),
    ("/api/get_ics_data?threshold=1&topic=Cultural%20Capital", 204),
    ("/api/not_an_endpoint", 404)
])
def test_http_codes(session, app, url, code):
    with app.test_client() as client:
        response = client.get(url)
        assert response.status_code == code


