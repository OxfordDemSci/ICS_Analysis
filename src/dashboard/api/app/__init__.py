from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

from app import routes

# Cross Origin Resource Sharing (for AJAX)
CORS(app)

# specify the Google Analytics key here
app.config["GA_KEY"] = ''

# don't sort JSON elements alphabetically
app.config['JSON_SORT_KEYS'] = False
