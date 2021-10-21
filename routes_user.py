from flask import Flask, blueprints
from flask_pymongo import PyMongo

import db_user, db_threads, db_thread_posts
import toml

settings = toml.load("settings.toml")

app = blueprints.Blueprint("api_user", __name__)
app.config["MONGO_URI"] = settings["settings"]["database-url"]
mongo = PyMongo(app)

@app.route('/user/auth')
def authenticate():
      return 

@app.route('/user/new')
def user_new():
      return

@app.route('/user/edit')
def user_edit():
      return

@app.route('/user/delete')
def user_delet():
      return

@app.route('/<username>/get')
def user_get_by_name(username):
      return

@app.route('/<user_id>/get')
def user_get_by_id(user_id):
      return