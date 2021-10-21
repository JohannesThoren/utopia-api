import re
from flask import Flask, blueprints, request
from flask_pymongo import PyMongo

import db, db_user, db_threads, db_thread_posts

api_user = blueprints.Blueprint("api_user", __name__)

@api_user.route('/user/auth')
def authenticate():
      return 


@api_user.route('/user/new')
def user_new():
      body = request.json
      if db_user.create_user(db.mongo, body["username"],body["password"],body["email"]):
            return {"response code": 200, "username": body["username"]}
      else:
            return {"response code": 403}
@api_user.route('/user/edit')
def user_edit():
      return

@api_user.route('/user/delete')
def user_delet():
      return

@api_user.route('/<username>/get')
def user_get_by_name(username):
      return

@api_user.route('/<user_id>/get')
def user_get_by_id(user_id):
      return