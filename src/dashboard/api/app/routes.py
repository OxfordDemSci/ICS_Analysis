from flask import request, current_app, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app import app, endpoints


# define rate limiting
limiter = Limiter(app,
                  key_func=get_remote_address,
                  # application_limits=['60/minute', '1000/hour', '10000/day'],
                  default_limits=['60/minute', '1000/hour', '10000/day'],
                  strategy='fixed-window-elastic-expiry',
                  storage_uri="memcached://cars_memcached:11211",
                  storage_options={}
                  )


@app.route('/')
def home():
    return current_app.send_static_file('docs.html')


@app.errorhandler(404)
def page_not_found(e):
    return f"<h1>404 Error</h1><p>The resource could not be found. {e}</p>", 404


