from flask import Flask, blueprints, request
from flask_pymongo import PyMongo


import db, db_user, db_threads, db_thread_posts

api_thread_posts = blueprints.Blueprint('api_thread_posts', __name__)

@api_thread_posts.route('/thread/<thread_id>/post/new')
def thread_posts_new(thread_id):
      body = request.json
      return db_thread_posts.new_post(db.mongo, thread_id, body["token"], body["content"], body["title"])

@api_thread_posts.route('/thread/<thread_id>/posts/get/all')
def thread_posts_all(thread_id):
      return db_thread_posts.get_all_posts(db.mongo, thread_id)

@api_thread_posts.route('/post/<post_id>')
def thread_posts_get_specific(post_id):
      return db_thread_posts.get_specific_post(db.mongo, post_id)

@api_thread_posts.route('/post/<post_id>/edit')
def thread_posts_specific_edit(thread_id, post_id):
      body = request.json
      return

@api_thread_posts.route('/post/<post_id>/delete')
def thread_posts_specific_delete(post_id):
      body = request.json
      return db_thread_posts.delete_post(db.mongo, post_id, body["token"])

