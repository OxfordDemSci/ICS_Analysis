from pathlib import Path

import connexion
import geopandas as gpd
from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy

from app.config import app_config

BASE_GEODATA = Path(__file__).resolve().parent.joinpath("data")
postcode_gdf = gpd.read_file(
    BASE_GEODATA.joinpath("geodata.gpkg"), layer="postcode_areas"
)
world_gdf = gpd.read_file(BASE_GEODATA.joinpath("geodata.gpkg"), layer="world")


db = SQLAlchemy()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["60/minute", "1000/hour", "10000/day"],
    strategy="fixed-window-elastic-expiry",
    storage_uri="",  # Set in create_app()
    storage_options={},
)


def create_app(config_name: str) -> Flask:
    connexion_app = connexion.FlaskApp(__name__, specification_dir="./")
    app = connexion_app.app
    app.config.from_object(app_config[config_name])
    connexion_app.add_api("api-config.yaml")
    db.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})
    if config_name == "local_development" or config_name == "testing":
        limiter._storage_uri = "memcached://localhost:11211"
    else:
        limiter._storage_uri = "memcached://ics_memcached:11211"
    limiter.init_app(app)
    return app
