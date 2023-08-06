import pytest

# def test_true(exist):
#     print(exist)
#     print(exist.exists())
#     assert True

# def test_app(app):
#     print(app.config)
#     print(dir(app))
#     assert True

# def test_db(db):
#     print(db)
#     print(dir(db))
#     assert True

def test_example(app, session):
    print(app)
    print(dir(app))
    print(session)
    print(dir(session))
    assert True