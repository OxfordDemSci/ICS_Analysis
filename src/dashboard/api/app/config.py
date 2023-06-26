class Configuration:
    DEBUG = False
    DB_PASSWORD="Fp2mQC4&#7JZ"
    DB_USERNAME="david"
    SQLALCHEMY_DATABASE_URI="postgresql://david:Fp2mQC4&#7JZ@ics_postgres:5432/ics"
    TEST_DATABASE_URI="postgresql://david:Fp2mQC4&#7JZ@ics_postgres:5432/ics_test"
    DEBUG=True
    ENABLE_CORS=True
    FLASK_APP="app.wsgi"
    JSON_SORT_KEYS=False

class DevelopmentConfig(Configuration):
    DEBUG = True
    # Override or add development-specific configuration variables here

class ProductionConfig(Configuration):
    # Override or add production-specific configuration variables here
    pass

# Set the active configuration class based on an environment variable
app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}