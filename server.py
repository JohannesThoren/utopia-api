from flask import Flask
from flask_pymongo import PyMongo
from werkzeug.datastructures import *

import toml

import routes_thread_posts
import routes_user
import routes_threads

settings = toml.load("settings.toml")

app = Flask(__name__)
app.register_blueprint(routes_user.app)
app.register_blueprint(routes_thread_posts.app)
app.register_blueprint(routes_threads.app)


if __name__ == "__main__":
      app.run(host="0.0.0.0", port=3500)