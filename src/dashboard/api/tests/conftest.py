from pathlib import Path
import pytest

from flask import Flask
import sqlalchemy as sa
from app import db as _db
from app import create_app
from alembic import command
from alembic.config import Config

from .make_test_data import insert_test_data


ALEMBIC = Path(__file__).resolve().parent.parent.joinpath('alembic.ini').resolve()

@pytest.fixture
def exist():
    return ALEMBIC

@pytest.fixture(scope='session')
def app():
    app = create_app('testing')
    with app.app_context():
        yield app

@pytest.fixture(scope="session")
def db(app: Flask):
    #Set up the test db and apply alembic migrations
    alembic_cfg = Config(ALEMBIC)
    alembic_cfg.set_main_option("sqlalchemy.url", app.config["TEST_DATABASE_URI"])
    with app.app_context():
        _db.create_all()
        command.upgrade(alembic_cfg, "head")

        # Insert test data
        with _db.session.begin_nested():
            insert_test_data(_db.session)

        yield _db
        _db.drop_all()
        _db.engine.dispose()


@pytest.fixture(scope="session")
def session(app, db):
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        session_factory = sa.orm.sessionmaker(bind=connection)
        session = sa.orm.scoped_session(session_factory)

        _db.session = session

        yield session

        transaction.rollback()
        connection.close()
        session.remove()

        # Teardown tables
        meta = sa.MetaData()
        meta.reflect(bind=db.engine)
        for table in reversed(meta.sorted_tables):
            table.drop(bind=db.engine)