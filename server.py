from flask import Flask, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from werkzeug.datastructures import *

from routes_board_posts import api_board_posts
from routes_boards import api_boards
from routes_user import api_user

import toml
from db import mongo
settings = toml.load("settings.toml")


app = Flask(__name__)
app.config["MONGO_URI"] = settings["settings"]["database-url"]
cors = CORS(app, resources={r"/*": {"origins": "*"}})
mongo.init_app(app)

app.register_blueprint(api_user)
app.register_blueprint(api_boards)
app.register_blueprint(api_board_posts)

if __name__ == "__main__":
      app.run(host="0.0.0.0", port=3500, debug=True)