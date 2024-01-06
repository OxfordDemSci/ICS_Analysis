import json
import logging
import socket
from pathlib import Path

import connexion  # type: ignore
import geopandas as gpd  # type: ignore
from flask import Flask, request
from flask_cors import CORS  # type: ignore
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy

from app.config import app_config

BASE = Path(__file__).resolve().parent
BASE_GEODATA = Path(__file__).resolve().parent.joinpath("data")
postcode_gdf = gpd.read_file(
    BASE_GEODATA.joinpath("geodata.gpkg"), layer="postcode_areas"
)
world_gdf = gpd.read_file(BASE_GEODATA.joinpath("geodata.gpkg"), layer="world")


def get_nginx_ip():
    try:
        nginx_ip = socket.gethostbyname("ics_nginx")
        return nginx_ip
    except socket.gaierror:
        return None


def is_exempt():
    nginx_ip = get_nginx_ip()
    return request.remote_addr == nginx_ip


db = SQLAlchemy()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["60/minute", "1000/hour", "10000/day"],
    strategy="fixed-window-elastic-expiry",
    storage_uri="",  # Set in create_app()
    storage_options={},
    default_limits_exempt_when=is_exempt,
)

try:
    assert BASE.joinpath("topic_map.json").exists()
except AssertionError:
    raise FileNotFoundError(
        "No topic_map found. You need to run ../scripts/reformat_csvs_for_db.py"
    )
with open(BASE.joinpath("topic_map.json"), "r") as f:
    TOPICS_BOOL_MAP = json.load(f)


def create_app(config_name: str) -> Flask:
    connexion_app = connexion.FlaskApp(__name__, specification_dir="./")
    app = connexion_app.app
    app.config.from_object(app_config[config_name])
    connexion_app.add_api("api-config.yaml")
    db.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})
    logging.basicConfig(level=logging.INFO)
    app.logger.addHandler(logging.StreamHandler())  # Log to the terminal
    app.logger.setLevel(logging.INFO)
    if config_name not in ["local_development", "testing"]:
        limiter._storage_uri = "memcached://ics_memcached:11211"
        limiter.init_app(app)
    return app
