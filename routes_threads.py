from flask import Flask, blueprints
from flask_pymongo import PyMongo

import db_user, db_threads, db_thread_posts
import toml

settings = toml.load("settings.toml")
app = blueprints.Blueprint("api_threads", __name__)
app.config["MONGO_URI"] = settings["settings"]["database-url"]
mongo = PyMongo(app)

@app.route('/threads/all')
def threads_all():
      return

@app.route('/threads/<thread_id>')
def threads_new(thread_id):
      return

@app.route('/threads/<thread_id>/edit')
def threads_specific_modify(thread_id):
      return

@app.route('/threads/<thread_id>/delete')      
def threads_specific_delete(thread_id):
      return
