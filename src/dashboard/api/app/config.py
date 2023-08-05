import os
from dotenv import load_dotenv
load_dotenv()

class Configuration:
    DEBUG = False
    DB_PASSWORD = os.environ.get('POSTGRES_READONLY_PASSWORD')
    DB_USERNAME = os.environ.get('POSTGRES_READONLY')
    POSTGRES_DB = os.environ.get('POSTGRES_DB')
    POSTGRES_DB_TEST = os.environ.get("POSTGRES_DB_TEST")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@ics_postgres:5432/{POSTGRES_DB}"
    TEST_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@ics_postgres:5432/{POSTGRES_DB_TEST}"
    DEBUG = True
    ENABLE_CORS = True
    FLASK_APP = "app.wsgi"
    JSON_SORT_KEYS = False

class DevelopmentConfig(Configuration):
    DEBUG = True
    # Override or add development-specific configuration variables here

class LocalDevelopmentConfig(Configuration):
    DB_PASSWORD = os.environ.get('POSTGRES_READONLY_PASSWORD')
    DB_USERNAME = os.environ.get('POSTGRES_READONLY')
    POSTGRES_DB = os.environ.get('POSTGRES_DB')
    POSTGRES_DB_TEST = os.environ.get("POSTGRES_DB_TEST")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/{POSTGRES_DB}"
    TEST_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/{POSTGRES_DB_TEST}"
    DEBUG=True


class ProductionConfig(Configuration):
    # Override or add production-specific configuration variables here
    pass

# Set the active configuration class based on an environment variable
app_config = {
    'development': DevelopmentConfig,
    'local_development': LocalDevelopmentConfig,
    'production': ProductionConfig
}