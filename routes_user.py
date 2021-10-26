from flask import Flask, blueprints, request
from flask_pymongo import PyMongo

import json

import db
import db_user
import db_threads
import db_thread_posts

api_user = blueprints.Blueprint("api_user", __name__)

# TODO All routess that should be a post request, should have all data in the body


@api_user.route('/user/auth',methods=['POST'])
def authenticate():
    body = json.loads(request.get_data().decode("UTF-8"))
    return db_user.get_token(db.mongo, body["username"], body["password"])

@api_user.route('/user/new',methods=['POST'])
def user_new():
    body = json.loads(request.get_data().decode("UTF-8"))
    return db_user.create_user(db.mongo, body["username"], body["password"], body["email"])

@api_user.route('/user/edit',methods=['POST'])
def user_edit():
    body = json.loads(request.get_data().decode("UTF-8"))
    return body

@api_user.route('/user/delete',methods=['POST'])
def user_delete():
    body = json.loads(request.get_data().decode("UTF-8"))
    return db_user.delete_user(db.mongo, body["token"])


@api_user.route('/user/get/username/<username>')
def user_get_by_name(username):
    return db_user.get_user_by_name(db.mongo, username)


@api_user.route('/user/get/id/<user_id>')
def user_get_by_id(user_id):
    return db_user.get_user_by_id(db.mongo, user_id)


@api_user.route('/user/get/token/<token>')
def user_get_by_token(token):
    return db_user.get_user_by_token(db.mongo, token)
