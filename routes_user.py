import re
from flask import Flask, blueprints, request
from flask_pymongo import PyMongo

import db, db_user, db_threads, db_thread_posts

api_user = blueprints.Blueprint("api_user", __name__)

@api_user.route('/user/get/token')
def authenticate():
      body = request.json
      return db_user.get_token(db.mongo, body["username"], body["password"])

@api_user.route('/user/new')
def user_new():
      body = request.json
      return db_user.create_user(db.mongo, body["username"],body["password"],body["email"])

@api_user.route('/user/edit')
def user_edit():
      return

@api_user.route('/user/delete')
def user_delete():
      return

@api_user.route('/user/get/username/<username>')
def user_get_by_name(username):
      return db_user.get_user_by_name(db.mongo, username)

@api_user.route('/user/get/id/<user_id>')
def user_get_by_id(user_id):
      return db_user.get_user_by_id(db.mongo, user_id)

@api_user.route('/user/get/token/<token>')
def user_get_by_token(token):
      return db_user.get_user_by_token(db.mongo, token)
      