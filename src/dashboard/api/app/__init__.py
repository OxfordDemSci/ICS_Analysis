from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import connexion
from pathlib import Path
import geopandas as gpd

from app.config import app_config

BASE_GEODATA = Path(__file__).resolve().parent.joinpath('data')
postcode_gdf = gpd.read_file(BASE_GEODATA.joinpath("geodata.gpkg"), layer="postcode_areas")
world_gdf = gpd.read_file(BASE_GEODATA.joinpath("geodata.gpkg"), layer="world")


db = SQLAlchemy()

def create_app(config_name: str) -> Flask:
    connexion_app = connexion.FlaskApp(__name__, specification_dir='./')
    app = connexion_app.app
    app.config.from_object(app_config[config_name])
    connexion_app.add_api('api-config.yaml')
    db.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})
    return app


