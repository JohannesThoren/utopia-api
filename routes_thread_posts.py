from flask import Flask, blueprints
from flask_pymongo import PyMongo

import db_user, db_threads, db_thread_posts
import toml

settings = toml.load("settings.toml")
app = blueprints.Blueprint('api_thread_posts', __name__)
app.config["MONGO_URI"] = settings["settings"]["database-url"]
mongo = PyMongo(app)

@app.route('/<thread_id>/posts/new')
def thread_posts_new(thread_id):
      return

@app.route('/<thread_id>/posts/get/latest')
def thread_posts_latest(thread_id):
      return

@app.route('/<thread_id>/posts/get/all')
def thread_posts_all(thread_id):
      return

@app.route('/<thread_id>/posts/<post_id>/edit')
def thread_posts_specific_edit(thread_id, post_id):
      return

@app.route('/<thread_id>/posts/<post_id>/delete')
def thread_posts_specific_delete(thread_id, post_id):
      return

@app.route('/<thread_id>/posts/get/<post_id>')
def thread_posts_get_specific(thread_id, post_id):
      return

@app.route('/<thread_id>/posts/<post_id>/delete')
def thread_posts_specific_delete(thread_id, post_id):
      return

@app.route('/<thread_id>/posts/get/<post_id>/comments')
def thread_posts_get_specific_get_comments(thread_id, post_id):
      return

@app.route('/<thread_id>/posts/get/<post_id>/comments/new')
def thread_posts_get_specific_get_comments_new(thread_id, post_id):
      return

@app.route('/<thread_id>/posts/get/<post_id>/comments/<comment_id>')
def thread_posts_get_specific_get_comments_specific(thread_id, post_id, comment_id):
      return
