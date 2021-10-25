from flask import Flask, send_file
from flask_cors import CORS
from flask_pymongo import PyMongo
from werkzeug.datastructures import *


from routes_thread_posts import api_thread_posts
from routes_threads import api_threads
from routes_user import api_user

import toml
from db import mongo
settings = toml.load("settings.toml")


app = Flask(__name__)
app.config["MONGO_URI"] = settings["settings"]["database-url"]
cors = CORS(app, resources={r"/*": {"origins": "*"}})
mongo.init_app(app)

app.register_blueprint(api_user)
app.register_blueprint(api_threads)
app.register_blueprint(api_thread_posts)

@app.route("/profile_picture")
def profilepic():
      return send_file("assets/profile.png", mimetype='image/gif')

if __name__ == "__main__":
      app.run(host="0.0.0.0", port=3500)